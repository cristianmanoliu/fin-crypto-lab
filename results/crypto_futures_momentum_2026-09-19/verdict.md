# Crypto futures momentum verdict (2026-09-19)

## FAMILY: FAIL

Selected: **futures_mom_top20** (DSR 0.659, PBO 0.016)

| check | result | measured |
|---|---|---|
| PC-1 | FAIL | -0.02 vs benchmark 0.19 |
| PC-3 | FAIL | DSR 0.659 |
| PC-4 | PASS | PBO 0.016 |
| PC-5 | PASS | drag 1.12% vs costs 1.84% (err 39%) |
| KC-1 | PASS | max full CAGR 1.18% |
| KC-2 | PASS | max turnover 16.80 |
| KC-3 | PASS | True |
| KC-4 | PASS | test maxDD 79.93% |
| KC-5 | PASS | min Σw 1.0000, max 1.0000 |
| KC-6 | PASS | min names 14 |

## Grid

| config | train Sharpe | test Sharpe | test CAGR | full CAGR | turnover | min names |
|---|---|---|---|---|---|---|
| **futures_mom_top20** **selected** | 0.76 | -0.02 | -25.65% | -0.58% | 11.12 | 14 |
| futures_mom_top30 | 0.62 | 0.19 | -16.03% | 1.18% | 5.17 | 14 |
| futures_mom_top10 | 0.45 | -0.25 | -35.89% | -16.20% | 16.80 | 10 |
