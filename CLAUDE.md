# CLAUDE.md

## What this project is

**fin-crypto-lab** — cross-sectional crypto momentum research platform.
Tests whether the momentum signal that drives `combo_blend` on US equities
transfers to crypto assets on Kraken. Weekly rotation, spot + perpetual
futures, same honesty battery (DSR, PBO, kill conditions). Backtest-first;
shadow only if PASS.

Sibling project to `~/Main/code/active/fin-equity-lab`. Design spec lives
there: `docs/superpowers/specs/2026-08-13-crypto-momentum-design.md`.
Implementation plan: `docs/superpowers/plans/2026-08-17-crypto-momentum.md`.

## Stack

- Python 3.12+, polars, numpy, httpx, pytest. uv-managed.
- No `exchange_calendars` (24/7 market), no `scipy`.
- `metrics_overfit.py` is a **verbatim copy** from fin-equity-lab — do not modify.
- Data source: Kraken REST API (public endpoints, trades-based OHLCV).

## Key invariants

- **24/7 calendar.** Every calendar day is a session. No exchange holidays.
- **Formation dates:** every Sunday at 00:00 UTC.
- **Fill rule:** signal on close of formation day → fill at open of next session.
- **Cost model:** percentage-based taker fees. Spot: 80bp/side. Futures: 5bp/side.
- **Pair naming:** Kraken **altname** internally (e.g. `XBTUSD`, `ETHUSD`).
- **Train/test split:** 2017-01-01 to 2022-06-30 / 2022-07-01 to 2026-04-30.
- **Grid:** 6 configs (spot top-10/20/30, futures top-10/20/30). Lookback=365, skip=7.
