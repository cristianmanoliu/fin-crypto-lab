"""Thin wrapper around Kraken REST public API. Rate limit: 1 req/sec."""
import logging
import time
from dataclasses import dataclass

import httpx

log = logging.getLogger("fin_crypto_lab.kraken")

BASE_URL = "https://api.kraken.com"
FUTURES_BASE_URL = "https://futures.kraken.com"
RATE_LIMIT_S = 1.1
_MAX_RETRIES = 12  # ~70 min total: outlasts an overnight WiFi drop (2026-09-24, 9 min was not enough)
_RETRY_BACKOFF = (10, 30, 60, 120, 300, 600)


def _get_with_retry(url: str, **kwargs) -> httpx.Response:
    """GET with exponential backoff on transient network errors."""
    for attempt in range(_MAX_RETRIES):
        try:
            resp = httpx.get(url, **kwargs)
            resp.raise_for_status()
            return resp
        except httpx.TransportError as exc:  # covers RemoteProtocolError too, which killed XRPUSD 2026-09-23
            wait = _RETRY_BACKOFF[min(attempt, len(_RETRY_BACKOFF) - 1)]
            log.warning("retry %d/%d in %ds: %s", attempt + 1, _MAX_RETRIES, wait, exc)
            time.sleep(wait)
    return httpx.get(url, **kwargs)  # final attempt, let it raise


class KrakenError(Exception):
    pass


@dataclass
class Trade:
    price: float
    volume: float
    timestamp: float
    side: str
    order_type: str
    trade_id: int


def _parse_asset_pairs(raw: dict) -> dict[str, dict]:
    """Filter to USD-quoted pairs, return {altname: metadata}."""
    out = {}
    for key, info in raw.items():
        quote = info.get("quote", "")
        if quote not in ("ZUSD", "USD"):
            continue
        altname = info["altname"]
        fees = info.get("fees") or [[0, 0.26]]
        fees_maker = info.get("fees_maker") or [[0, 0.16]]
        out[altname] = {
            "kraken_name": key,
            "base": info.get("base", ""),
            "taker_fee_pct": fees[0][1],
            "maker_fee_pct": fees_maker[0][1],
            "ordermin": info.get("ordermin", "0"),
        }
    return out


def _parse_trades(raw: list) -> list[Trade]:
    return [
        Trade(
            price=float(t[0]),
            volume=float(t[1]),
            timestamp=float(t[2]),
            side=t[3],
            order_type=t[4],
            trade_id=int(t[6]) if len(t) > 6 else 0,
        )
        for t in raw
    ]


def get_asset_pairs() -> dict[str, dict]:
    """Fetch all USD-quoted asset pairs from Kraken."""
    resp = _get_with_retry(f"{BASE_URL}/0/public/AssetPairs", timeout=30)
    data = resp.json()
    if data.get("error"):
        raise KrakenError(str(data["error"]))
    return _parse_asset_pairs(data["result"])


def get_ohlc(
    pair_kraken_name: str, interval: int = 1440, since: int | None = None,
) -> list[dict]:
    """Fetch OHLC candles. interval=1440 = daily. Returns list of dicts
    with keys: date, open, high, low, close, volume, vwap, trade_count."""
    import datetime as _dt
    params: dict = {"pair": pair_kraken_name, "interval": interval}
    if since is not None:
        params["since"] = str(since)
    resp = _get_with_retry(f"{BASE_URL}/0/public/OHLC",
                           params=params, timeout=30)
    data = resp.json()
    if data.get("error"):
        raise KrakenError(str(data["error"]))
    result = data["result"]
    candles = [v for k, v in result.items() if k != "last"][0]
    rows = []
    for c in candles:
        ts, o, h, lo, cl, vwap, vol, count = c
        rows.append({
            "date": _dt.date.fromtimestamp(int(ts)),
            "open": float(o), "high": float(h), "low": float(lo),
            "close": float(cl), "volume": float(vol), "vwap": float(vwap),
            "trade_count": int(count),
        })
    return rows


def get_trades(
    pair_kraken_name: str, since: int | None = None,
) -> tuple[list[Trade], int]:
    """Fetch trades for a pair. `since` is a nanosecond timestamp.
    Returns (trades, last_id) for pagination."""
    params: dict = {"pair": pair_kraken_name}
    if since is not None:
        params["since"] = str(since)
    resp = _get_with_retry(f"{BASE_URL}/0/public/Trades",
                           params=params, timeout=30)
    data = resp.json()
    if data.get("error"):
        raise KrakenError(str(data["error"]))
    result = data["result"]
    last = int(result.get("last", 0))
    trade_data = [v for k, v in result.items() if k != "last"][0]
    return _parse_trades(trade_data), last


# --- Futures API (futures.kraken.com) ---


def get_futures_instruments() -> dict[str, dict]:
    """Fetch all USD-quoted perpetual futures instruments.
    Returns {altname: {symbol, base, quote, openingDate, ...}}."""
    resp = _get_with_retry(
        f"{FUTURES_BASE_URL}/derivatives/api/v3/instruments", timeout=30)
    data = resp.json()
    if data.get("result") != "success":
        raise KrakenError(str(data))
    out = {}
    for inst in data["instruments"]:
        sym = inst["symbol"]
        if not sym.startswith("PF_") or inst.get("quote") != "USD":
            continue
        if not inst.get("tradeable", False):
            continue
        base = inst.get("base", "")
        altname = f"{base}USD"
        out[altname] = {
            "futures_symbol": sym,
            "base": base,
            "quote": "USD",
            "openingDate": inst.get("openingDate", ""),
        }
    return out


def get_futures_ohlc(futures_symbol: str) -> list[dict]:
    """Fetch full daily OHLCV history for a perpetual futures instrument.
    Returns list of dicts with keys: date, open, high, low, close, volume."""
    import datetime as _dt
    resp = _get_with_retry(
        f"{FUTURES_BASE_URL}/api/charts/v1/trade/{futures_symbol}/1d",
        timeout=30)
    data = resp.json()
    candles = data.get("candles", [])
    rows = []
    for c in candles:
        rows.append({
            "date": _dt.date.fromtimestamp(int(c["time"]) // 1000),
            "open": float(c["open"]),
            "high": float(c["high"]),
            "low": float(c["low"]),
            "close": float(c["close"]),
            "volume": float(c["volume"]),
            "vwap": float(c["close"]),
            "trade_count": 0,
        })
    return rows
