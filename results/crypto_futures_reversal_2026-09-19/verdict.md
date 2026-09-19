# Crypto futures reversal verdict (2026-09-19)

## FAMILY: FAIL

Selected: **futures_mom_top20** (DSR 0.574, PBO 0.081)

| check | result | measured |
|---|---|---|
| PC-1 | FAIL | 0.18 vs benchmark 0.19 |
| PC-3 | FAIL | DSR 0.574 |
| PC-4 | PASS | PBO 0.081 |
| PC-5 | PASS | drag 1.60% vs costs 2.45% (err 35%) |
| KC-1 | PASS | max full CAGR -12.24% |
| KC-2 | PASS | max turnover 34.29 |
| KC-3 | PASS | True |
| KC-4 | FAIL | test maxDD 81.28% |
| KC-5 | PASS | min Σw 1.0000, max 1.0000 |
| KC-6 | PASS | min names 14 |

## Grid

| config | train Sharpe | test Sharpe | test CAGR | full CAGR | turnover | min names |
|---|---|---|---|---|---|---|
| **futures_mom_top20** **selected** | 0.24 | 0.18 | -17.94% | -12.24% | 17.55 | 14 |
| futures_mom_top30 | 0.12 | 0.19 | -16.29% | -14.61% | 5.43 | 14 |
| futures_mom_top10 | -0.19 | 0.04 | -31.87% | -31.79% | 34.29 | 10 |
