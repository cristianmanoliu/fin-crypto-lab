# Crypto spot voladj verdict (2026-09-19)

## FAMILY: FAIL

Selected: **spot_mom_top30** (DSR 0.903, PBO 0.123)

| check | result | measured |
|---|---|---|
| PC-1 | FAIL | 0.35 vs benchmark 0.39 |
| PC-3 | PASS | DSR 0.903 |
| PC-4 | PASS | PBO 0.123 |
| PC-5 | PASS | drag 6.63% vs costs 11.28% (err 41%) |
| KC-1 | PASS | max full CAGR 9.94% |
| KC-2 | PASS | max turnover 7.18 |
| KC-3 | PASS | True |
| KC-4 | PASS | test maxDD 67.49% |
| KC-5 | PASS | min Σw 1.0000, max 1.0000 |
| KC-6 | PASS | min names 5 |

## Grid

| config | train Sharpe | test Sharpe | test CAGR | full CAGR | turnover | min names |
|---|---|---|---|---|---|---|
| **spot_mom_top30** **selected** | 0.53 | 0.35 | 4.22% | 9.94% | 3.73 | 5 |
| spot_mom_top20 | 0.52 | 0.25 | -2.55% | 6.49% | 4.82 | 5 |
| spot_mom_top10 | 0.50 | 0.09 | -11.14% | 0.62% | 7.18 | 5 |
