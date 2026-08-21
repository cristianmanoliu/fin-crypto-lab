"""Download orchestrator. Fetches all USD-quoted pairs from Kraken,
paginates trades, aggregates to daily OHLCV, writes to store.

Run: uv run python -m fin_crypto_lab.download [--data-dir data/spot]
Exit 0 = success, 1 = partial (some pairs failed)."""
import argparse
import logging
import sys
import time
from pathlib import Path

import polars as pl

# 2017-01-01 00:00:00 UTC in nanoseconds — Kraken `since` param unit
EPOCH_2017_NS = 1_483_228_800_000_000_000

from fin_crypto_lab import config
from fin_crypto_lab.aggregate import trades_to_daily
from fin_crypto_lab.kraken_client import (
    KrakenError,
    Trade,
    get_asset_pairs,
    get_trades,
    RATE_LIMIT_S,
)
from fin_crypto_lab.store import read_manifest, write_ohlcv

log = logging.getLogger("fin_crypto_lab.download")


def plan_downloads(data_dir: Path) -> list[dict]:
    """Plan which pairs to download and from where to resume."""
    pairs = get_asset_pairs()
    manifest = read_manifest(data_dir)
    since_map = dict(
        zip(manifest["pair"].to_list(), manifest["last_trade_id"].to_list())
    )
    plans = []
    for altname, info in sorted(pairs.items()):
        plans.append({
            "pair": altname,
            "kraken_name": info.get("kraken_name", altname),
            "since": since_map.get(altname, EPOCH_2017_NS),
        })
    return plans


def download_pair(
    pair: str, kraken_name: str, since: int | None,
    data_dir: Path, existing_trades: list[Trade] | None = None,
) -> None:
    """Fetch all trades for a pair, aggregate, write to store."""
    all_trades: list[Trade] = list(existing_trades or [])
    last = since
    page = 0
    while True:
        trades, new_last = get_trades(kraken_name, since=last)
        if not trades or new_last == last:
            break
        all_trades.extend(trades)
        last = new_last
        page += 1
        if page % 100 == 0:
            log.info("  %s: %d pages, %d trades", pair, page, len(all_trades))
        time.sleep(RATE_LIMIT_S)

    if not all_trades:
        log.warning("%s: no trades fetched", pair)
        return

    df = trades_to_daily(all_trades)
    if df.height == 0:
        log.warning("%s: trades aggregated to 0 daily bars", pair)
        return

    # Merge with existing data on incremental resume
    existing_path = data_dir / "ohlcv" / f"{pair}.parquet"
    if existing_path.exists() and since is not None:
        old = pl.read_parquet(existing_path)
        df = pl.concat([old, df], how="vertical_relaxed").unique(subset=["date"], keep="last").sort("date")

    total_count = len(all_trades)
    write_ohlcv(df, pair, last_trade_id=last or 0,
                trade_count=total_count, data_dir=data_dir)
    log.info("%s: %d days, %d trades, last_id=%s", pair, df.height,
             total_count, last)


def main() -> int:
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s")
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, default=config.SPOT_DATA_DIR)
    args = parser.parse_args()

    plans = plan_downloads(args.data_dir)
    log.info("downloading %d pairs to %s", len(plans), args.data_dir)
    errors = 0
    for i, p in enumerate(plans, 1):
        log.info("[%d/%d] %s (since=%s)", i, len(plans), p["pair"], p["since"])
        try:
            download_pair(p["pair"], p["kraken_name"], p["since"],
                          args.data_dir)
        except Exception:
            log.exception("FAILED: %s", p["pair"])
            errors += 1
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
