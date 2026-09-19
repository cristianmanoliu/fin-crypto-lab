"""Cross-sectional momentum signals for crypto. Point-in-time:
only panel indices <= f_idx are ever read."""
import numpy as np

from fin_crypto_lab.panel import Panel


def momentum(panel: Panel, f_idx: int, lookback: int = 365,
             skip: int = 7) -> np.ndarray:
    """Raw price momentum: close_ff[f-skip] / close_ff[f-lookback] - 1."""
    if f_idx < lookback:
        raise ValueError(f"f_idx {f_idx} < lookback {lookback}")
    then = panel.close_ff[f_idx - lookback, :]
    recent = panel.close_ff[f_idx - skip, :]
    with np.errstate(invalid="ignore", divide="ignore"):
        return recent / then - 1.0


def residual_momentum(panel: Panel, f_idx: int, lookback: int = 365,
                      skip: int = 7, market_col: int | None = None
                      ) -> np.ndarray:
    """Momentum after stripping market (BTC) beta via OLS.
    market_col: column index of the market proxy (e.g. XBTUSD or BTCUSD).
    If None, uses equal-weight average of all columns as market."""
    if f_idx < lookback:
        raise ValueError(f"f_idx {f_idx} < lookback {lookback}")
    start = f_idx - lookback
    end = f_idx - skip
    closes = panel.close_ff[start:end + 1, :]
    with np.errstate(invalid="ignore", divide="ignore"):
        rets = closes[1:] / closes[:-1] - 1.0

    if market_col is not None:
        mkt = rets[:, market_col].copy()
    else:
        mkt = np.nanmean(rets, axis=1)

    valid_mkt = np.isfinite(mkt)
    n = rets.shape[1]
    out = np.full(n, np.nan)
    for j in range(n):
        col = rets[:, j]
        mask = valid_mkt & np.isfinite(col)
        if mask.sum() < 20:
            continue
        y, x = col[mask], mkt[mask]
        x_dm = x - x.mean()
        beta = np.dot(x_dm, y) / np.dot(x_dm, x_dm) if np.dot(x_dm, x_dm) > 1e-15 else 0.0
        resid = y - (y.mean() - beta * x.mean()) - beta * x
        # ponytail: cumulative residual return as signal; OLS is the minimum viable approach
        out[j] = float(np.sum(resid))
    return out
