# Crypto spot momentum verdict (2026-09-19)

## FAMILY: FAIL

Selected: **spot_mom_top30** (DSR 0.992, PBO 0.075)

| check | result | measured |
|---|---|---|
| PC-1 | FAIL | 0.39 vs benchmark 0.39 |
| PC-3 | PASS | DSR 0.992 |
| PC-4 | PASS | PBO 0.075 |
| PC-5 | PASS | drag 10.54% vs costs 13.78% (err 24%) |
| KC-1 | PASS | max full CAGR 54.96% |
| KC-2 | PASS | max turnover 38.58 |
| KC-3 | PASS | True |
| KC-4 | PASS | test maxDD 71.09% |
| KC-5 | PASS | min Σw 1.0000, max 1.0000 |
| KC-6 | PASS | min names 5 |

## Grid

| config | train Sharpe | test Sharpe | test CAGR | full CAGR | turnover | min names |
|---|---|---|---|---|---|---|
| **spot_mom_top30** **selected** | 1.02 | 0.39 | 4.73% | 54.96% | 4.80 | 5 |
| spot_mom_top20 | 0.97 | -0.44 | -42.07% | 17.16% | 16.91 | 5 |
| spot_mom_top10 | 0.59 | 0.47 | -41.87% | -10.92% | 38.58 | 5 |
