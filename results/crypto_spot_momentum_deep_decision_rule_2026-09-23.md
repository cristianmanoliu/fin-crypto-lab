# Crypto spot momentum on full trade history: decision rule (2026-09-23)

Status: LOCKED at commit. Any change is a new dated `_v2` doc.

## Purpose

Re-run the pre-registered spot momentum grid on the completed top-60
trade-history panel (Kraken `/public/Trades`, 2017 onward). The
2026-08-24 spot FAIL rested on the 720-candle OHLC cap (about two years of
data), which cannot reach `TRAIN_END`. The 2026-09-19 batch is not evidence:
it ran while XBTUSD had a data hole from 2018-08-07 to 2024-09-03, and it
deflated every DSR at N = 3 (see the finding of the same date).

## Trial ledger (cumulative, this dataset)

| Date | Run | Trials | Pre-registered |
|---|---|---|---|
| 2026-08-24 | spot + futures momentum, 3 configs each | 6 | yes (design spec) |
| 2026-09-19 | 10 signals x 3 configs x 2 instruments | 60 | no |
| 2026-09-23 | this run: spot momentum, 3 configs | 3 | this doc |

The 09-19 trials count although their panel was defective: their outcomes
were observed, and that is what the deflation corrects for.
**This run deflates at N = 69.** `sweep.THRESHOLDS["N_TRIALS"]` is the
fixture value and the runner passes it to `deflated_sharpe_ratio`.
Futures configs are not re-run: their data did not change.

## Data gate (all must hold before the runner starts)

- DG-1: every top-60 pair (`download._top_pairs_by_volume`, top = 60) has
  `last_trade_id > 0` and a checkpoint date on or after 2026-09-01.
- DG-2: no top-60 pair has a gap over 7 days after 2017-01-01, except the
  accepted Kraken-side thin stretches: LTCUSD 2013 to 2015, XLMUSD
  2018-02-16 to 2018-08-13 (both came from completed trade runs, so the
  exchange has no trades there).
- DG-3: the download process has exited (`pgrep -f fin_crypto_lab.download`
  returns nothing) before the manifest is read.

`scripts/check_top60_complete.py` evaluates DG-1 and DG-2 and exits 0 only
when both hold. Its output is pasted into the finding.

## Construct (unchanged from `sweep.py` and `config.py`)

- Signal: `signals.momentum`, lookback 365 sessions, skip 7.
- Grid: `spot_mom_top10`, `spot_mom_top20`, `spot_mom_top30`, equal weight,
  weekly formation every Sunday 00:00 UTC, fill at next open.
- Universe: top 30 by trailing 90-day average USD volume among all pairs
  with data on disk, point in time.
- Costs: 80 bp taker per side. Slip sweep 0 / 50 / 100 / 160 bp. Verdict
  reads the 160 bp member.
- Split: formations 2017-01-01 to 2026-04-30, `TRAIN_END` 2022-06-30.
- Selection: highest train Sharpe among the three configs.

## Checks (numbered as the runner reports them)

| Check | Rule |
|---|---|
| PC-1 | Selected config test Sharpe >= equal-weight universe benchmark test Sharpe |
| PC-3 | DSR >= 0.90 at N = 69 |
| PC-4 | PBO <= 0.50 (CSCV, 16 blocks, across the 3 configs) |
| PC-5 | Cost reconciliation error <= 50% |
| KC-1 | No config full-sample CAGR > 100% |
| KC-2 | No config annual turnover > 52x |
| KC-3 | All NAV paths finite and positive |
| KC-4 | Selected config test max drawdown <= 80% |
| KC-5 | Weights sum to 1 within 0.001 at every formation |
| KC-6 | Selected config never holds fewer than 5 names |

Exit 0 = PASS, 1 = FAIL, 2 = a KC fired.

## Disclosed limitations

1. **Survivorship in the train window.** Only the 60 pairs most liquid in
   2024-08 to 2026-08 have history before 2024-08. Pairs that were liquid
   in 2018 to 2023 and later faded or delisted are absent from the train
   universe. Long-only returns on survivors are biased upward. Therefore:
   a FAIL on this panel is robust. A PASS is provisional and has one
   consequence only: it authorizes downloading the full trade history of
   the remaining pairs and a new pre-registration. **No shadow follows from
   this run.**
2. **Thin train universe.** 31 of the 60 pairs list after `TRAIN_END`, so
   the train universe never exceeds 29 pairs. KC-6 applies as written.
3. **XRPUSD rows between 2024-11-26 and 2026-08-24 were OHLC-sourced** at
   the time of writing. The restarted download replaces them with
   trade-aggregated bars. DG-1 confirms the replacement happened.

## Outputs

`results/crypto_spot_momentum_<run date>/verdict.md` (the runner names the
folder by run date) and `docs/findings/<run date>-crypto-spot-momentum-deep.md`.
