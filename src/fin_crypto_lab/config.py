"""Crypto momentum research config. All constants pre-registered;
verdict runs must not override them ad hoc."""
import datetime as dt
from pathlib import Path

DATA_DIR = Path("data")
SPOT_DATA_DIR = DATA_DIR / "spot"
FUTURES_DATA_DIR = DATA_DIR / "futures"
RESULTS_DIR = Path("results")

NAV_DEFAULT = 100_000.0

# Kraken tier 1 fees (per side, basis points)
SPOT_TAKER_BP = 80.0
FUTURES_TAKER_BP = 5.0

# Slippage sweep levels
SPOT_SLIP_LEVELS_BP = (0.0, 50.0, 100.0, 160.0)
FUTURES_SLIP_LEVELS_BP = (0.0, 5.0, 10.0, 20.0)

# Decision-level slip (round-trip taker)
SPOT_DECISION_SLIP_BP = 160.0
FUTURES_DECISION_SLIP_BP = 10.0

# Train/test split (spot: 2017-2022 train, 2022-2026 test)
TRAIN_END = dt.date(2022, 6, 30)
FORM_START = dt.date(2017, 1, 1)
FORM_END = dt.date(2026, 4, 30)

# Futures split (perps launched 2022-03; shorter history)
FUTURES_FORM_START = dt.date(2022, 3, 27)
FUTURES_TRAIN_END = dt.date(2024, 6, 30)
FUTURES_FORM_END = dt.date(2026, 9, 14)


def spot_cost_frac(notional: float) -> float:
    """Spot taker cost as a fraction of trade notional (per side)."""
    return SPOT_TAKER_BP / 1e4


def futures_cost_frac(notional: float) -> float:
    """Futures taker cost as a fraction of trade notional (per side)."""
    return FUTURES_TAKER_BP / 1e4
