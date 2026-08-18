import datetime as dt

import polars as pl
import pytest

from fin_crypto_lab.store import (
    MANIFEST_SCHEMA,
    read_manifest,
    read_ohlcv,
    write_ohlcv,
)


def test_manifest_schema_has_required_keys():
    assert set(MANIFEST_SCHEMA) >= {
        "pair", "first_date", "last_date", "rows",
        "last_trade_id", "trade_count", "downloaded_at",
    }


def test_read_manifest_empty(tmp_path):
    m = read_manifest(tmp_path)
    assert m.height == 0
    assert "pair" in m.columns


def test_write_and_read_ohlcv(tmp_path):
    df = pl.DataFrame({
        "date": [dt.date(2024, 1, 1), dt.date(2024, 1, 2)],
        "open": [42000.0, 42500.0],
        "high": [42500.0, 43000.0],
        "low": [41500.0, 42000.0],
        "close": [42200.0, 42800.0],
        "volume": [100.5, 200.3],
        "trade_count": [5000, 6000],
        "vwap": [42100.0, 42600.0],
    })
    write_ohlcv(df, "XBTUSD", last_trade_id=99999, trade_count=11000,
                data_dir=tmp_path)
    m = read_manifest(tmp_path)
    assert m.height == 1
    assert m["pair"][0] == "XBTUSD"
    assert m["last_trade_id"][0] == 99999

    got = read_ohlcv("XBTUSD", data_dir=tmp_path)
    assert got.height == 2
    assert got["close"][0] == 42200.0


def test_read_ohlcv_missing_pair(tmp_path):
    with pytest.raises(KeyError):
        read_ohlcv("NOSUCH", data_dir=tmp_path)


def test_write_ohlcv_upserts_manifest(tmp_path):
    df1 = pl.DataFrame({
        "date": [dt.date(2024, 1, 1)],
        "open": [1.0], "high": [1.0], "low": [1.0], "close": [1.0],
        "volume": [1.0], "trade_count": [1], "vwap": [1.0],
    })
    df2 = pl.DataFrame({
        "date": [dt.date(2024, 1, 1), dt.date(2024, 1, 2)],
        "open": [1.0, 2.0], "high": [1.0, 2.0], "low": [1.0, 2.0],
        "close": [1.0, 2.0], "volume": [1.0, 2.0],
        "trade_count": [1, 2], "vwap": [1.0, 2.0],
    })
    write_ohlcv(df1, "XBTUSD", last_trade_id=100, trade_count=1,
                data_dir=tmp_path)
    write_ohlcv(df2, "XBTUSD", last_trade_id=200, trade_count=3,
                data_dir=tmp_path)
    m = read_manifest(tmp_path)
    assert m.height == 1
    assert m["rows"][0] == 2
    assert m["last_trade_id"][0] == 200
