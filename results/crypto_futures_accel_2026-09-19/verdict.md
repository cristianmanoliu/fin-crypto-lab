# Crypto futures accel verdict (2026-09-19)

## FAMILY: FAIL

Selected: **futures_mom_top10** (DSR 0.833, PBO 0.396)

| check | result | measured |
|---|---|---|
| PC-1 | PASS | 0.36 vs benchmark 0.19 |
| PC-3 | FAIL | DSR 0.833 |
| PC-4 | PASS | PBO 0.396 |
| PC-5 | PASS | drag 3.00% vs costs 4.67% (err 36%) |
| KC-1 | PASS | max full CAGR 7.29% |
| KC-2 | PASS | max turnover 27.67 |
| KC-3 | PASS | True |
| KC-4 | PASS | test maxDD 75.04% |
| KC-5 | PASS | min Σw 1.0000, max 1.0000 |
| KC-6 | PASS | min names 10 |

## Grid

| config | train Sharpe | test Sharpe | test CAGR | full CAGR | turnover | min names |
|---|---|---|---|---|---|---|
| **futures_mom_top10** **selected** | 0.67 | 0.36 | -9.09% | 7.29% | 27.67 | 10 |
| futures_mom_top30 | 0.62 | 0.19 | -16.03% | 1.18% | 5.17 | 14 |
| futures_mom_top20 | 0.58 | 0.31 | -8.24% | 4.28% | 14.61 | 14 |
