# Crypto futures highprox verdict (2026-09-19)

## FAMILY: FAIL

Selected: **futures_mom_top10** (DSR 0.684, PBO 0.245)

| check | result | measured |
|---|---|---|
| PC-1 | PASS | 0.21 vs benchmark 0.19 |
| PC-3 | FAIL | DSR 0.684 |
| PC-4 | PASS | PBO 0.245 |
| PC-5 | PASS | drag 2.01% vs costs 3.17% (err 36%) |
| KC-1 | PASS | max full CAGR -0.24% |
| KC-2 | PASS | max turnover 19.91 |
| KC-3 | PASS | True |
| KC-4 | PASS | test maxDD 69.22% |
| KC-5 | PASS | min Σw 1.0000, max 1.0000 |
| KC-6 | PASS | min names 10 |

## Grid

| config | train Sharpe | test Sharpe | test CAGR | full CAGR | turnover | min names |
|---|---|---|---|---|---|---|
| **futures_mom_top10** **selected** | 0.41 | 0.21 | -7.33% | -0.24% | 19.91 | 10 |
| futures_mom_top20 | 0.13 | 0.13 | -15.80% | -13.38% | 11.34 | 14 |
| futures_mom_top30 | 0.12 | 0.19 | -16.29% | -14.61% | 5.43 | 14 |
