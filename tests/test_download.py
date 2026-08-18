import datetime as dt
from unittest.mock import patch

import polars as pl
import pytest

from fin_crypto_lab.download import plan_downloads
from fin_crypto_lab.store import MANIFEST_SCHEMA


def test_plan_downloads_fresh_store(tmp_path):
    pairs = {
        "XBTUSD": {"kraken_name": "XXBTZUSD"},
        "ETHUSD": {"kraken_name": "XETHZUSD"},
    }
    with patch("fin_crypto_lab.download.get_asset_pairs", return_value=pairs):
        plans = plan_downloads(tmp_path)
    assert len(plans) == 2
    assert all(p["since"] is None for p in plans)


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
    assert eth["since"] is None
