# fin-crypto-lab

This project tests if cross-sectional momentum moves from US equities to crypto assets on Kraken. It uses weekly rotation on spot and perpetual futures. It applies the same honesty battery as the sibling project fin-equity-lab: DSR (Deflated Sharpe Ratio), PBO (Probability of Backtest Overfitting), and kill conditions.

## Result

This project ran 20 sweeps (10 signals x spot and futures). 19 sweeps returned FAIL. 1 sweep returned a narrow PASS (spot volume-trend, Sharpe 0.39, equal to the benchmark). No deployable edge exists. The project is complete.

The honesty battery ran at a cumulative N=69 trials. The 2026-09-19 batch (60 of those trials) deflated at N=3 on a panel with a six-year XBTUSD hole. The project records that batch as spent trials, not as correct results. See `docs/findings/2026-09-23-crypto-verdicts-n3-and-xbt-hole.md`.

## Architecture

Data flows through these steps: download, panel, signal, backtest, sweep, verdict.

The project uses two Kraken APIs:
- Spot market: `api.kraken.com` (trades and OHLC)
- Futures market: `futures.kraken.com` (daily candles, full history for each instrument)

`download.py` controls the download. `aggregate.py` converts raw trades to daily OHLCV. `store.py` controls the parquet files and the manifest. Data location: `data/{spot,futures}/ohlcv/*.parquet` and `manifest.parquet`.

`panel.py` assembles aligned `[T x N]` numpy matrices. `universe.py` assembles point-in-time volume snapshots at each formation date. It uses a 90-day trailing average daily USD volume. `signals.py` contains 10 signal functions. All functions are point-in-time.

## Signals

| Signal | Description |
|---|---|
| `momentum` | Raw price return |
| `residual_momentum` | Removes BTC beta through OLS |
| `volume_weighted_momentum` | Momentum weighted by volume |
| `vol_adjusted_momentum` | Momentum divided by realized vol |
| `high_proximity` | 52-week high ratio |
| `acceleration` | Recent half vs older half momentum |
| `short_term_reversal` | Negative 28-day return |
| `mean_reversion` | Negative z-score |
| `low_volatility` | Negative realized vol |
| `volume_trend` | Recent vs trailing volume ratio |

## Key invariants

- 24/7 calendar. All calendar days are sessions.
- Formation dates: each Sunday at 00:00 UTC.
- Fill rule: signal on close of formation day, fill at open of next session.
- Cost model: percentage taker fees. Spot 80bp/side, futures 5bp/side.
- Pair naming: Kraken altname for spot (for example `XBTUSD`). Futures use the format currency+USD (for example `BTCUSD`).
- Train/test splits, spot: train 2017-01-01 to 2022-06-30, test 2022-07-01 to 2026-04-30.
- Train/test splits, futures: train 2022-03-27 to 2024-06-30, test 2024-07-01 to 2026-09-14.
- Grid: 6 configs. Spot: top-10/20/30 at lookback=365. Futures: top-10/20/30 at lookback=90.

## Commands

```bash
uv run pytest tests/ -v                              # all tests (~0.3s)

uv run python -m fin_crypto_lab.download --data-dir data/spot          # spot: full trade history
uv run python -m fin_crypto_lab.download --data-dir data/spot --fast   # spot: OHLC (720 candles max)
uv run python -m fin_crypto_lab.download --futures                     # futures: from futures.kraken.com

uv run python -m fin_crypto_lab.run_sweep --instrument spot                     # spot momentum sweep
uv run python -m fin_crypto_lab.run_sweep --instrument futures                  # futures momentum sweep
uv run python -m fin_crypto_lab.run_sweep --instrument spot --signal residual   # residual momentum
```

Sweep exit codes: 0 = PASS, 1 = FAIL, 2 = kill condition fired.

## Stack

Python 3.12+, polars, numpy, httpx, pytest. Managed with uv.
