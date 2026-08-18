"""Thin wrapper around Kraken REST public API. Rate limit: 1 req/sec."""
import logging
from dataclasses import dataclass

import httpx

log = logging.getLogger("fin_crypto_lab.kraken")

BASE_URL = "https://api.kraken.com"
RATE_LIMIT_S = 1.1


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
        fees = info.get("fees", [[0, 0.26]])
        fees_maker = info.get("fees_maker", [[0, 0.16]])
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
    resp = httpx.get(f"{BASE_URL}/0/public/AssetPairs", timeout=30)
    resp.raise_for_status()
    data = resp.json()
    if data.get("error"):
        raise KrakenError(str(data["error"]))
    return _parse_asset_pairs(data["result"])


def get_trades(
    pair_kraken_name: str, since: int | None = None,
) -> tuple[list[Trade], int]:
    """Fetch trades for a pair. `since` is a nanosecond timestamp.
    Returns (trades, last_id) for pagination."""
    params: dict = {"pair": pair_kraken_name}
    if since is not None:
        params["since"] = str(since)
    resp = httpx.get(f"{BASE_URL}/0/public/Trades",
                     params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    if data.get("error"):
        raise KrakenError(str(data["error"]))
    result = data["result"]
    last = int(result.get("last", 0))
    trade_data = [v for k, v in result.items() if k != "last"][0]
    return _parse_trades(trade_data), last
