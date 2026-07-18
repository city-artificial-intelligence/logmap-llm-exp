import Papa from 'papaparse';
import type {
  Data, OracleRow, GenRow, LeaderRow, CostDriverRow, LandscapeRow, ShortlistRow, ModelRow, PricingRow,
  TradeoffRow, ReliabilityRow, ConfigCell,
} from './types';

const num = (v: unknown): number => {
  const n = typeof v === 'number' ? v : parseFloat(String(v));
  return Number.isFinite(n) ? n : NaN;
};
/** parse a numeric field that may be blank (missing measurement) into number | null */
const numN = (v: unknown): number | null => {
  const s = String(v ?? '').trim();
  if (s === '') return null;
  const n = parseFloat(s);
  return Number.isFinite(n) ? n : null;
};
const bool = (v: unknown): boolean => String(v).trim().toLowerCase() === 'true';

async function csv(url: string): Promise<Record<string, string>[]> {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Failed to load ${url} (${res.status})`);
  const text = await res.text();
  const parsed = Papa.parse<Record<string, string>>(text, {
    header: true,
    skipEmptyLines: true,
    transformHeader: (h) => h.trim(),
  });
  if (parsed.errors.length) {
    // tolerate minor parse warnings but surface hard failures
    const fatal = parsed.errors.find((e) => e.type === 'Delimiter');
    if (fatal) throw new Error(`Parse error in ${url}: ${fatal.message}`);
  }
  return parsed.data;
}

/** infer the developer lab from a model id (for grouping / colour) */
export function labOf(model: string): string {
  const m = model.toLowerCase();
  if (m.startsWith('gemini') || m.startsWith('gemma')) return 'Google';
  if (m.startsWith('deepseek')) return 'DeepSeek';
  if (m.startsWith('claude')) return 'Anthropic';
  if (m.startsWith('gpt') || m.startsWith('o1') || m.startsWith('o3')) return 'OpenAI';
  if (m.startsWith('qwen')) return 'Alibaba';
  if (m.startsWith('mistral') || m.startsWith('ministral')) return 'Mistral';
  if (m.startsWith('llama')) return 'Meta';
  if (m.startsWith('grok')) return 'xAI';
  if (m.startsWith('glm')) return 'Zhipu';
  if (m.startsWith('nova')) return 'Amazon';
  return 'Other';
}

export async function loadData(base: string): Promise<Data> {
  const at = (f: string) => `${base}data/${f}`;
  const [
    rawOracle, rawGen, rawLeader, rawCost, rawLand, rawShort, rawPricing, rawMetrics,
    rawTradeoff, rawReli, rawReason, rawThink, rawPrompt, rawFewshot,
  ] = await Promise.all([
    csv(at('fig_oracle_value.csv')),
    csv(at('fig_generational.csv')),
    csv(at('fig_pareto.csv')),
    csv(at('fig_cost_drivers.csv')),
    csv(at('fig_landscape.csv')),
    csv(at('table_shortlist.csv')),
    csv(at('pricing_all.csv')),
    csv(at('model_metrics_all.csv')),
    csv(at('fig_tradeoffs.csv')),
    csv(at('fig_reliability.csv')),
    csv(at('cfg_reasoning.csv')),
    csv(at('cfg_thinking.csv')),
    csv(at('cfg_prompt.csv')),
    csv(at('cfg_fewshot.csv')),
  ]);

  const oracle: OracleRow[] = rawOracle.map((r) => ({
    task: r.task,
    logmap: num(r.logmap_f1),
    llm: num(r.llm_gf25_f1),
    perfect: num(r.perfect_f1),
    err20: num(r.sim_err20_f1),
    err30: num(r.sim_err30_f1),
    delta: num(r.delta_llm),
    ceiling: num(r.ceiling),
    capture: num(r.capture_frac),
  }));
  const gen: GenRow[] = rawGen.map((r) => ({ generation: r.generation, yi: num(r.mean_yi) }));
  const leader: LeaderRow[] = rawLeader.map((r) => ({
    model: r.model,
    f1: num(r.f1),
    yi: num(r.yi),
    cost: num(r.cost_usd_per_run),
    reasoning: num(r.reasoning_share),
    fail: num(r.fail_rate),
    pareto: bool(r.on_pareto_frontier),
  }));
  const costDrivers: CostDriverRow[] = rawCost.map((r) => ({
    model: r.model,
    cost: num(r.cost_usd_per_run),
    reasoning: num(r.reasoning_share),
  }));
  const landscape: LandscapeRow[] = rawLand.map((r) => ({
    model: r.model,
    yi: num(r.yi),
    cost: num(r.cost_usd_per_run),
    t: num(r.spectrum_t),
    panel: bool(r.is_selected_panel),
    pareto: bool(r.on_pareto_frontier),
    efficiency: bool(r.efficiency_outlier),
    poorValue: bool(r.poor_value_outlier),
    highlighted: bool(r.is_highlighted),
  }));
  // strip any residual LaTeX escapes (\$, \,, \%, ~) for clean web display
  const deLatex = (s: string) =>
    s.replace(/\\([$%&_#{}])/g, '$1').replace(/\\,/g, ' ').replace(/~/g, ' ').trim();
  const shortlist: ShortlistRow[] = rawShort.map((r) => ({
    tier: r.tier,
    model: r.model,
    lab: r.lab,
    role: deLatex(r.role),
    justification: deLatex(r.justification),
  }));

  // merge landscape (18, has YI + flags) with the leaderboard (has F1/reasoning/fail)
  const byModel = new Map(leader.map((l) => [l.model.toLowerCase(), l]));
  const models: ModelRow[] = landscape.map((l) => {
    const lb = byModel.get(l.model.toLowerCase());
    return {
      model: l.model,
      lab: labOf(l.model),
      yi: l.yi,
      cost: l.cost,
      t: l.t,
      panel: l.panel,
      pareto: l.pareto,
      efficiency: l.efficiency,
      poorValue: l.poorValue,
      f1: lb ? lb.f1 : null,
      reasoning: lb ? lb.reasoning : null,
      fail: lb ? lb.fail : null,
    };
  });

  // Pricing landscape (all priced candidates). Join measured F1/YI + panel flag from
  // model_metrics_all so tested models can be emphasised and their score shown on hover.
  const metricByModel = new Map(rawMetrics.map((r) => [r.model.toLowerCase(), r]));
  const pricing: PricingRow[] = rawPricing
    .map((r) => {
      const met = metricByModel.get(r.model.toLowerCase());
      return {
        model: r.model,
        lab: r.lab || labOf(r.model),
        inputPer1m: num(r.input_usd_per_1m),
        outputPer1m: num(r.output_usd_per_1m),
        tested: bool(r.has_f1),
        f1: met && bool(met.has_f1) && Number.isFinite(num(met.f1)) ? num(met.f1) : null,
        yi: met && bool(met.has_yi) && Number.isFinite(num(met.yi)) ? num(met.yi) : null,
        panel: met ? bool(met.selected_panel) : false,
      };
    })
    // only rows with both price coordinates belong on the input-vs-output plot
    .filter((p) => Number.isFinite(p.inputPer1m) && Number.isFinite(p.outputPer1m) && p.inputPer1m > 0 && p.outputPer1m > 0);

  // Cost / speed / reliability trade-off board (human-mouse, best config per model).
  const tradeoffs: TradeoffRow[] = rawTradeoff.map((r) => ({
    model: r.model,
    lab: r.lab || labOf(r.model),
    yi: num(r.yi),
    f1: numN(r.f1),
    cost: num(r.cost_usd_per_run),
    proc: num(r.proc_time_s),
    fail: num(r.fail_rate),
    config: r.config || '',
    costPareto: bool(r.on_cost_pareto),
    speedPareto: bool(r.on_speed_pareto),
  }));

  const reliability: ReliabilityRow[] = rawReli.map((r) => ({
    model: r.model,
    lab: r.lab || labOf(r.model),
    config: r.config || '',
    fail: numN(r.fail_rate),
    retries: numN(r.retries),
    cls: r.cls === 'unreliable' || r.cls === 'pareto' ? r.cls : 'reliable',
  }));

  // Configuration-sensitivity sweeps (each cell = one knob level for one model).
  const reasoning: ConfigCell[] = rawReason.map((r) => ({
    model: r.model, lab: r.lab || labOf(r.model),
    level: r.effort, order: ['minimal', 'low', 'medium', 'high'].indexOf(r.effort),
    yi: numN(r.yi), fail: null,
  }));
  const thinking: ConfigCell[] = rawThink.map((r) => ({
    model: r.model, lab: r.lab || labOf(r.model),
    level: r.budget, order: num(r.budget),
    yi: numN(r.yi), fail: numN(r.fail),
  }));
  const prompt: ConfigCell[] = rawPrompt.map((r) => ({
    model: r.model, lab: r.lab || labOf(r.model),
    level: r.prompt, order: NaN,
    yi: numN(r.yi), fail: null,
  }));
  const fewshot: ConfigCell[] = rawFewshot.map((r) => ({
    model: r.model, lab: r.lab || labOf(r.model),
    level: r.n, order: num(r.n),
    yi: numN(r.yi), fail: null,
  }));

  return {
    oracle, gen, leader, costDrivers, landscape, shortlist, models, pricing,
    tradeoffs, reliability, config: { reasoning, thinking, prompt, fewshot },
  };
}
