#!/usr/bin/env bash
# Run every local (vLLM) oracle in probe.toml on the probe sets (both tasks). Resumable: rerun to fill gaps.
# Each model must already be served at the base_url of its job config (after [path_map]); a model whose
# endpoint does not answer is skipped, so serve one model, run this, swap, run again.
#
#   experiments/anchor-probe/run_local.sh                      # every local model that is up
#   experiments/anchor-probe/run_local.sh Qwen3-8B Gemma-3-27B
#   PROBE_SETS="v5-g-150 v5-mix-150" LIMIT=6 experiments/anchor-probe/run_local.sh   # smoke test
set -uo pipefail
cd "$(dirname "$0")/../.."
export PYTHONPATH=src

EXP=${EXP:-experiments/anchor-probe/probe.toml}
PROBE_SETS=${PROBE_SETS:-"v4-100 v4-200 v5-g-150 v5-mix-150"}

ps_args=(); for p in $PROBE_SETS; do ps_args+=(--probe-set "$p"); done
extra=(); [ -n "${LIMIT:-}" ] && extra+=(--limit "$LIMIT")

declare -A url; local_models=()
while IFS=$'\t' read -r label style base; do
  [ "$style" = "openrouter" ] || { url[$label]=$base; local_models+=("$label"); }
done < <(python -m logmap_llm.anchor_probe models "$EXP" | awk -F'\t' 'NF==3')

if [ $# -gt 0 ]; then models=("$@"); else models=("${local_models[@]}"); fi

done_=(); skipped=(); failed=()
for m in "${models[@]}"; do
  base=${url[$m]:-}
  [ -n "$base" ] || { echo "$m: not a local model in $EXP" >&2; failed+=("$m"); continue; }
  if ! curl -sf -m 5 "$base/models" >/dev/null; then
    echo "--- $m: no server at $base, skipped"; skipped+=("$m"); continue
  fi
  echo "=== $m ($base) ==="
  if python -m logmap_llm.anchor_probe consult "$EXP" --model "$m" "${ps_args[@]}" "${extra[@]}"; then
    done_+=("$m"); else failed+=("$m"); fi
done

echo "done: ${done_[*]:-none}"
echo "skipped (server down): ${skipped[*]:-none}"
[ ${#failed[@]} -eq 0 ] || { echo "failed (rerun to resume): ${failed[*]}" >&2; exit 1; }
