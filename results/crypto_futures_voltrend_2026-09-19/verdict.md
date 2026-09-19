# Crypto futures voltrend verdict (2026-09-19)

## FAMILY: FAIL

Selected: **futures_mom_top30** (DSR 0.521, PBO 0.044)

| check | result | measured |
|---|---|---|
| PC-1 | PASS | 0.19 vs benchmark 0.19 |
| PC-3 | FAIL | DSR 0.521 |
| PC-4 | PASS | PBO 0.044 |
| PC-5 | PASS | drag 0.48% vs costs 0.77% (err 37%) |
| KC-1 | PASS | max full CAGR -14.61% |
| KC-2 | PASS | max turnover 21.08 |
| KC-3 | PASS | True |
| KC-4 | PASS | test maxDD 76.54% |
| KC-5 | PASS | min Σw 1.0000, max 1.0000 |
| KC-6 | PASS | min names 14 |

## Grid

| config | train Sharpe | test Sharpe | test CAGR | full CAGR | turnover | min names |
|---|---|---|---|---|---|---|
| **futures_mom_top30** **selected** | 0.12 | 0.19 | -16.29% | -14.61% | 5.43 | 14 |
| futures_mom_top20 | -0.11 | 0.22 | -15.84% | -20.38% | 12.83 | 14 |
| futures_mom_top10 | -0.43 | 0.07 | -28.50% | -35.02% | 21.08 | 10 |
