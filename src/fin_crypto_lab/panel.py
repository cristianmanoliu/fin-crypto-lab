"""Crypto panel: aligned [T sessions x N symbols] numpy matrices.
24/7 calendar — every calendar day is a session."""
import datetime as dt
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import polars as pl

from fin_crypto_lab import config, store


@dataclass
class Panel:
    sessions: pl.Series
    symbols: list[str]
    open: np.ndarray
    high: np.ndarray
    low: np.ndarray
    close: np.ndarray
    close_ff: np.ndarray
    volume: np.ndarray
    vwap: np.ndarray
    tradable: np.ndarray

    def session_index(self, date: dt.date) -> int:
        idx = self.sessions.search_sorted(date)
        if idx >= len(self.sessions) or self.sessions[int(idx)] != date:
            raise KeyError(f"{date} is not a session in this panel")
        return int(idx)


def crypto_sessions(start: str, end: str) -> pl.Series:
    """Every calendar day from start to end inclusive."""
    return pl.date_range(
        dt.date.fromisoformat(start),
        dt.date.fromisoformat(end),
        eager=True,
    )


def weekly_formations(sessions: pl.Series) -> list[dt.date]:
    """Every Sunday in the sessions range."""
    return [d for d in sessions.to_list() if d.weekday() == 6]


def build_panel(
    symbols: list[str], sessions: pl.Series,
    data_dir: Path = config.SPOT_DATA_DIR,
    manifest: pl.DataFrame | None = None,
) -> Panel:
    t, n = len(sessions), len(symbols)
    grid = pl.DataFrame({"date": sessions})
    mats = {
        "open": np.full((t, n), np.nan),
        "high": np.full((t, n), np.nan),
        "low": np.full((t, n), np.nan),
        "close": np.full((t, n), np.nan),
        "volume": np.full((t, n), np.nan),
        "vwap": np.full((t, n), np.nan),
    }
    for j, sym in enumerate(symbols):
        df = store.read_ohlcv(sym, data_dir=data_dir, manifest=manifest)
        aligned = grid.join(df, on="date", how="left")
        for col in ("open", "high", "low", "close", "volume", "vwap"):
            mats[col][:, j] = aligned[col].cast(pl.Float64).to_numpy()

    close_ff = _ffill_after_first(mats["close"])
    tradable = (~np.isnan(mats["open"])) & (mats["volume"] > 0)
    return Panel(
        sessions=sessions, symbols=list(symbols),
        open=mats["open"], high=mats["high"], low=mats["low"],
        close=mats["close"], close_ff=close_ff,
        volume=mats["volume"], vwap=mats["vwap"],
        tradable=tradable,
    )


def _ffill_after_first(a: np.ndarray) -> np.ndarray:
    """Forward-fill each column, but only after its first non-NaN value."""
    out = a.copy()
    t = a.shape[0]
    idx = np.where(~np.isnan(a), np.arange(t)[:, None], -1).astype(np.intp)
    np.maximum.accumulate(idx, axis=0, out=idx)
    valid = idx >= 0
    cols = np.broadcast_to(np.arange(a.shape[1]), a.shape)
    out[valid] = a[idx[valid], cols[valid]]
    return out
