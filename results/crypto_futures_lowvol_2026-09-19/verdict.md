# Crypto futures lowvol verdict (2026-09-19)

## FAMILY: FAIL

Selected: **futures_mom_top30** (DSR 0.625, PBO 0.863)

| check | result | measured |
|---|---|---|
| PC-1 | PASS | 0.19 vs benchmark 0.19 |
| PC-3 | FAIL | DSR 0.625 |
| PC-4 | FAIL | PBO 0.863 |
| PC-5 | PASS | drag 0.48% vs costs 0.77% (err 37%) |
| KC-1 | PASS | max full CAGR -6.64% |
| KC-2 | PASS | max turnover 8.80 |
| KC-3 | PASS | True |
| KC-4 | PASS | test maxDD 76.54% |
| KC-5 | PASS | min Σw 1.0000, max 1.0000 |
| KC-6 | PASS | min names 14 |

## Grid

| config | train Sharpe | test Sharpe | test CAGR | full CAGR | turnover | min names |
|---|---|---|---|---|---|---|
| **futures_mom_top30** **selected** | 0.12 | 0.19 | -16.29% | -14.61% | 5.43 | 14 |
| futures_mom_top10 | 0.12 | 0.24 | -4.76% | -6.64% | 8.80 | 10 |
| futures_mom_top20 | -0.01 | 0.31 | -3.42% | -10.81% | 7.36 | 14 |
