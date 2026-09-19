# Crypto futures meanrev verdict (2026-09-19)

## FAMILY: FAIL

Selected: **futures_mom_top20** (DSR 0.495, PBO 0.009)

| check | result | measured |
|---|---|---|
| PC-1 | FAIL | 0.15 vs benchmark 0.19 |
| PC-3 | FAIL | DSR 0.495 |
| PC-4 | PASS | PBO 0.009 |
| PC-5 | PASS | drag 1.25% vs costs 1.97% (err 37%) |
| KC-1 | PASS | max full CAGR -14.61% |
| KC-2 | PASS | max turnover 26.29 |
| KC-3 | PASS | True |
| KC-4 | FAIL | test maxDD 80.10% |
| KC-5 | PASS | min Σw 1.0000, max 1.0000 |
| KC-6 | PASS | min names 14 |

## Grid

| config | train Sharpe | test Sharpe | test CAGR | full CAGR | turnover | min names |
|---|---|---|---|---|---|---|
| **futures_mom_top20** **selected** | 0.16 | 0.15 | -21.05% | -16.43% | 14.20 | 14 |
| futures_mom_top30 | 0.12 | 0.19 | -16.29% | -14.61% | 5.43 | 14 |
| futures_mom_top10 | -0.37 | -0.01 | -31.41% | -34.42% | 26.29 | 10 |
