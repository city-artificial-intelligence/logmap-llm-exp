#!/usr/bin/env bash
# One command for the experiment: check paths, run models, report, plot. Always resumable.
#
#   experiments/anchor-probe/run_all.sh            # step 1: local vLLM models (those whose server is up)
#   experiments/anchor-probe/run_all.sh openrouter # step 2: OpenRouter models (needs OPENROUTER_API_KEY)
#   experiments/anchor-probe/run_all.sh all        # both
#   LIMIT=6 experiments/anchor-probe/run_all.sh    # smoke test
#
# Local models whose server is down are skipped: serve the missing ones and rerun. DeepSeek and Mistral results are
# already in runs/, so step 2 only asks gemini-2.5-flash. Commit experiments/anchor-probe/runs/ afterwards.
set -uo pipefail
cd "$(dirname "$0")/../.."
export PYTHONPATH=src
EXP=${EXP:-experiments/anchor-probe/probe.toml}
export EXP
mode=${1:-local}

python -m logmap_llm.anchor_probe check "$EXP" || exit 1
rc_local=0; rc_or=0
case $mode in local|all) experiments/anchor-probe/run_local.sh; rc_local=$? ;; esac
case $mode in openrouter|all) experiments/anchor-probe/run_openrouter.sh; rc_or=$? ;; esac
python -m logmap_llm.anchor_probe report "$EXP"
python -m logmap_llm.anchor_probe budget "$EXP"
python experiments/anchor-probe/plot_results.py
exit $((rc_local || rc_or))
