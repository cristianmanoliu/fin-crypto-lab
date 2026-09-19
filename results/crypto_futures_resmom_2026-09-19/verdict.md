# Crypto futures resmom verdict (2026-09-19)

## FAMILY: FAIL

Selected: **futures_mom_top10** (DSR 0.362, PBO 0.068)

| check | result | measured |
|---|---|---|
| PC-1 | FAIL | -0.28 vs benchmark 0.19 |
| PC-3 | FAIL | DSR 0.362 |
| PC-4 | PASS | PBO 0.068 |
| PC-5 | PASS | drag 4.24% vs costs 6.97% (err 39%) |
| KC-1 | PASS | max full CAGR -14.61% |
| KC-2 | FAIL | max turnover 54.72 |
| KC-3 | PASS | True |
| KC-4 | FAIL | test maxDD 88.04% |
| KC-5 | PASS | min Σw 1.0000, max 1.0000 |
| KC-6 | PASS | min names 10 |

## Grid

| config | train Sharpe | test Sharpe | test CAGR | full CAGR | turnover | min names |
|---|---|---|---|---|---|---|
| **futures_mom_top10** **selected** | 0.17 | -0.28 | -45.15% | -30.87% | 54.72 | 10 |
| futures_mom_top20 | 0.15 | -0.13 | -34.57% | -23.72% | 28.76 | 14 |
| futures_mom_top30 | 0.12 | 0.19 | -16.29% | -14.61% | 5.43 | 14 |
