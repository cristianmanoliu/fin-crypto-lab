# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project is

**fin-crypto-lab** tests whether cross-sectional momentum transfers from US equities to crypto assets on Kraken. Weekly rotation, spot + perpetual futures, same honesty battery (DSR, PBO, kill conditions) as the sibling project `fin-equity-lab`. Backtest only; shadow only if PASS.

Design spec: `~/Main/code/active/fin-equity-lab/docs/superpowers/specs/2026-08-13-crypto-momentum-design.md`.

## Commands

```bash
uv run pytest tests/ -v                              # all tests (unit only, ~0.3s)
uv run pytest tests/test_signals.py -v                # single test file
uv run pytest tests/ -m integration                   # integration tests (hits Kraken API)

uv run python -m fin_crypto_lab.download --data-dir data/spot          # spot: full trade history
uv run python -m fin_crypto_lab.download --data-dir data/spot --fast   # spot: OHLC (720 candles max)
uv run python -m fin_crypto_lab.download --futures                     # futures: from futures.kraken.com

uv run python -m fin_crypto_lab.run_sweep --instrument spot                     # spot momentum sweep
uv run python -m fin_crypto_lab.run_sweep --instrument futures                  # futures momentum sweep
uv run python -m fin_crypto_lab.run_sweep --instrument spot --signal residual   # residual momentum
# --signal choices: momentum, residual, volwt, highprox, reversal, voladj, accel, lowvol, voltrend, meanrev
```

Sweep exit codes: 0 = PASS, 1 = FAIL, 2 = kill condition fired.

## Stack

Python 3.12+, polars, numpy, httpx, pytest. uv-managed. No `exchange_calendars` (24/7 market), no `scipy`.

## Key invariants

- **24/7 calendar.** Every calendar day is a session. No exchange holidays.
- **Formation dates:** every Sunday at 00:00 UTC.
- **Fill rule:** signal on close of formation day, fill at open of next session.
- **Cost model:** percentage-based taker fees. Spot: 80bp/side. Futures: 5bp/side.
- **Pair naming:** Kraken **altname** for spot (e.g. `XBTUSD`, `ETHUSD`). Futures use base+USD (e.g. `BTCUSD`, `ETHUSD`) from the `PF_` instrument's base field.
- **Train/test splits:**
  - Spot: 2017-01-01 to 2022-06-30 / 2022-07-01 to 2026-04-30.
  - Futures: 2022-03-27 to 2024-06-30 / 2024-07-01 to 2026-09-14 (perps launched 2022-03).
- **Grid:** 6 configs (spot top-10/20/30 at lookback=365, futures top-10/20/30 at lookback=90).
- **`metrics_overfit.py` is a verbatim copy** from fin-equity-lab. Do not modify.

## Architecture

Data flows left to right: download, panel, signal, backtest, sweep, verdict.

**Two Kraken APIs:**
- Spot: `api.kraken.com` (`kraken_client.get_asset_pairs`, `get_trades`, `get_ohlc`).
- Futures: `futures.kraken.com` (`get_futures_instruments`, `get_futures_ohlc`). Daily candles endpoint returns full history since instrument inception in one call.

**Data pipeline:** `download.py` orchestrates. `aggregate.py` converts raw trades to daily OHLCV. `store.py` manages parquet files + manifest. Layout: `data/{spot,futures}/ohlcv/*.parquet` + `manifest.parquet`.

**Panel:** `panel.py` builds aligned `[T sessions x N symbols]` numpy matrices from per-pair parquet files. `close_ff` is forward-filled after first valid bar (valuation price). `tradable` = bar exists AND volume > 0.

**Universe:** `universe.py` builds point-in-time volume-ranked snapshots at each formation date. 90-day trailing average daily USD volume. Top-N by volume.

**Signals:** `signals.py` contains 10 signal functions, all point-in-time (only panel indices <= f_idx are read):
- `momentum()` (raw price return), `residual_momentum()` (strips BTC beta via OLS)
- `volume_weighted_momentum()`, `vol_adjusted_momentum()` (momentum / realized vol)
- `high_proximity()` (52-week high ratio), `acceleration()` (recent vs older half momentum)
- `short_term_reversal()` (negative 28-day return), `mean_reversion()` (negative z-score)
- `low_volatility()` (negative realized vol), `volume_trend()` (recent/trailing volume ratio)

**Backtest:** `backtest.py` runs a NAV engine with percentage costs. `slippage_sweep()` runs the same strategy at multiple slippage levels.

**Sweep:** `sweep.py` holds the pre-registered grid, thresholds, and target construction (`topn_targets` with `min_names` floor). `run_sweep.py` is the honesty battery runner: grid search, DSR, PBO, kill conditions, verdict output.

**Selection rule:** highest train Sharpe within the instrument's sub-grid. PC-1 check compares selected config's test Sharpe against an equal-weight benchmark.
