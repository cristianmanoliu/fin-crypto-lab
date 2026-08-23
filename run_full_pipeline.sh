#!/usr/bin/env bash
# Fire-and-forget: download all data, run both sweeps, report verdicts.
# Usage: nohup bash run_full_pipeline.sh > pipeline.log 2>&1 &
set -euo pipefail
cd "$(dirname "$0")"

echo "=== $(date) === CRYPTO MOMENTUM PIPELINE START ==="

echo ""
echo "--- SPOT DOWNLOAD ---"
uv run python -m fin_crypto_lab.download --data-dir data/spot
echo "--- SPOT DOWNLOAD DONE $(date) ---"

echo ""
echo "--- FUTURES DOWNLOAD ---"
uv run python -m fin_crypto_lab.download --data-dir data/futures
echo "--- FUTURES DOWNLOAD DONE $(date) ---"

echo ""
echo "--- SPOT SWEEP ---"
uv run python -m fin_crypto_lab.run_sweep --instrument spot
SPOT_EXIT=$?
echo "--- SPOT SWEEP EXIT: $SPOT_EXIT $(date) ---"

echo ""
echo "--- FUTURES SWEEP ---"
uv run python -m fin_crypto_lab.run_sweep --instrument futures
FUTURES_EXIT=$?
echo "--- FUTURES SWEEP EXIT: $FUTURES_EXIT $(date) ---"

echo ""
echo "=== $(date) === PIPELINE COMPLETE ==="
echo "SPOT:    exit $SPOT_EXIT (0=PASS, 1=FAIL, 2=KILL)"
echo "FUTURES: exit $FUTURES_EXIT (0=PASS, 1=FAIL, 2=KILL)"
echo "Verdicts in: results/"
ls -la results/crypto_*/verdict.md 2>/dev/null || echo "(no verdict files found)"
