import datetime as dt

import polars as pl

from fin_crypto_lab.aggregate import trades_to_daily
from fin_crypto_lab.kraken_client import Trade


def _make_trade(price, volume, ts, side="b"):
    return Trade(price=price, volume=volume, timestamp=ts,
                 side=side, order_type="m", trade_id=0)


def test_trades_to_daily_single_day():
    trades = [
        _make_trade(42000.0, 1.0, 1704067200.0),   # 2024-01-01 00:00:00
        _make_trade(42500.0, 2.0, 1704070800.0),   # 2024-01-01 01:00:00
    ]
    df = trades_to_daily(trades)
    assert df.height == 1
    assert df["date"][0] == dt.date(2024, 1, 1)
    assert df["open"][0] == 42000.0
    assert df["high"][0] == 42500.0
    assert df["low"][0] == 42000.0
    assert df["close"][0] == 42500.0
    assert df["volume"][0] == 3.0
    assert df["trade_count"][0] == 2
    assert abs(df["vwap"][0] - 42333.333) < 1.0


def test_trades_to_daily_multi_day():
    trades = [
        _make_trade(100.0, 1.0, 1704067200.0),   # 2024-01-01
        _make_trade(200.0, 1.0, 1704153600.0),   # 2024-01-02
    ]
    df = trades_to_daily(trades)
    assert df.height == 2
    assert df["date"].to_list() == [dt.date(2024, 1, 1), dt.date(2024, 1, 2)]


def test_trades_to_daily_empty():
    df = trades_to_daily([])
    assert df.height == 0
    assert "date" in df.columns


def test_trades_to_daily_sorted_by_date():
    trades = [
        _make_trade(200.0, 1.0, 1704153600.0),   # 2024-01-02
        _make_trade(100.0, 1.0, 1704067200.0),   # 2024-01-01
    ]
    df = trades_to_daily(trades)
    assert df["date"].to_list() == [dt.date(2024, 1, 1), dt.date(2024, 1, 2)]
