import datetime as dt
from pathlib import Path

from fin_crypto_lab import config


def test_spot_data_dir_is_path():
    assert isinstance(config.SPOT_DATA_DIR, Path)


def test_futures_data_dir_is_path():
    assert isinstance(config.FUTURES_DATA_DIR, Path)


def test_spot_taker_bp():
    assert config.SPOT_TAKER_BP == 80.0


def test_futures_taker_bp():
    assert config.FUTURES_TAKER_BP == 5.0


def test_spot_slip_levels():
    assert config.SPOT_SLIP_LEVELS_BP == (0.0, 50.0, 100.0, 160.0)


def test_futures_slip_levels():
    assert config.FUTURES_SLIP_LEVELS_BP == (0.0, 5.0, 10.0, 20.0)


def test_spot_decision_slip():
    assert config.SPOT_DECISION_SLIP_BP == 160.0


def test_futures_decision_slip():
    assert config.FUTURES_DECISION_SLIP_BP == 10.0


def test_nav_default():
    assert config.NAV_DEFAULT == 100_000.0


def test_train_end():
    assert config.TRAIN_END == dt.date(2022, 6, 30)


def test_form_start():
    assert config.FORM_START == dt.date(2017, 1, 1)


def test_form_end():
    assert config.FORM_END == dt.date(2026, 4, 30)


def test_spot_cost_frac():
    assert config.spot_cost_frac(10_000.0) == 80.0 / 1e4


def test_futures_cost_frac():
    assert config.futures_cost_frac(10_000.0) == 5.0 / 1e4
