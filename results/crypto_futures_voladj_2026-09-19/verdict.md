# Crypto futures voladj verdict (2026-09-19)

## FAMILY: FAIL

Selected: **futures_mom_top20** (DSR 0.747, PBO 0.248)

| check | result | measured |
|---|---|---|
| PC-1 | FAIL | 0.11 vs benchmark 0.19 |
| PC-3 | FAIL | DSR 0.747 |
| PC-4 | PASS | PBO 0.248 |
| PC-5 | PASS | drag 1.20% vs costs 1.89% (err 37%) |
| KC-1 | PASS | max full CAGR 2.41% |
| KC-2 | PASS | max turnover 16.69 |
| KC-3 | PASS | True |
| KC-4 | PASS | test maxDD 75.73% |
| KC-5 | PASS | min Σw 1.0000, max 1.0000 |
| KC-6 | PASS | min names 14 |

## Grid

| config | train Sharpe | test Sharpe | test CAGR | full CAGR | turnover | min names |
|---|---|---|---|---|---|---|
| **futures_mom_top20** **selected** | 0.72 | 0.11 | -19.16% | 2.41% | 11.66 | 14 |
| futures_mom_top30 | 0.62 | 0.19 | -16.03% | 1.18% | 5.17 | 14 |
| futures_mom_top10 | 0.54 | -0.01 | -24.83% | -6.50% | 16.69 | 10 |
