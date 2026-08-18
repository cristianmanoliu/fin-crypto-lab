"""Aggregate raw Kraken trades into daily OHLCV candles.
Day boundary: 00:00 UTC."""
import datetime as dt

import polars as pl

from fin_crypto_lab.kraken_client import Trade


def trades_to_daily(trades: list[Trade]) -> pl.DataFrame:
    """Convert a list of Trade objects to daily OHLCV DataFrame."""
    if not trades:
        return pl.DataFrame(schema={
            "date": pl.Date, "open": pl.Float64, "high": pl.Float64,
            "low": pl.Float64, "close": pl.Float64, "volume": pl.Float64,
            "trade_count": pl.Int64, "vwap": pl.Float64,
        })
    rows = pl.DataFrame({
        "timestamp": [t.timestamp for t in trades],
        "price": [t.price for t in trades],
        "volume": [t.volume for t in trades],
    }).with_columns(
        date=pl.from_epoch(pl.col("timestamp").cast(pl.Int64)).dt.date(),
        notional=pl.col("price") * pl.col("volume"),
    )
    return (
        rows.sort("timestamp")
        .group_by("date")
        .agg(
            open=pl.col("price").first(),
            high=pl.col("price").max(),
            low=pl.col("price").min(),
            close=pl.col("price").last(),
            volume=pl.col("volume").sum(),
            trade_count=pl.len(),
            vwap=pl.col("notional").sum() / pl.col("volume").sum(),
        )
        .sort("date")
    )
