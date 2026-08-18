import datetime as dt

import numpy as np
import polars as pl
import pytest

from fin_crypto_lab.panel import Panel
from fin_crypto_lab.signals import momentum


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
