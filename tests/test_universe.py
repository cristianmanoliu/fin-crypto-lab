import datetime as dt

import polars as pl
import pytest

from fin_crypto_lab.store import write_ohlcv
from fin_crypto_lab.universe import UNIVERSE_SCHEMA, build_universe


def _write_pair(tmp_path, pair, dates, closes, volumes):
    df = pl.DataFrame({
        "date": dates,
        "open": closes, "high": closes, "low": closes, "close": closes,
        "volume": volumes,
        "trade_count": [100] * len(dates),
        "vwap": closes,
    })
    write_ohlcv(df, pair, last_trade_id=1, trade_count=100 * len(dates),
                data_dir=tmp_path)


def test_universe_schema():
    assert set(UNIVERSE_SCHEMA) >= {"snapshot_date", "symbol", "rank",
                                     "avg_daily_volume"}


def test_build_universe_ranks_by_volume(tmp_path):
    dates = [dt.date(2024, 1, 1) + dt.timedelta(days=i) for i in range(100)]
    _write_pair(tmp_path, "XBTUSD", dates, [40000.0] * 100, [500.0] * 100)
    _write_pair(tmp_path, "ETHUSD", dates, [2000.0] * 100, [3000.0] * 100)
    _write_pair(tmp_path, "SOLUSD", dates, [100.0] * 100, [10000.0] * 100)

    formations = [dt.date(2024, 4, 7)]
    u = build_universe(tmp_path / "ohlcv", formations, lookback=90, top_n=2)
    assert u.height == 2
    symbols = u.sort("rank")["symbol"].to_list()
    assert symbols[0] == "XBTUSD"
    assert symbols[1] == "ETHUSD"


def test_build_universe_excludes_short_history(tmp_path):
    dates_long = [dt.date(2024, 1, 1) + dt.timedelta(days=i) for i in range(100)]
    dates_short = [dt.date(2024, 3, 1) + dt.timedelta(days=i) for i in range(10)]
    _write_pair(tmp_path, "XBTUSD", dates_long, [40000.0] * 100, [500.0] * 100)
    _write_pair(tmp_path, "NEWUSD", dates_short, [1.0] * 10, [1000000.0] * 10)

    formations = [dt.date(2024, 4, 7)]
    u = build_universe(tmp_path / "ohlcv", formations, lookback=90, top_n=10)
    symbols = u["symbol"].to_list()
    assert "XBTUSD" in symbols
    assert "NEWUSD" not in symbols
