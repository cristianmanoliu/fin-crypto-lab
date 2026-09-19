# Crypto spot volwt verdict (2026-09-19)

## FAMILY: FAIL

Selected: **spot_mom_top10** (DSR 0.993, PBO 0.153)

| check | result | measured |
|---|---|---|
| PC-1 | FAIL | -0.03 vs benchmark 0.39 |
| PC-3 | PASS | DSR 0.993 |
| PC-4 | PASS | PBO 0.153 |
| PC-5 | PASS | drag 15.90% vs costs 22.55% (err 29%) |
| KC-1 | PASS | max full CAGR 54.96% |
| KC-2 | PASS | max turnover 8.00 |
| KC-3 | PASS | True |
| KC-4 | FAIL | test maxDD 86.71% |
| KC-5 | PASS | min Σw 1.0000, max 1.0000 |
| KC-6 | PASS | min names 5 |

## Grid

| config | train Sharpe | test Sharpe | test CAGR | full CAGR | turnover | min names |
|---|---|---|---|---|---|---|
| **spot_mom_top10** **selected** | 1.04 | -0.03 | -26.35% | 35.49% | 8.00 | 5 |
| spot_mom_top20 | 1.02 | 0.28 | -5.58% | 48.64% | 6.19 | 5 |
| spot_mom_top30 | 1.02 | 0.39 | 4.73% | 54.96% | 4.80 | 5 |
