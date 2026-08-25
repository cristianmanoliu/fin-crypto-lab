# Crypto spot momentum verdict (2026-08-24)

## FAMILY: FAIL

Selected: **spot_mom_top10** (DSR 0.048, PBO 0.767)

| check | result | measured |
|---|---|---|
| PC-1 | FAIL | -0.69 vs benchmark -0.14 |
| PC-3 | FAIL | DSR 0.048 |
| PC-4 | FAIL | PBO 0.767 |
| PC-5 | PASS | drag 1.30% vs costs 1.49% (err 13%) |
| KC-1 | PASS | max full CAGR -5.49% |
| KC-2 | PASS | max turnover 0.83 |
| KC-3 | PASS | True |
| KC-4 | PASS | test maxDD 48.56% |
| KC-5 | PASS | min Σw 1.0000, max 1.0000 |
| KC-6 | PASS | min names 10 |

## Grid

| config | train Sharpe | test Sharpe | test CAGR | full CAGR | turnover | min names |
|---|---|---|---|---|---|---|
| **spot_mom_top10** **selected** | nan | -0.69 | -12.83% | -5.49% | 0.83 | 10 |
| spot_mom_top20 | nan | -0.91 | -15.53% | -6.71% | 0.63 | 20 |
| spot_mom_top30 | nan | -0.89 | -15.32% | -6.61% | 0.48 | 21 |
