import datetime as dt

import numpy as np
import polars as pl
import pytest

from fin_crypto_lab.backtest import BacktestResult, run_backtest, slippage_sweep
from fin_crypto_lab.panel import Panel


def _make_panel():
    dates = [dt.date(2024, 1, d) for d in range(1, 11)]
    sessions = pl.Series(dates)
    n = 2
    t = 10
    close = np.array([[100.0, 50.0]] * t)
    close[5:, 0] = 110.0
    return Panel(
        sessions=sessions, symbols=["A", "B"],
        open=close.copy(), high=close.copy(), low=close.copy(),
        close=close.copy(), close_ff=close.copy(),
        volume=np.ones((t, n)) * 1000.0,
        vwap=close.copy(),
        tradable=np.ones((t, n), dtype=bool),
    )


def test_run_backtest_basic():
    p = _make_panel()
    targets = pl.DataFrame({
        "formation_date": [dt.date(2024, 1, 2)],
        "symbol": ["A"],
        "weight": [1.0],
    })
    cost_fn = lambda notional: 0.008
    res = run_backtest(p, targets, nav0=100_000, slip_bp=0.0,
                       cost_frac_fn=cost_fn)
    assert isinstance(res, BacktestResult)
    assert res.nav.height == 10
    assert res.nav["nav"][0] == 100_000


def test_run_backtest_same_close_fill_impossible():
    p = _make_panel()
    targets = pl.DataFrame({
        "formation_date": [dt.date(2024, 1, 2)],
        "symbol": ["A"],
        "weight": [1.0],
    })
    cost_fn = lambda notional: 0.0
    res = run_backtest(p, targets, nav0=100_000, slip_bp=0.0,
                       cost_frac_fn=cost_fn)
    assert res.trades.height > 0
    assert res.trades["exec_date"][0] == dt.date(2024, 1, 3)


def test_slippage_sweep_returns_all_levels():
    p = _make_panel()
    targets = pl.DataFrame({
        "formation_date": [dt.date(2024, 1, 2)],
        "symbol": ["A"],
        "weight": [1.0],
    })
    cost_fn = lambda notional: 0.008
    levels = (0.0, 50.0, 100.0)
    sw = slippage_sweep(p, targets, nav0=100_000, slip_levels=levels,
                        cost_frac_fn=cost_fn)
    assert set(sw.keys()) == {0.0, 50.0, 100.0}


def test_run_backtest_unknown_symbol_raises():
    p = _make_panel()
    targets = pl.DataFrame({
        "formation_date": [dt.date(2024, 1, 2)],
        "symbol": ["NOSUCH"],
        "weight": [1.0],
    })
    cost_fn = lambda notional: 0.0
    with pytest.raises(ValueError, match="not in panel"):
        run_backtest(p, targets, nav0=100_000, slip_bp=0.0,
                     cost_frac_fn=cost_fn)


def test_costs_reduce_nav():
    p = _make_panel()
    targets = pl.DataFrame({
        "formation_date": [dt.date(2024, 1, 2)],
        "symbol": ["A"],
        "weight": [1.0],
    })
    res_no_cost = run_backtest(p, targets, nav0=100_000, slip_bp=0.0,
                               cost_frac_fn=lambda n: 0.0)
    res_with_cost = run_backtest(p, targets, nav0=100_000, slip_bp=0.0,
                                 cost_frac_fn=lambda n: 0.008)
    final_no = res_no_cost.nav["nav"][-1]
    final_with = res_with_cost.nav["nav"][-1]
    assert final_with < final_no
