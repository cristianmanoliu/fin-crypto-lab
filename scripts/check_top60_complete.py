"""Data gate DG-1 and DG-2 for the deep spot sweep. Exit 0 only when every
top-60 pair has a trade checkpoint on or after CUTOFF and no unexplained gap.
Run: uv run python scripts/check_top60_complete.py"""
import datetime as dt
import sys
from pathlib import Path

import polars as pl

from fin_crypto_lab.download import _top_pairs_by_volume, read_manifest

DATA = Path("data/spot")
CUTOFF = dt.date(2026, 9, 1)
MAX_GAP_DAYS = 7
# Kraken-side thin stretches from completed trade runs; see the pre-reg.
ACCEPTED_GAPS = {("LTCUSD", 2013), ("LTCUSD", 2014), ("LTCUSD", 2015),
                 ("XLMUSD", 2018)}


def main() -> int:
    m = read_manifest(DATA)
    top = _top_pairs_by_volume(DATA, m, 60)
    rows = m.filter(pl.col("pair").is_in(list(top))).with_columns(
        checkpoint=(pl.col("last_trade_id") // 10**6)
        .cast(pl.Datetime("ms")).dt.date())
    bad = rows.filter((pl.col("last_trade_id") == 0)
                      | (pl.col("checkpoint") < CUTOFF))
    print(f"DG-1: {rows.height - bad.height}/{rows.height} pairs "
          f"checkpointed on or after {CUTOFF}")
    if bad.height:
        print(bad.select(["pair", "checkpoint"]))

    gaps = []
    for pair in top:
        df = pl.read_parquet(DATA / "ohlcv" / f"{pair}.parquet").sort("date")
        g = df.select("date").with_columns(
            gap=(pl.col("date") - pl.col("date").shift(1)).dt.total_days()
        ).filter(pl.col("gap") > MAX_GAP_DAYS)
        for d, n in g.rows():
            if (pair, d.year) not in ACCEPTED_GAPS:
                gaps.append((pair, d, n))
    print(f"DG-2: {len(gaps)} unexplained gaps > {MAX_GAP_DAYS} days")
    for row in gaps:
        print("  ", row)
    ok = bad.height == 0 and not gaps
    print("GATE:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
