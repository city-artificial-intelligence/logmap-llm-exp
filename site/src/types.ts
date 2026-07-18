export interface OracleRow {
  task: string;
  logmap: number;
  llm: number;
  perfect: number;
  err20: number;
  err30: number;
  delta: number;
  ceiling: number;
  capture: number;
}
export interface GenRow {
  generation: string;
  yi: number;
}
export interface LeaderRow {
  model: string;
  f1: number;
  yi: number;
  cost: number;
  reasoning: number;
  fail: number;
  pareto: boolean;
}
export interface CostDriverRow {
  model: string;
  cost: number;
  reasoning: number;
}
export interface LandscapeRow {
  model: string;
  yi: number;
  cost: number;
  t: number;
  panel: boolean;
  pareto: boolean;
  efficiency: boolean;
  poorValue: boolean;
  highlighted: boolean;
}
export interface ShortlistRow {
  tier: string;
  model: string;
  lab: string;
  role: string;
  justification: string;
}
/** merged per-model record used by the explorer and leaderboard */
export interface ModelRow {
  model: string;
  lab: string;
  yi: number;
  cost: number;
  t: number;
  panel: boolean;
  pareto: boolean;
  efficiency: boolean;
  poorValue: boolean;
  f1: number | null;
  reasoning: number | null;
  fail: number | null;
}
/** one candidate model on the pricing landscape (all 66 priced models) */
export interface PricingRow {
  model: string;
  lab: string;
  inputPer1m: number;
  outputPer1m: number;
  /** has a measured oracle F1 (performance-tested), vs price-only */
  tested: boolean;
  f1: number | null;
  yi: number | null;
  panel: boolean;
}
/** one model on the cost / speed / reliability trade-off board (human-mouse, best config) */
export interface TradeoffRow {
  model: string;
  lab: string;
  yi: number;
  f1: number | null;
  cost: number;
  /** average wall-clock processing time per run, seconds */
  proc: number;
  fail: number;
  config: string;
  costPareto: boolean;
  speedPareto: boolean;
}
/** reliability of a model+configuration: how often it fails or has to retry */
export interface ReliabilityRow {
  model: string;
  lab: string;
  config: string;
  fail: number | null;
  retries: number | null;
  /** best/Pareto-optimal, plain reliable, or unreliable (fails/retries a lot) */
  cls: 'unreliable' | 'reliable' | 'pareto';
}
/** one cell of a configuration-sensitivity sweep (model × knob level → metric) */
export interface ConfigCell {
  model: string;
  lab: string;
  /** the knob level (reasoning effort name, prompt id, or numeric level as string) */
  level: string;
  /** numeric ordering for the level (for a sorted x-axis); NaN for nominal levels */
  order: number;
  yi: number | null;
  fail: number | null;
}
export interface ConfigSweeps {
  reasoning: ConfigCell[];
  thinking: ConfigCell[];
  prompt: ConfigCell[];
  fewshot: ConfigCell[];
}
export interface Data {
  oracle: OracleRow[];
  gen: GenRow[];
  leader: LeaderRow[];
  costDrivers: CostDriverRow[];
  landscape: LandscapeRow[];
  shortlist: ShortlistRow[];
  models: ModelRow[];
  pricing: PricingRow[];
  tradeoffs: TradeoffRow[];
  reliability: ReliabilityRow[];
  config: ConfigSweeps;
}

export type Theme = 'light' | 'dark';
