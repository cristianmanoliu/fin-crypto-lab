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
    get_ohlc,
    get_trades,
    RATE_LIMIT_S,
)
from fin_crypto_lab.store import read_manifest, write_ohlcv

log = logging.getLogger("fin_crypto_lab.download")


def plan_downloads(data_dir: Path, top: int | None = None) -> list[dict]:
    """Plan which pairs to download and from where to resume.

    If *top* is set, only plan downloads for the top-N pairs by average
    daily USD volume (measured from existing OHLCV data on disk).  Pairs
    outside the cutoff keep whatever data they already have."""
    pairs = get_asset_pairs()
    manifest = read_manifest(data_dir)
    since_map = dict(
        zip(manifest["pair"].to_list(), manifest["last_trade_id"].to_list())
    )

    selected = set(pairs.keys())
    if top is not None:
        selected = _top_pairs_by_volume(data_dir, manifest, top)
        log.info("top-%d filter: %d pairs selected for full download", top, len(selected))

    plans = []
    for altname, info in sorted(pairs.items()):
        if altname not in selected:
            continue
        plans.append({
            "pair": altname,
            "kraken_name": info.get("kraken_name", altname),
            "since": since_map.get(altname, EPOCH_2017_NS),
        })
    return plans


def _top_pairs_by_volume(
    data_dir: Path, manifest: pl.DataFrame, top: int,
) -> set[str]:
    """Return the *top* pairs by average daily USD volume from on-disk OHLCV."""
    ohlcv_dir = data_dir / "ohlcv"
    vols: list[tuple[str, float]] = []
    for pair in manifest["pair"].to_list():
        path = ohlcv_dir / f"{pair}.parquet"
        if not path.exists():
            continue
        try:
            df = pl.read_parquet(path)
            avg = float((df["close"] * df["volume"]).mean())
            vols.append((pair, avg))
        except Exception:
            continue
    vols.sort(key=lambda x: -x[1])
    return {p for p, _ in vols[:top]}


CHECKPOINT_PAGES = 500


def download_pair(
    pair: str, kraken_name: str, since: int | None,
    data_dir: Path, existing_trades: list[Trade] | None = None,
) -> None:
    """Fetch all trades for a pair, aggregate, write to store.

    Checkpoints to disk every CHECKPOINT_PAGES pages so that a restart
    resumes mid-pair instead of re-downloading from epoch."""
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
        if page % CHECKPOINT_PAGES == 0:
            _flush(pair, all_trades, last, data_dir)
            log.info("  %s: checkpoint at page %d", pair, page)
        time.sleep(RATE_LIMIT_S)

    if not all_trades:
        log.warning("%s: no trades fetched", pair)
        return

    _flush(pair, all_trades, last, data_dir)
    log.info("%s: %d days (final), last_id=%s", pair,
             trades_to_daily(all_trades).height, last)


def _flush(pair: str, trades: list[Trade], last_id: int, data_dir: Path) -> None:
    """Aggregate trades to daily OHLCV, merge with existing data, write."""
    df = trades_to_daily(trades)
    if df.height == 0:
        return
    existing_path = data_dir / "ohlcv" / f"{pair}.parquet"
    if existing_path.exists():
        old = pl.read_parquet(existing_path)
        df = pl.concat([old, df], how="vertical_relaxed").unique(
            subset=["date"], keep="last"
        ).sort("date")
    write_ohlcv(df, pair, last_trade_id=last_id or 0,
                trade_count=len(trades), data_dir=data_dir)


def download_pair_fast(pair: str, kraken_name: str, data_dir: Path) -> None:
    """Fetch daily OHLC candles via /public/OHLC — one call per pair.
    OHLC returns full history (~720 candles max), no merge needed."""
    rows = get_ohlc(kraken_name, interval=1440)
    if not rows:
        log.warning("%s: no OHLC data", pair)
        return
    df = pl.DataFrame(rows).cast({"trade_count": pl.Int64})
    total_trades = int(df["trade_count"].sum())
    write_ohlcv(df, pair, last_trade_id=0, trade_count=total_trades,
                data_dir=data_dir)
    log.info("%s: %d days (fast/OHLC)", pair, df.height)


def main() -> int:
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s")
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, default=config.SPOT_DATA_DIR)
    parser.add_argument("--fast", action="store_true",
                        help="Use /public/OHLC (1 call/pair) instead of /public/Trades")
    parser.add_argument("--top", type=int, default=None,
                        help="Only download the top-N pairs by USD volume")
    args = parser.parse_args()

    plans = plan_downloads(args.data_dir, top=args.top)
    log.info("downloading %d pairs to %s%s", len(plans), args.data_dir,
             " (FAST/OHLC mode)" if args.fast else "")
    errors = 0
    for i, p in enumerate(plans, 1):
        log.info("[%d/%d] %s", i, len(plans), p["pair"])
        try:
            if args.fast:
                download_pair_fast(p["pair"], p["kraken_name"], args.data_dir)
            else:
                download_pair(p["pair"], p["kraken_name"], p["since"],
                              args.data_dir)
        except Exception:
            log.exception("FAILED: %s", p["pair"])
            errors += 1
        time.sleep(RATE_LIMIT_S)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
