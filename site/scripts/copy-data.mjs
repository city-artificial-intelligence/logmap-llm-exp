// Copy the CSVs that drive the portal into public/data/ so the app is data-driven.
// Primary source: the tidy per-figure CSVs (paper_om_workshop/data), which are derived
// from the raw extracts under analysis/sviatoslav_cost_benefit/data/ by the export script.
// The raw extracts are also copied into public/data/raw/ for transparency / download.
import { cpSync, mkdirSync, existsSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const root = join(here, '..', '..'); // logmap_reconnaissance_mission/
const tidy = join(root, 'paper_om_workshop', 'data');
const raw = join(root, 'analysis', 'sviatoslav_cost_benefit', 'data');
const shared = join(root, 'shared_artefacts'); // consolidated per-model metrics + full pricing list
const outDir = join(here, '..', 'public', 'data');
const rawOut = join(outDir, 'raw');
mkdirSync(outDir, { recursive: true });
mkdirSync(rawOut, { recursive: true });

const tidyFiles = [
  'fig_oracle_value.csv', 'fig_generational.csv', 'fig_pareto.csv',
  'fig_cost_drivers.csv', 'fig_landscape.csv', 'table_shortlist.csv', 'manifest.json',
  // trade-off + configuration figures (cost-efficiency / latency / reliability / tuning knobs)
  'fig_tradeoffs.csv', 'fig_reliability.csv',
  'cfg_reasoning.csv', 'cfg_thinking.csv', 'cfg_prompt.csv', 'cfg_fewshot.csv',
];
// shared_artefacts: the full 66-model pricing list + the consolidated metrics table
// (drives the Pricing landscape view). Price-only models are flagged so the app never
// places them on a performance axis.
const sharedFiles = ['pricing_all.csv', 'model_metrics_all.csv'];
const rawFiles = [
  'leaderboard_by_metric.csv', 'leaderboard_by_cost.csv', 'oasystem_logmap_oracle.csv',
  'consolidated_yi_cost_humanmouse.csv', 'pricing_per_model.csv',
];

// A source is only "missing" (build-breaking) when it is absent AND we have no
// already-materialised copy in public/data/. In a standalone checkout the upstream
// export dirs may not be present, but the plotted CSVs are committed alongside the app.
let copied = 0, kept = 0, miss = 0;
const take = (src, dst, label) => {
  if (existsSync(src)) { cpSync(src, dst); copied++; }
  else if (existsSync(dst)) { kept++; } // authored/committed copy already in place
  else { console.warn(`MISSING (${label}):`, src); miss++; }
};
for (const f of tidyFiles) take(join(tidy, f), join(outDir, f), 'tidy');
for (const f of sharedFiles) take(join(shared, f), join(outDir, f), 'shared');
for (const f of rawFiles) {
  const s = join(raw, f);
  if (existsSync(s)) cpSync(s, join(rawOut, f));
}
console.log(
  `copy-data: ${copied} refreshed from source, ${kept} kept from public/data/ ` +
    `(${miss} missing with no local copy), raw extracts -> public/data/raw/`,
);
if (miss) process.exitCode = 1;
