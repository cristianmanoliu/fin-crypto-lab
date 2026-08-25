# Crypto futures momentum verdict (2026-08-24)

## FAMILY: FAIL

Selected: **futures_mom_top10** (DSR 0.128, PBO 0.500)

| check | result | measured |
|---|---|---|
| PC-1 | FAIL | -0.41 vs benchmark 0.02 |
| PC-3 | FAIL | DSR 0.128 |
| PC-4 | PASS | PBO 0.500 |
| PC-5 | PASS | drag 0.08% vs costs 0.10% (err 19%) |
| KC-1 | PASS | max full CAGR -3.51% |
| KC-2 | PASS | max turnover 0.83 |
| KC-3 | PASS | True |
| KC-4 | PASS | test maxDD 41.19% |
| KC-5 | PASS | min Σw 1.0000, max 1.0000 |
| KC-6 | PASS | min names 10 |

## Grid

| config | train Sharpe | test Sharpe | test CAGR | full CAGR | turnover | min names |
|---|---|---|---|---|---|---|
| **futures_mom_top10** **selected** | nan | -0.41 | -8.33% | -3.51% | 0.83 | 10 |
| futures_mom_top20 | nan | -0.70 | -12.25% | -5.23% | 0.62 | 20 |
| futures_mom_top30 | nan | -0.73 | -12.85% | -5.50% | 0.47 | 21 |
