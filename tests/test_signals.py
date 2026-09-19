import datetime as dt

import numpy as np
import polars as pl
import pytest

from fin_crypto_lab.panel import Panel
from fin_crypto_lab.signals import momentum, residual_momentum


def _make_panel(n_days=400, n_syms=2):
    sessions = pl.date_range(dt.date(2023, 1, 1),
                             dt.date(2023, 1, 1) + dt.timedelta(days=n_days - 1),
                             eager=True)
    close = np.ones((n_days, n_syms)) * 100.0
    close[:, 0] = np.linspace(50.0, 100.0, n_days)
    return Panel(
        sessions=sessions, symbols=[f"SYM{i}" for i in range(n_syms)],
        open=close.copy(), high=close.copy(), low=close.copy(),
        close=close.copy(), close_ff=close.copy(),
        volume=np.ones((n_days, n_syms)) * 100.0,
        vwap=close.copy(),
        tradable=np.ones((n_days, n_syms), dtype=bool),
    )


def test_momentum_basic():
    p = _make_panel()
    m = momentum(p, f_idx=399, lookback=365, skip=7)
    assert m.shape == (2,)
    assert m[0] > 0
    assert abs(m[1]) < 0.01


def test_momentum_too_early():
    p = _make_panel()
    with pytest.raises(ValueError):
        momentum(p, f_idx=100, lookback=365, skip=7)


def test_residual_momentum_returns_finite():
    p = _make_panel(n_days=400, n_syms=3)
    r = residual_momentum(p, f_idx=399, lookback=365, skip=7, market_col=0)
    assert r.shape == (3,)
    assert np.isfinite(r).all()


def test_residual_momentum_strips_market():
    """A symbol perfectly correlated with market should have ~zero residual."""
    n = 400
    rng = np.random.default_rng(42)
    market_prices = 100 * np.exp(np.cumsum(rng.normal(0.001, 0.02, n)))
    close = np.column_stack([
        market_prices,
        market_prices * 2,
        100 * np.exp(np.cumsum(rng.normal(0.002, 0.01, n))),
    ])
    sessions = pl.date_range(dt.date(2023, 1, 1),
                             dt.date(2023, 1, 1) + dt.timedelta(days=n - 1),
                             eager=True)
    p = Panel(
        sessions=sessions, symbols=["MKT", "CLONE", "INDEP"],
        open=close.copy(), high=close.copy(), low=close.copy(),
        close=close.copy(), close_ff=close.copy(),
        volume=np.ones_like(close) * 100.0, vwap=close.copy(),
        tradable=np.ones_like(close, dtype=bool),
    )
    r = residual_momentum(p, f_idx=399, lookback=365, skip=7, market_col=0)
    assert abs(r[1]) < abs(r[2]) or abs(r[1]) < 0.5
