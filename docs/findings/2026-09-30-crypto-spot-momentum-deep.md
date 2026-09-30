# Crypto spot momentum on full trade history: FAIL

Date: 2026-09-30

## Result

The pre-registered deep re-run (`results/crypto_spot_momentum_deep_decision_rule_2026-09-23.md`,
N = 69) FAILED. The run used the full 2017+ trade history for the top 60 pairs. The data
gate passed first: DG-1 60/60 pairs checkpointed after 2026-09-01, DG-2 zero unexplained gaps.
Verdict: `results/crypto_spot_momentum_2026-09-30/verdict.md`.

| check | result | measured |
|---|---|---|
| PC-1 | FAIL | test Sharpe 0.26 vs benchmark 0.31 |
| PC-3 | FAIL | DSR 0.765 at n_trials = 69 |
| PC-4 | PASS | PBO 0.148 |
| PC-5 | PASS | drag 12.24% vs costs 20.86% |
| KC-1 to KC-6 | PASS | test maxDD 69.31% |

Selected config: `spot_mom_top10` (train 0.38, test 0.26, test CAGR -2.51%).
The other two: `spot_mom_top30` test 0.39 (CAGR 6.60%), `spot_mom_top20` test 0.19.

## What it means

The 08-24 FAIL was not only a data-depth artifact. With about nine years of data, momentum
is still below its benchmark and the drawdown is near 70%. No config beats the benchmark
on the train-selected pick. `spot_mom_top30` reaches test 0.39, but the runner selects on
train Sharpe, so that is not a pick. Choosing it now would be selection on the test set.

The PC-4 pass (PBO 0.148) says the ranking among the three configs is stable. It does not
say the family has an edge.

## Consequences

- Crypto spot momentum is CLOSED. A retry needs a materially different construct and its
  own pre-registration (same closure logic as the equity lab).
- The "download the remaining ~595 pairs" follow-up is NOT authorized. Only a PASS authorized it.
- The cumulative DSR budget stays at N = 69. This run was already counted.
- Survivorship caveat from the pre-reg still holds: the panel is pairs liquid today. It
  flatters the result, so the FAIL is, if anything, understated.
