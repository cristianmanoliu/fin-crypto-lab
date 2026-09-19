"""Cross-sectional momentum signals for crypto. Point-in-time:
only panel indices <= f_idx are ever read."""
import numpy as np

from fin_crypto_lab.panel import Panel


def _daily_rets(panel: Panel, start: int, end: int) -> np.ndarray:
    closes = panel.close_ff[start:end + 1, :]
    with np.errstate(invalid="ignore", divide="ignore"):
        return closes[1:] / closes[:-1] - 1.0


def _check_lookback(f_idx: int, lookback: int) -> None:
    if f_idx < lookback:
        raise ValueError(f"f_idx {f_idx} < lookback {lookback}")


# --- 1. Raw momentum (existing) ---

def momentum(panel: Panel, f_idx: int, lookback: int = 365,
             skip: int = 7) -> np.ndarray:
    """close[f-skip] / close[f-lookback] - 1."""
    _check_lookback(f_idx, lookback)
    then = panel.close_ff[f_idx - lookback, :]
    recent = panel.close_ff[f_idx - skip, :]
    with np.errstate(invalid="ignore", divide="ignore"):
        return recent / then - 1.0


# --- 2. Residual momentum (existing) ---

def residual_momentum(panel: Panel, f_idx: int, lookback: int = 365,
                      skip: int = 7, market_col: int | None = None
                      ) -> np.ndarray:
    _check_lookback(f_idx, lookback)
    start = f_idx - lookback
    end = f_idx - skip
    rets = _daily_rets(panel, start, end)

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
        out[j] = float(np.sum(resid))
    return out


# --- 3. Volume-weighted momentum ---

def volume_weighted_momentum(panel: Panel, f_idx: int, lookback: int = 365,
                             skip: int = 7) -> np.ndarray:
    _check_lookback(f_idx, lookback)
    start = f_idx - lookback
    end = f_idx - skip
    rets = _daily_rets(panel, start, end)
    day_vols = panel.volume[start + 1:end + 1, :]
    n = rets.shape[1]
    out = np.full(n, np.nan)
    for j in range(n):
        r, v = rets[:, j], day_vols[:, j]
        mask = np.isfinite(r) & np.isfinite(v) & (v > 0)
        if mask.sum() < 20:
            continue
        w = v[mask] / v[mask].sum()
        out[j] = float(np.dot(w, r[mask])) * mask.sum()
    return out


# --- 4. 52-week high proximity (George & Hwang 2004) ---

def high_proximity(panel: Panel, f_idx: int, lookback: int = 365,
                   skip: int = 7) -> np.ndarray:
    """close[f-skip] / max(high[f-lookback:f-skip]). Closer to high = stronger."""
    _check_lookback(f_idx, lookback)
    start = f_idx - lookback
    end = f_idx - skip
    highs = panel.high[start:end + 1, :]
    current = panel.close_ff[end, :]
    with np.errstate(invalid="ignore", divide="ignore"):
        peak = np.nanmax(highs, axis=0)
        return current / peak


# --- 5. Short-term reversal (contrarian, 1-4 week return inverted) ---

def short_term_reversal(panel: Panel, f_idx: int, lookback: int = 365,
                        skip: int = 7) -> np.ndarray:
    """Negative of 28-day return. Buys recent losers."""
    _check_lookback(f_idx, 28)
    recent = panel.close_ff[f_idx - skip, :]
    month_ago = panel.close_ff[f_idx - 28, :]
    with np.errstate(invalid="ignore", divide="ignore"):
        return -(recent / month_ago - 1.0)


# --- 6. Volatility-adjusted momentum (momentum / realized vol) ---

def vol_adjusted_momentum(panel: Panel, f_idx: int, lookback: int = 365,
                          skip: int = 7) -> np.ndarray:
    """Momentum divided by realized volatility. Penalizes noisy movers."""
    _check_lookback(f_idx, lookback)
    mom = momentum(panel, f_idx, lookback, skip)
    start = f_idx - lookback
    end = f_idx - skip
    rets = _daily_rets(panel, start, end)
    n = rets.shape[1]
    out = np.full(n, np.nan)
    for j in range(n):
        col = rets[:, j]
        valid = np.isfinite(col)
        if valid.sum() < 20 or not np.isfinite(mom[j]):
            continue
        vol = np.std(col[valid], ddof=1)
        if vol > 1e-15:
            out[j] = mom[j] / vol
    return out


# --- 7. Acceleration (recent momentum minus older momentum) ---

def acceleration(panel: Panel, f_idx: int, lookback: int = 365,
                 skip: int = 7) -> np.ndarray:
    """Difference between recent-half and older-half momentum.
    Positive = momentum is increasing."""
    _check_lookback(f_idx, lookback)
    half = lookback // 2
    recent_start = f_idx - half
    recent = panel.close_ff[f_idx - skip, :]
    mid = panel.close_ff[recent_start, :]
    old = panel.close_ff[f_idx - lookback, :]
    with np.errstate(invalid="ignore", divide="ignore"):
        recent_mom = recent / mid - 1.0
        old_mom = mid / old - 1.0
        return recent_mom - old_mom


# --- 8. Low volatility (inverse realized vol, buys calm coins) ---

def low_volatility(panel: Panel, f_idx: int, lookback: int = 365,
                   skip: int = 7) -> np.ndarray:
    """Negative realized vol. Ranks calm coins highest."""
    _check_lookback(f_idx, lookback)
    start = f_idx - lookback
    end = f_idx - skip
    rets = _daily_rets(panel, start, end)
    n = rets.shape[1]
    out = np.full(n, np.nan)
    for j in range(n):
        col = rets[:, j]
        valid = np.isfinite(col)
        if valid.sum() < 20:
            continue
        out[j] = -np.std(col[valid], ddof=1)
    return out


# --- 9. Volume trend (rising volume = bullish attention) ---

def volume_trend(panel: Panel, f_idx: int, lookback: int = 365,
                 skip: int = 7) -> np.ndarray:
    """Ratio of recent 30-day avg volume to trailing lookback avg volume.
    Rising volume = momentum confirmation."""
    _check_lookback(f_idx, lookback)
    start = f_idx - lookback
    end = f_idx - skip
    vols = panel.volume[start:end + 1, :]
    recent_vols = panel.volume[max(start, end - 30):end + 1, :]
    with np.errstate(invalid="ignore", divide="ignore"):
        long_avg = np.nanmean(vols, axis=0)
        short_avg = np.nanmean(recent_vols, axis=0)
        return short_avg / long_avg


# --- 10. Mean reversion (distance from trailing mean, buy dips) ---

def mean_reversion(panel: Panel, f_idx: int, lookback: int = 365,
                   skip: int = 7) -> np.ndarray:
    """Negative z-score: (mean - current) / std. Buys below-average coins."""
    _check_lookback(f_idx, lookback)
    start = f_idx - lookback
    end = f_idx - skip
    closes = panel.close_ff[start:end + 1, :]
    current = panel.close_ff[end, :]
    n = closes.shape[1]
    out = np.full(n, np.nan)
    for j in range(n):
        col = closes[:, j]
        valid = np.isfinite(col)
        if valid.sum() < 20:
            continue
        mu = np.mean(col[valid])
        sd = np.std(col[valid], ddof=1)
        if sd > 1e-15 and np.isfinite(current[j]):
            out[j] = (mu - current[j]) / sd
    return out
