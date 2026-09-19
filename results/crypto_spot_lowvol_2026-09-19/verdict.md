# Crypto spot lowvol verdict (2026-09-19)

## FAMILY: FAIL

Selected: **spot_mom_top30** (DSR 0.999, PBO 0.633)

| check | result | measured |
|---|---|---|
| PC-1 | FAIL | 0.39 vs benchmark 0.39 |
| PC-3 | PASS | DSR 0.999 |
| PC-4 | FAIL | PBO 0.633 |
| PC-5 | PASS | drag 10.54% vs costs 13.78% (err 24%) |
| KC-1 | PASS | max full CAGR 55.30% |
| KC-2 | PASS | max turnover 5.07 |
| KC-3 | PASS | True |
| KC-4 | PASS | test maxDD 71.09% |
| KC-5 | PASS | min Σw 1.0000, max 1.0000 |
| KC-6 | PASS | min names 5 |

## Grid

| config | train Sharpe | test Sharpe | test CAGR | full CAGR | turnover | min names |
|---|---|---|---|---|---|---|
| **spot_mom_top30** **selected** | 1.02 | 0.39 | 4.73% | 54.96% | 4.80 | 5 |
| spot_mom_top20 | 1.01 | 0.27 | 0.55% | 51.32% | 5.07 | 5 |
| spot_mom_top10 | 0.94 | 0.63 | 17.48% | 55.30% | 4.81 | 5 |
