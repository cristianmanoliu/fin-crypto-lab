# Crypto spot voltrend verdict (2026-09-19)

## FAMILY: PASS

Selected: **spot_mom_top30** (DSR 0.999, PBO 0.030)

| check | result | measured |
|---|---|---|
| PC-1 | PASS | 0.39 vs benchmark 0.39 |
| PC-3 | PASS | DSR 0.999 |
| PC-4 | PASS | PBO 0.030 |
| PC-5 | PASS | drag 10.50% vs costs 13.83% (err 24%) |
| KC-1 | PASS | max full CAGR 54.25% |
| KC-2 | PASS | max turnover 11.67 |
| KC-3 | PASS | True |
| KC-4 | PASS | test maxDD 71.09% |
| KC-5 | PASS | min Σw 1.0000, max 1.0000 |
| KC-6 | PASS | min names 5 |

## Grid

| config | train Sharpe | test Sharpe | test CAGR | full CAGR | turnover | min names |
|---|---|---|---|---|---|---|
| **spot_mom_top30** **selected** | 1.01 | 0.39 | 4.90% | 54.25% | 4.81 | 5 |
| spot_mom_top20 | 1.01 | 0.24 | -5.26% | 47.72% | 7.62 | 5 |
| spot_mom_top10 | 0.95 | 0.05 | -19.79% | 32.67% | 11.67 | 5 |
