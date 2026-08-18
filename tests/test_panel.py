import datetime as dt

import numpy as np
import polars as pl
import pytest

from fin_crypto_lab.panel import (
    Panel,
    build_panel,
    crypto_sessions,
    weekly_formations,
)
from fin_crypto_lab.store import write_ohlcv


def test_crypto_sessions_includes_weekends():
    s = crypto_sessions("2024-01-01", "2024-01-07")
    assert len(s) == 7
    dates = s.to_list()
    assert dt.date(2024, 1, 6) in dates
    assert dt.date(2024, 1, 7) in dates


def test_crypto_sessions_single_day():
    s = crypto_sessions("2024-01-01", "2024-01-01")
    assert len(s) == 1


def test_weekly_formations_sundays():
    s = crypto_sessions("2024-01-01", "2024-01-31")
    forms = weekly_formations(s)
    assert all(d.weekday() == 6 for d in forms)
    assert dt.date(2024, 1, 7) in forms
    assert dt.date(2024, 1, 14) in forms


def test_build_panel_basic(tmp_path):
    df = pl.DataFrame({
        "date": [dt.date(2024, 1, 1), dt.date(2024, 1, 2), dt.date(2024, 1, 3)],
        "open": [100.0, 101.0, 102.0],
        "high": [105.0, 106.0, 107.0],
        "low": [95.0, 96.0, 97.0],
        "close": [103.0, 104.0, 105.0],
        "volume": [10.0, 20.0, 30.0],
        "trade_count": [100, 200, 300],
        "vwap": [101.0, 102.0, 103.0],
    })
    write_ohlcv(df, "XBTUSD", last_trade_id=1, trade_count=600,
                data_dir=tmp_path)
    sessions = crypto_sessions("2024-01-01", "2024-01-03")
    p = build_panel(["XBTUSD"], sessions, data_dir=tmp_path)
    assert p.close.shape == (3, 1)
    assert p.close[0, 0] == 103.0
    assert p.tradable[0, 0] is np.True_


def test_build_panel_forward_fills_close(tmp_path):
    df = pl.DataFrame({
        "date": [dt.date(2024, 1, 1), dt.date(2024, 1, 3)],
        "open": [100.0, 102.0],
        "high": [105.0, 107.0],
        "low": [95.0, 97.0],
        "close": [103.0, 105.0],
        "volume": [10.0, 30.0],
        "trade_count": [100, 300],
        "vwap": [101.0, 103.0],
    })
    write_ohlcv(df, "XBTUSD", last_trade_id=1, trade_count=400,
                data_dir=tmp_path)
    sessions = crypto_sessions("2024-01-01", "2024-01-03")
    p = build_panel(["XBTUSD"], sessions, data_dir=tmp_path)
    assert p.close_ff[1, 0] == 103.0
    assert not p.tradable[1, 0]


def test_session_index():
    sessions = crypto_sessions("2024-01-01", "2024-01-05")
    p = Panel(
        sessions=sessions, symbols=["A"],
        open=np.ones((5, 1)), high=np.ones((5, 1)), low=np.ones((5, 1)),
        close=np.ones((5, 1)), close_ff=np.ones((5, 1)),
        volume=np.ones((5, 1)), vwap=np.ones((5, 1)),
        tradable=np.ones((5, 1), dtype=bool),
    )
    assert p.session_index(dt.date(2024, 1, 1)) == 0
    assert p.session_index(dt.date(2024, 1, 3)) == 2
    with pytest.raises(KeyError):
        p.session_index(dt.date(2024, 2, 1))
