"""Cross-sectional momentum signal for crypto. Point-in-time:
only panel indices <= f_idx are ever read."""
import numpy as np

from fin_crypto_lab.panel import Panel


def momentum(panel: Panel, f_idx: int, lookback: int = 365,
             skip: int = 7) -> np.ndarray:
    """365-day lookback, 7-day skip.
    Returns close_ff[f-skip] / close_ff[f-lookback] - 1."""
    if f_idx < lookback:
        raise ValueError(f"f_idx {f_idx} < lookback {lookback}")
    then = panel.close_ff[f_idx - lookback, :]
    recent = panel.close_ff[f_idx - skip, :]
    with np.errstate(invalid="ignore", divide="ignore"):
        return recent / then - 1.0
