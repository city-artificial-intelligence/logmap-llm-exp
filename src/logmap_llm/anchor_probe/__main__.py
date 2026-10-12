"""CLI:  python -m logmap_llm.anchor_probe <command> <probe.toml> [options]

  check    load every job config, list the LogMap files, reference and M_ask prediction files each task will use
  build    build a probe set (v4 or v5) for one task from LogMap's anchors / hard-discarded output
  consult  run each job's oracle on each probe set of a task (resumable; --dry-run makes no calls)
  report   compare probe ranking with real M_ask ranking (no calls)
  negtypes type M_ask's false candidates by hierarchy relation to the true match; same for probe negatives (no calls)
"""
from __future__ import annotations

import argparse
from pathlib import Path

from .inputs import load_experiment, logmap_file


def main() -> None:
    ap = argparse.ArgumentParser(prog="python -m logmap_llm.anchor_probe", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("check", "build", "consult", "report", "negtypes"):
        p = sub.add_parser(name)
        p.add_argument("experiment", help="probe.toml")
        p.add_argument("--task", action="append", help="restrict to these task names (repeatable)")
        if name == "build":
            p.add_argument("--version", choices=["v4", "v5"], required=True)
            p.add_argument("--n-pos", type=int, default=50)
            p.add_argument("--n-neg", type=int, default=50, help="v4: hard-discarded; v5: granularity negatives")
            p.add_argument("--n-lexical", type=int, default=0, help="v5 only: extra v4-style hard-discarded negatives")
            p.add_argument("--lo", type=float, default=0.3)
            p.add_argument("--hi", type=float, default=0.8)
            p.add_argument("--pool-frac", type=float, default=0.1)
            p.add_argument("--seed", type=int, default=42)
            p.add_argument("--max-children", type=int, default=50, help="v5: drop substituted hub classes")
            p.add_argument("--out", required=True, help="output labels TSV")
        if name == "consult":
            p.add_argument("--model", action="append", help="restrict to these oracle model_names (repeatable)")
            p.add_argument("--probe-set", action="append", help="restrict to probe sets whose file stem matches")
            p.add_argument("--limit", type=int, default=None, help="first N pairs only (smoke test)")
            p.add_argument("--max-workers", type=int, default=None)
            p.add_argument("--dry-run", action="store_true")
        if name == "report":
            p.add_argument("--probe-set", action="append")
    a = ap.parse_args()
    tasks = load_experiment(a.experiment, a.task)

    if a.cmd == "check":
        for t in tasks:
            print(f"[{t.name}] LogMap task {t.cfg.alignmentTask.task_name!r}, {len(t.jobs)} jobs, logmap_dir {t.logmap_dir}")
            print(f"  ontologies: {t.cfg.alignmentTask.onto_source_filepath} | {t.cfg.alignmentTask.onto_target_filepath}")
            print(f"  reference : {t.extra.get('reference') or t.cfg.evaluation.reference_alignment_path}")
            for kind in ("anchors", "hard_discarded", "m_ask"):
                try:
                    print(f"  {kind:14s}: {logmap_file(t, kind)}")
                except FileNotFoundError as e:
                    print(f"  {kind:14s}: MISSING ({e})")
            for j in t.jobs:
                pc = Path(j.paths.predictions_csv())
                print(f"  - {j.label:42s} {j.cfg.oracle.interaction_style!s:28s} {j.cfg.oracle.base_url}  "
                      f"M_ask predictions {'ok' if pc.exists() else 'MISSING'}: {pc}")
            for ps in t.probe_sets:
                print(f"  probe set {ps.name}: {'ok' if ps.exists() else 'MISSING'}")
        return

    if a.cmd == "build":
        from .build import build
        if len(tasks) != 1:
            raise SystemExit("build: select exactly one task with --task")
        build(tasks[0], a.version, a.n_pos, a.n_neg, Path(a.out), n_lexical=a.n_lexical, lo=a.lo, hi=a.hi,
              pool_frac=a.pool_frac, seed=a.seed, max_children=a.max_children)
        return

    if a.cmd == "consult":
        from .consult import consult
        for t in tasks:
            for ps in t.probe_sets:
                if a.probe_set and ps.stem not in a.probe_set:
                    continue
                if not ps.exists():
                    print(f"[{t.name}] probe set {ps.name} not built yet -- skipped")
                    continue
                for j in t.jobs:
                    if a.model and j.label not in a.model:
                        continue
                    consult(j, ps, t.out_dir(ps) / f"{j.slug}.csv", limit=a.limit, dry_run=a.dry_run,
                            max_workers=a.max_workers)
        return

    if a.cmd == "negtypes":
        from .negtypes import negtypes
        for t in tasks:
            negtypes(t)
        return

    if a.cmd == "report":
        from .report import analyse, write
        for t in tasks:
            for ps in t.probe_sets:
                if a.probe_set and ps.stem not in a.probe_set:
                    continue
                if not ps.exists():
                    print(f"[{t.name}] probe set {ps.name} not built yet -- skipped")
                    continue
                res = analyse(t, ps)
                if res is not None:
                    write(t, ps, *res)


if __name__ == "__main__":
    main()
