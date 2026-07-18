# LogMapLLM Oracle — Cost/Benefit Explorer

An interactive web portal that showcases the LogMapLLM LLM-oracle cost/benefit data. It answers
one question — *which LLM should validate LogMap's uncertain mappings?* — across six views, all
driven by the CSVs extracted under `../analysis/sviatoslav_cost_benefit/data/`.

## Views (in tab order)
- **Overview** — de-boxed hero + kicker, a 4-cell headline stat strip (100× cost for ~2 pt of F1;
  oracle helps 7/9 tasks; generation 2.65×; reasoning 72–95% of cost), the selected 9-model panel
  (Table 1), and mini charts (generation, cost drivers — Figures 1–2).
- **Leaderboard** (Table 2) — sortable, searchable ("/" focuses the filter) per-model table with a
  YI micro-meter, rank column, and panel / Pareto / outlier badges.
- **Trade-offs** (Figures 3–5) — the *other* axes of the choice, re-scored on the broader
  human-mouse field (32 models, best config each): quality vs **latency** (avg processing time on a
  log axis, bubble size + hue = cost, with the speed–quality frontier; interactive metric / scale /
  lab / frontier controls), **cost-efficiency** ($ per YI point and per F1 point as an honest
  log-axis dot plot), and **reliability** (failure rate / retries-per-call for the configurations
  that don't answer cleanly). A 4-cell trade-off stat strip up top.
- **Configuration** (Figures 6–9) — how far the tuning knobs move oracle quality: **few-shot count
  → mean YI** trend lines for the richest sweeps, then **reasoning effort**, **thinking budget**
  (YI *and* fail-rate toggle), and **prompt template** as sequential iris heatmaps (each cell
  prints its value with contrast-aware ink).
- **Value** (Figures 10–11) — per-task global F1 as a grouped **dot plot** (position, not bar
  length, encodes value — honest on the zoomed 0.55–0.95 window) for LogMap / +LLM / +perfect with
  optional simulated 20%/30% oracles, plus the capture-ratio chart with polarity colouring.
- **Pricing** (Figure 12) — the full candidate field: input vs output token price ($/1M) for all 66
  priced models on log–log axes. The ~24 with a measured oracle score are emphasised (iris, with the
  selected panel ringed); the rest are shown in grey as *price-only* and are deliberately **never**
  placed on a quality axis (they have no performance number to plot). A checkbox hides the price-only
  set to focus on the tested subset.

## Stack & standards
Vite + React 18 + TypeScript (strict) + ECharts. No UI framework or CSS library — an "Iris Console"
design-token stylesheet (zinc neutrals, hairline borders, one iris accent) with light/dark theming
(pre-paint theme stamp in `app.html` + `prefers-color-scheme` fallback + a persisted toggle),
self-hosted fonts (`@fontsource-variable/inter`, `@fontsource-variable/jetbrains-mono` — no CDN),
numbered FIGURE/TABLE kickers with captions, skeleton loading, responsive grid, semantic landmarks,
keyboard-operable tabs/controls, `aria-*` labels, a skip link, focusable scroll regions,
hash-routed deep links per view (`#leaderboard`, `#tradeoffs`, …) with document-title sync, and
`prefers-reduced-motion` support (CSS *and* canvas chart animation). The chart palette is CVD-validated (Machado) against both card surfaces —
see the notes in `src/chart.ts`. Vendor code is split into cached `echarts` / `react` chunks;
`base: './'` makes the built site hostable from any path.

## Data flow (driven by the CSVs)
`npm run predev`/`prebuild` runs `scripts/copy-data.mjs`, which copies the tidy per-figure CSVs from
`../paper_om_workshop/data/` (derived from the raw extracts in `../analysis/sviatoslav_cost_benefit/data/`
by that project's export script) plus the consolidated metrics + full pricing list from
`../shared_artefacts/` (`pricing_all.csv`, `model_metrics_all.csv` — the Pricing view's source, with
`has_f1` flagging which of the 66 priced models are performance-tested) into `public/data/`. The app
fetches and parses them at runtime with PapaParse (`src/data.ts`) — so dropping in updated CSVs and
reloading updates the site, no code change.

The Trade-offs and Configuration views add six more tidy CSVs (`fig_tradeoffs.csv`,
`fig_reliability.csv`, `cfg_reasoning.csv`, `cfg_thinking.csv`, `cfg_prompt.csv`, `cfg_fewshot.csv`),
extracted from the human-mouse study's `tradeoffs` / `report` / `model_explorer` HTML exports
(cost/speed/reliability charts joined to the per-config master table on `model + cost + yi`, which
recovers F1). Each is documented in `manifest.json`. `copy-data.mjs` refreshes any file that still
has an upstream source and otherwise keeps the copy already in `public/data/`, so the site builds
standalone.

**A note on measurement basis.** The performance plots (Value / Leaderboard) use the
curated 18-model set that has a *measured* human-mouse `$/run` and oracle score. The extra models in
`shared_artefacts` that only have estimated costs (or price alone) are surfaced honestly on the
Pricing view rather than mixed onto the measured-cost performance axis, which would compare
inconsistent bases.

## Run it
```bash
cd demo_portal
npm install
npm run dev        # http://localhost:5173  (copies data first)
# production:
npm run build      # typecheck + bundle -> dist/
npm run preview    # serve the build at http://localhost:4173
```

## Verify (headless)
```bash
npm run build && npm run smoke   # loads every view in headless Chrome, fails on any console/page
                                 # error, writes 12 full-page screenshots/*.png (6 light + 6 dark)
```

## Deploy
`npm run build` produces a static `dist/`. Because `base` is relative and the CSVs live in
`public/data/`, the folder can be served by any static host (GitHub Pages, S3, nginx, `python -m http.server`).

**GitHub Pages (automated):** `.github/workflows/deploy.yml` builds and publishes `dist/` on every
push to `main` (and on manual dispatch). One-time setup after pushing the repo to GitHub:
Settings → Pages → Source = **GitHub Actions**. The workflow assumes this folder is the repository
root — if it's pushed as a subdirectory of a larger repo, move `.github/` to the repo root and
point the job's `working-directory` / artifact `path` at the site folder.

## Structure
```
src/
  App.tsx              shell: theme, tab state, data loading, layout
  data.ts              fetch + parse the CSVs into typed records
  types.ts             data + view types
  chart.ts             theme-aware chart colours, spectrum interpolation, formatters
  components/EChart.tsx self-managing ECharts wrapper (init / setOption / resize / dispose)
  views/               one per tab: Overview, Leaderboard, Tradeoffs, Configuration,
                       OracleValue ("Value"), PricingLandscape
scripts/
  copy-data.mjs        pull the driving CSVs into public/data/
  smoke.mjs            headless render test + screenshots
```

## Notes / possible next steps
- This is the **data-explorer** component of the wider demonstration; it can sit alongside the planned
  live-pipeline / three.js visualisation.
- ECharts is registered modularly via `echarts/core` in `src/components/EChart.tsx` (only the
  chart/component types the views use ship — ~581 kB / 194 kB gzip vs ~1 MB / 343 kB whole). If a view
  adds a new chart or component type, register it there.
- Lint config is intentionally omitted (strict `tsc` is the quality gate); add ESLint if desired.
