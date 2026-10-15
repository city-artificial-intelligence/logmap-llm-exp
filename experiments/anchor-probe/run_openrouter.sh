#!/usr/bin/env bash
# Run every OpenRouter oracle in probe.toml on the probe sets (both tasks). Resumable: rerun to fill gaps.
#
#   experiments/anchor-probe/run_openrouter.sh                 # all OpenRouter models
#   experiments/anchor-probe/run_openrouter.sh google/gemini-2.5-flash
#   TASK=anatomy experiments/anchor-probe/run_openrouter.sh   # one task only
#   PROBE_SETS="v5-g-150 v5-mix-150" LIMIT=6 experiments/anchor-probe/run_openrouter.sh   # smoke test
#
# Needs OPENROUTER_API_KEY (OPEN_ROUTER_API_KEY is accepted too).
set -uo pipefail
cd "$(dirname "$0")/../.."
export PYTHONPATH=src

EXP=${EXP:-experiments/anchor-probe/probe.toml}
PROBE_SETS=${PROBE_SETS:-"v4-100 v4-200 v5-g-150 v5-mix-150"}
export OPENROUTER_API_KEY=${OPENROUTER_API_KEY:-${OPEN_ROUTER_API_KEY:-}}
[ -n "$OPENROUTER_API_KEY" ] || { echo "OPENROUTER_API_KEY is not set" >&2; exit 1; }

ps_args=(); for p in $PROBE_SETS; do ps_args+=(--probe-set "$p"); done
extra=(); [ -n "${LIMIT:-}" ] && extra+=(--limit "$LIMIT")
[ -n "${TASK:-}" ] && extra+=(--task "$TASK")   # e.g. TASK=anatomy
[ -n "${WORKERS:-}" ] && extra+=(--max-workers "$WORKERS")   # fewer parallel calls, e.g. WORKERS=2

mapfile -t models < <(python -m logmap_llm.anchor_probe models "$EXP" | awk -F'\t' 'NF==3 && $2=="openrouter" {print $1}')
[ $# -gt 0 ] && models=("$@")

failed=()
for m in "${models[@]}"; do
  echo "=== $m ==="
  python -m logmap_llm.anchor_probe consult "$EXP" --model "$m" "${ps_args[@]}" "${extra[@]}" || failed+=("$m")
done

[ ${#failed[@]} -eq 0 ] && echo "all done" || { echo "failed (rerun to resume): ${failed[*]}" >&2; exit 1; }
