# Crypto futures volwt verdict (2026-09-19)

## FAMILY: FAIL

Selected: **futures_mom_top30** (DSR 0.619, PBO 0.675)

| check | result | measured |
|---|---|---|
| PC-1 | PASS | 0.19 vs benchmark 0.19 |
| PC-3 | FAIL | DSR 0.619 |
| PC-4 | FAIL | PBO 0.675 |
| PC-5 | PASS | drag 0.48% vs costs 0.77% (err 37%) |
| KC-1 | PASS | max full CAGR -14.61% |
| KC-2 | PASS | max turnover 17.05 |
| KC-3 | PASS | True |
| KC-4 | PASS | test maxDD 76.54% |
| KC-5 | PASS | min Σw 1.0000, max 1.0000 |
| KC-6 | PASS | min names 14 |

## Grid

| config | train Sharpe | test Sharpe | test CAGR | full CAGR | turnover | min names |
|---|---|---|---|---|---|---|
| **futures_mom_top30** **selected** | 0.12 | 0.19 | -16.29% | -14.61% | 5.43 | 14 |
| futures_mom_top20 | 0.05 | 0.19 | -17.28% | -17.05% | 11.97 | 14 |
| futures_mom_top10 | -0.05 | 0.25 | -18.15% | -21.50% | 17.05 | 10 |
