# Crypto spot momentum verdict (2026-09-30)

## FAMILY: FAIL

Selected: **spot_mom_top10** (DSR 0.765 at n_trials=69, PBO 0.148)

| check | result | measured |
|---|---|---|
| PC-1 | FAIL | 0.26 vs benchmark 0.31 |
| PC-3 | FAIL | DSR 0.765 (n_trials=69) |
| PC-4 | PASS | PBO 0.148 |
| PC-5 | PASS | drag 12.24% vs costs 20.86% (err 41%) |
| KC-1 | PASS | max full CAGR 2.75% |
| KC-2 | PASS | max turnover 7.30 |
| KC-3 | PASS | True |
| KC-4 | PASS | test maxDD 69.31% |
| KC-5 | PASS | min Σw 1.0000, max 1.0000 |
| KC-6 | PASS | min names 5 |

## Grid

| config | train Sharpe | test Sharpe | test CAGR | full CAGR | turnover | min names |
|---|---|---|---|---|---|---|
| **spot_mom_top10** **selected** | 0.38 | 0.26 | -2.51% | -1.86% | 7.30 | 5 |
| spot_mom_top30 | 0.37 | 0.39 | 6.60% | 2.75% | 3.91 | 5 |
| spot_mom_top20 | 0.35 | 0.19 | -5.01% | -3.01% | 5.73 | 5 |
