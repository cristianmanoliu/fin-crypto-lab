import datetime as dt
from unittest.mock import patch

import polars as pl
import pytest

from fin_crypto_lab.download import EPOCH_2017_NS, download_pair, plan_downloads
from fin_crypto_lab.store import MANIFEST_SCHEMA, read_ohlcv, write_ohlcv


def test_plan_downloads_fresh_store(tmp_path):
    pairs = {
        "XBTUSD": {"kraken_name": "XXBTZUSD"},
        "ETHUSD": {"kraken_name": "XETHZUSD"},
    }
    with patch("fin_crypto_lab.download.get_asset_pairs", return_value=pairs):
        plans = plan_downloads(tmp_path)
    assert len(plans) == 2
    assert all(p["since"] == EPOCH_2017_NS for p in plans)


def test_plan_downloads_incremental(tmp_path):
    manifest = pl.DataFrame({
        "pair": ["XBTUSD"],
        "first_date": [dt.date(2024, 1, 1)],
        "last_date": [dt.date(2024, 1, 10)],
        "rows": [10],
        "last_trade_id": [99999],
        "trade_count": [50000],
        "downloaded_at": [dt.datetime(2024, 1, 11)],
    }, schema=MANIFEST_SCHEMA)
    path = tmp_path / "manifest.parquet"
    path.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_parquet(path)

    pairs = {
        "XBTUSD": {"kraken_name": "XXBTZUSD"},
        "ETHUSD": {"kraken_name": "XETHZUSD"},
    }
    with patch("fin_crypto_lab.download.get_asset_pairs", return_value=pairs):
        plans = plan_downloads(tmp_path)
    xbt = [p for p in plans if p["pair"] == "XBTUSD"][0]
    eth = [p for p in plans if p["pair"] == "ETHUSD"][0]
    assert xbt["since"] == 99999
    assert eth["since"] == EPOCH_2017_NS


def test_download_pair_merges_on_resume(tmp_path):
    """Incremental resume must merge with existing data, not overwrite."""
    old_df = pl.DataFrame({
        "date": [dt.date(2024, 1, 1), dt.date(2024, 1, 2)],
        "open": [100.0, 101.0], "high": [105.0, 106.0],
        "low": [95.0, 96.0], "close": [103.0, 104.0],
        "volume": [10.0, 20.0], "trade_count": [100, 200],
        "vwap": [101.0, 102.0],
    })
    write_ohlcv(old_df, "XBTUSD", last_trade_id=50000, trade_count=300,
                data_dir=tmp_path)

    from fin_crypto_lab.kraken_client import Trade
    new_trades = [
        Trade(price=110.0, volume=5.0, timestamp=1704326400.0,
              side="b", order_type="m", trade_id=0),  # 2024-01-04
    ]
    with patch("fin_crypto_lab.download.get_trades", return_value=([], 60000)):
        download_pair("XBTUSD", "XXBTZUSD", since=50000, data_dir=tmp_path,
                      existing_trades=new_trades)

    got = read_ohlcv("XBTUSD", data_dir=tmp_path)
    assert got.height == 3  # old 2 days + new 1 day = 3, not just 1
    assert got["date"].to_list() == [
        dt.date(2024, 1, 1), dt.date(2024, 1, 2), dt.date(2024, 1, 4),
    ]
