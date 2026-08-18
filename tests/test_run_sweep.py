import datetime as dt
from pathlib import Path

from fin_crypto_lab.run_sweep import write_verdict


def test_write_verdict_creates_file(tmp_path):
    rows = [
        {
            "name": "spot_mom_top10",
            "train_sharpe": 1.5,
            "test_sharpe": 1.2,
            "test_cagr": 0.15,
            "full_cagr": 0.18,
            "turnover": 8.0,
            "min_names": 10,
            "selected": True,
            "slip_finals": {0.0: 200_000, 50.0: 195_000},
        },
        {
            "name": "spot_mom_top20",
            "train_sharpe": 1.3,
            "test_sharpe": 1.0,
            "test_cagr": 0.10,
            "full_cagr": 0.12,
            "turnover": 6.0,
            "min_names": 20,
            "selected": False,
            "slip_finals": {0.0: 180_000, 50.0: 175_000},
        },
    ]
    checks = [
        ("PC-1", True, "1.20 vs benchmark 0.80"),
        ("PC-3", True, "DSR 0.950"),
        ("PC-4", True, "PBO 0.200"),
        ("KC-1", True, "max full CAGR 18.00%"),
    ]
    extra = {"selected": "spot_mom_top10", "dsr": 0.95, "pbo": 0.20,
             "instrument": "spot"}
    out = write_verdict(rows, checks, family_pass=True, extra=extra,
                        run_label="test_run", results_dir=tmp_path)
    verdict_file = out / "verdict.md"
    assert verdict_file.exists()
    text = verdict_file.read_text()
    assert "FAMILY: PASS" in text
    assert "spot_mom_top10" in text
    assert "PC-1" in text


def test_write_verdict_fail(tmp_path):
    rows = [
        {
            "name": "futures_mom_top10",
            "train_sharpe": 0.5,
            "test_sharpe": 0.3,
            "test_cagr": -0.05,
            "full_cagr": -0.02,
            "turnover": 40.0,
            "min_names": 8,
            "selected": True,
            "slip_finals": {0.0: 90_000},
        },
    ]
    checks = [
        ("PC-1", False, "0.30 vs benchmark 0.50"),
    ]
    extra = {"selected": "futures_mom_top10", "dsr": 0.70, "pbo": 0.60,
             "instrument": "futures"}
    out = write_verdict(rows, checks, family_pass=False, extra=extra,
                        run_label="test_fail", results_dir=tmp_path)
    text = (out / "verdict.md").read_text()
    assert "FAMILY: FAIL" in text
