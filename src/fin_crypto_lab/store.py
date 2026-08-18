"""Parquet OHLCV store for crypto pairs. One file per pair, plus a
manifest tracking spans and the last trade ID for incremental fetch."""
import datetime as dt
from pathlib import Path

import polars as pl

from fin_crypto_lab import config

MANIFEST_SCHEMA = {
    "pair": pl.Utf8,
    "first_date": pl.Date,
    "last_date": pl.Date,
    "rows": pl.Int64,
    "last_trade_id": pl.Int64,
    "trade_count": pl.Int64,
    "downloaded_at": pl.Datetime("us"),
}


def read_manifest(data_dir: Path = config.SPOT_DATA_DIR) -> pl.DataFrame:
    path = data_dir / "manifest.parquet"
    if path.exists():
        return pl.read_parquet(path)
    return pl.DataFrame(schema=MANIFEST_SCHEMA)


def _upsert_manifest(
    pair: str, df: pl.DataFrame, last_trade_id: int,
    trade_count: int, data_dir: Path,
) -> None:
    path = data_dir / "manifest.parquet"
    entry = pl.DataFrame({
        "pair": [pair],
        "first_date": [df["date"][0]],
        "last_date": [df["date"][-1]],
        "rows": [df.height],
        "last_trade_id": [last_trade_id],
        "trade_count": [trade_count],
        "downloaded_at": [dt.datetime.now()],
    }, schema=MANIFEST_SCHEMA)
    manifest = read_manifest(data_dir).filter(pl.col("pair") != pair)
    path.parent.mkdir(parents=True, exist_ok=True)
    pl.concat([manifest, entry]).write_parquet(path)


def write_ohlcv(
    df: pl.DataFrame, pair: str, last_trade_id: int, trade_count: int,
    data_dir: Path = config.SPOT_DATA_DIR,
) -> None:
    df = df.sort("date")
    ohlcv_dir = data_dir / "ohlcv"
    ohlcv_dir.mkdir(parents=True, exist_ok=True)
    df.write_parquet(ohlcv_dir / f"{pair}.parquet")
    _upsert_manifest(pair, df, last_trade_id, trade_count, data_dir)


def read_ohlcv(
    pair: str, data_dir: Path = config.SPOT_DATA_DIR,
    manifest: pl.DataFrame | None = None,
) -> pl.DataFrame:
    if manifest is None:
        manifest = read_manifest(data_dir)
    row = manifest.filter(pl.col("pair") == pair)
    if row.height == 0:
        raise KeyError(f"{pair}: not in manifest")
    path = data_dir / "ohlcv" / f"{pair}.parquet"
    return pl.read_parquet(path)
