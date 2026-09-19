# Crypto spot accel verdict (2026-09-19)

## FAMILY: FAIL

Selected: **spot_mom_top30** (DSR 0.828, PBO 0.000)

| check | result | measured |
|---|---|---|
| PC-1 | FAIL | 0.35 vs benchmark 0.39 |
| PC-3 | FAIL | DSR 0.828 |
| PC-4 | PASS | PBO 0.000 |
| PC-5 | PASS | drag 6.63% vs costs 11.28% (err 41%) |
| KC-1 | PASS | max full CAGR 9.94% |
| KC-2 | PASS | max turnover 9.82 |
| KC-3 | PASS | True |
| KC-4 | PASS | test maxDD 67.49% |
| KC-5 | PASS | min Σw 1.0000, max 1.0000 |
| KC-6 | PASS | min names 5 |

## Grid

| config | train Sharpe | test Sharpe | test CAGR | full CAGR | turnover | min names |
|---|---|---|---|---|---|---|
| **spot_mom_top30** **selected** | 0.53 | 0.35 | 4.22% | 9.94% | 3.73 | 5 |
| spot_mom_top20 | 0.52 | 0.14 | -7.81% | 4.44% | 5.28 | 5 |
| spot_mom_top10 | 0.47 | -0.50 | -39.92% | -14.99% | 9.82 | 5 |
