import datetime as dt

import numpy as np
import polars as pl
import pytest

from fin_crypto_lab.sweep import (
    GRID,
    THRESHOLDS,
    benchmark_targets,
    config_name,
    period_returns,
    topn_targets,
    weekly_cagr,
    weekly_sharpe,
)


def test_grid_has_six_configs():
    assert len(GRID) == 6
    names = [config_name(g) for g in GRID]
    assert len(set(names)) == 6


def test_grid_instruments():
    instruments = {g["instrument"] for g in GRID}
    assert instruments == {"spot", "futures"}


def test_config_name_format():
    g = {"instrument": "spot", "top_n": 20, "lookback": 365, "skip": 7}
    assert config_name(g) == "spot_mom_top20"


def test_n_trials_matches_locked_ledger():
    # results/crypto_spot_momentum_deep_decision_rule_2026-09-23.md
    assert THRESHOLDS["N_TRIALS"] == 69


def test_thresholds_present():
    for key in ("DSR_MIN", "PBO_MAX", "COST_RECON_TOL", "KC1_MAX_CAGR",
                "KC2_MAX_TURNOVER", "KC4_MAX_DD", "KC5_WEIGHT_TOL",
                "KC6_MIN_NAMES", "S_BLOCKS", "N_TRIALS"):
        assert key in THRESHOLDS


def _universe():
    return pl.DataFrame({
        "snapshot_date": [dt.date(2024, 1, 7)] * 3,
        "symbol": ["A", "B", "C"],
        "rank": [1, 2, 3],
        "avg_daily_volume": [100.0, 80.0, 60.0],
    }, schema={
        "snapshot_date": pl.Date, "symbol": pl.Utf8,
        "rank": pl.UInt32, "avg_daily_volume": pl.Float64,
    })


def test_topn_targets_selects_top_n():
    univ = _universe()
    sig = {dt.date(2024, 1, 7): {"A": 0.5, "B": 0.3, "C": 0.1}}
    tgt = topn_targets(sig, univ, n=2)
    assert tgt.height == 2
    assert set(tgt["symbol"].to_list()) == {"A", "B"}
    assert abs(tgt["weight"].sum() - 1.0) < 1e-10


def test_topn_targets_falls_back_to_latest_snap():
    univ = _universe()
    sig = {dt.date(2024, 1, 14): {"A": 0.5, "B": 0.3, "C": 0.1}}
    tgt = topn_targets(sig, univ, n=2)
    assert tgt.height == 2


def test_topn_targets_skips_thin_formations():
    univ = _universe()
    sig = {dt.date(2024, 1, 7): {"A": 0.5, "B": 0.3, "C": 0.1}}
    tgt = topn_targets(sig, univ, n=10, min_names=5)
    assert tgt.height == 0


def test_topn_targets_empty_on_no_signal():
    univ = _universe()
    tgt = topn_targets({}, univ, n=2)
    assert tgt.height == 0


def test_benchmark_targets_equal_weight():
    univ = _universe()
    formations = [dt.date(2024, 1, 7)]
    bm = benchmark_targets(univ, formations)
    assert bm.height == 3
    assert abs(bm["weight"].sum() - 1.0) < 1e-10


def test_period_returns_basic():
    nav = pl.DataFrame({
        "date": [dt.date(2024, 1, 7), dt.date(2024, 1, 14),
                 dt.date(2024, 1, 21)],
        "nav": [100.0, 110.0, 105.0],
    })
    formations = [dt.date(2024, 1, 7), dt.date(2024, 1, 14),
                  dt.date(2024, 1, 21)]
    rets = period_returns(nav, formations)
    assert len(rets) == 2
    assert abs(rets[0] - 0.1) < 1e-10
    assert abs(rets[1] - (105 / 110 - 1)) < 1e-10


def test_weekly_sharpe_annualizes():
    rng = np.random.default_rng(42)
    rets = (0.002 + rng.normal(0, 0.02, 52)).tolist()
    sr = weekly_sharpe(rets)
    assert np.isfinite(sr)


def test_weekly_sharpe_zero_vol():
    sr = weekly_sharpe([0.0, 0.0, 0.0])
    assert np.isnan(sr)


def test_weekly_cagr_basic():
    rets = [0.01] * 52
    cagr = weekly_cagr(rets)
    assert abs(cagr - ((1.01 ** 52) ** (52 / 52) - 1)) < 0.01


def test_weekly_cagr_empty():
    assert np.isnan(weekly_cagr([]))
