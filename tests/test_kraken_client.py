from fin_crypto_lab.kraken_client import (
    KrakenError,
    _parse_asset_pairs,
    _parse_trades,
)


def test_parse_asset_pairs_filters_usd():
    raw = {
        "XXBTZUSD": {
            "altname": "XBTUSD", "base": "XXBT", "quote": "ZUSD",
            "fees": [[0, 0.26], [50000, 0.24]],
            "fees_maker": [[0, 0.16], [50000, 0.14]],
            "ordermin": "0.0001",
        },
        "XXBTZEUR": {
            "altname": "XBTEUR", "base": "XXBT", "quote": "ZEUR",
            "fees": [[0, 0.26]], "fees_maker": [[0, 0.16]],
            "ordermin": "0.0001",
        },
        "XETHZUSD": {
            "altname": "ETHUSD", "base": "XETH", "quote": "ZUSD",
            "fees": [[0, 0.26]], "fees_maker": [[0, 0.16]],
            "ordermin": "0.01",
        },
    }
    result = _parse_asset_pairs(raw)
    assert "XBTUSD" in result
    assert "ETHUSD" in result
    assert "XBTEUR" not in result
    assert result["XBTUSD"]["taker_fee_pct"] == 0.26


def test_parse_trades():
    raw = [
        ["42000.0", "0.5", 1700000000.0, "b", "m", "", 1],
        ["42100.0", "0.3", 1700000001.0, "s", "l", "", 2],
    ]
    trades = _parse_trades(raw)
    assert len(trades) == 2
    assert trades[0].price == 42000.0
    assert trades[0].volume == 0.5
    assert trades[1].trade_id == 2


def test_parse_trades_empty():
    assert _parse_trades([]) == []
