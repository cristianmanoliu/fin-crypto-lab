# The 2026-09-19 crypto verdicts: deflated at N = 3, on a panel with no Bitcoin for six years

Date: 2026-09-23

## What happened

On 2026-09-19 (commits `b07120c`, `4aaf3fb`, `5f87365`, `13db17d`) a
10-signal batch sweep ran on spot and futures and wrote 20 verdicts to
`results/*_2026-09-19/`. One read PASS: `crypto_spot_voltrend` (test Sharpe
0.39, equal to its benchmark, test max drawdown 71%, DSR 0.999). Two defects
make every one of those 20 verdicts non-evidence.

### 1. The DSR deflated at N = 3

`run_sweep.py` called `deflated_sharpe_ratio` without `n_trials`, so the
trial count fell back to `len(trial_sharpes)`, which is the three configs
of the instrument sub-grid. The fixture value `THRESHOLDS["N_TRIALS"]` (then
6) was never read. Three near-identical configs (train Sharpes 1.01, 1.01,
0.95) also give a tiny cross-sectional variance, so the expected maximum
Sharpe under the null is near zero and the DSR reads 0.999 for almost any
positive Sharpe. This is the same defect fin-equity-lab found in the
insider-cluster family (N derived from the grid, not the cumulative budget).

No pre-registration exists for the batch. The design spec registers six
momentum configs. The other nine signals appeared in code and in verdicts on
the same day.

### 2. XBTUSD had no trades data from 2018-08-07 to 2024-09-03

The trades download for XBTUSD died with an error class the retry wrapper
did not catch. The per-pair `except` moved on, the manifest kept the 2018
checkpoint with `last_trade_id > 0`, and later sessions read that as
"finished". XRPUSD failed the same way on 2026-09-23 at its Nov-2024
checkpoint, which is how the pattern was found.

`tradable` requires a bar with volume, so Bitcoin was absent from the
universe for the last four years of the train window and the first two of
the test window. `residual_momentum` strips the market column, which is
XBTUSD when present. Every 09-19 run saw this panel.

## What is done

- `kraken_client._get_with_retry` now retries on any `httpx.TransportError`
  (`669524d`). The download was restarted the same evening and resumes both
  pairs from their checkpoints.
- `run_sweep.py` passes `n_trials=THRESHOLDS["N_TRIALS"]` and prints it in
  the verdict. `THRESHOLDS["N_TRIALS"]` is 69: 6 (2026-08-24) + 60
  (2026-09-19) + 3 (the deep re-run). Test-locked.
- Pre-registration for the deep re-run:
  `results/crypto_spot_momentum_deep_decision_rule_2026-09-23.md`, with a
  data gate (`scripts/check_top60_complete.py`) that must pass before the
  runner starts.

## What is not done, on purpose

- The 20 verdicts of 2026-09-19 stay as committed. They are listed here as
  spent trials and nothing else. Do not cite `crypto_spot_voltrend` as a
  PASS.
- The nine non-momentum signals have no pre-registration. Re-running them on
  the deep panel costs 27 more trials each time and needs its own doc first.

## Lessons

- A checkpoint is not completion. `last_trade_id > 0` means "some trades
  were saved", not "the pair is done". The gate is the checkpoint DATE
  decoded from the id (nanoseconds), plus a gap scan of the parquet.
- A per-pair `except` that logs and continues turns a crash into a silent
  hole. The log line `ERROR FAILED: <pair>` is the only trace, and the log
  file is ephemeral.
- A DSR near 1.0 on a three-config grid is a symptom, not a result.
