# Crypto spot momentum verdict (2026-09-19)

## FAMILY: FAIL

Selected: **spot_mom_top10** (DSR 0.899, PBO 0.265)

| check | result | measured |
|---|---|---|
| PC-1 | FAIL | 0.20 vs benchmark 0.39 |
| PC-3 | FAIL | DSR 0.899 |
| PC-4 | PASS | PBO 0.265 |
| PC-5 | PASS | drag 12.39% vs costs 22.54% (err 45%) |
| KC-1 | PASS | max full CAGR 9.94% |
| KC-2 | PASS | max turnover 6.90 |
| KC-3 | PASS | True |
| KC-4 | PASS | test maxDD 70.87% |
| KC-5 | PASS | min Σw 1.0000, max 1.0000 |
| KC-6 | PASS | min names 5 |

## Grid

| config | train Sharpe | test Sharpe | test CAGR | full CAGR | turnover | min names |
|---|---|---|---|---|---|---|
| **spot_mom_top10** **selected** | 0.58 | 0.20 | -6.11% | 6.65% | 6.90 | 5 |
| spot_mom_top20 | 0.53 | 0.16 | -6.50% | 5.22% | 5.06 | 5 |
| spot_mom_top30 | 0.53 | 0.35 | 4.22% | 9.94% | 3.73 | 5 |
