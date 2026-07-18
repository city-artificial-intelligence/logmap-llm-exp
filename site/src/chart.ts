import type { Theme } from './types';

/* Fonts (self-hosted via @fontsource, loaded in main.tsx) */
export const FONT_UI = "'Inter Variable', 'Inter', system-ui, sans-serif";
export const FONT_MONO = "'JetBrains Mono Variable', ui-monospace, 'SF Mono', Menlo, monospace";

/* -----------------------------------------------------------------------------
   Palette — validated with the Machado-CVD checker against the real card
   surfaces (light #ffffff, dark #17171b):
   - 8-slot categorical: light worst adjacent ΔE 24.2 (PASS); dark worst 10.3
     (floor band, green↔amber — never plotted adjacently here; every
     multi-series chart ships a legend + surface gaps as secondary encoding).
   - 5-series dot-plot set (all-pairs, since the dots cluster): worst ΔE 14.6
     light / 19.8 dark, all marks ≥3:1 on their surface. The baseline grey
     intentionally fails the chroma floor: "no oracle" reads as colorless by
     design, identified by legend + fixed cluster position.
   Slot 1 (iris) deliberately equals the UI accent: "our oracle" owns the
   product color. Light slots 3 (amber) & 7 (magenta) are sub-3:1 relief-band
   fills — never use them for text or single-encoding charts.
   ----------------------------------------------------------------------------- */
const CATEGORY_LIGHT = ['#5e6ad2', '#1a9e74', '#eda100', '#008300', '#0e8bd1', '#e34948', '#e87ba4', '#eb6834'];
const CATEGORY_DARK = ['#7b87e8', '#1ea578', '#c98500', '#008300', '#2b91d4', '#e66767', '#d55181', '#d95926'];

export function category(theme: Theme): string[] {
  return theme === 'dark' ? CATEGORY_DARK : CATEGORY_LIGHT;
}

/** the named series roles used across the views */
export function seriesColors(theme: Theme) {
  const cat = category(theme);
  return {
    /** "LogMap, no oracle" — deliberately recessive reference series */
    baseline: theme === 'dark' ? '#6e6e78' : '#85858f',
    /** "+ LLM oracle" — slot 1, the product accent */
    llm: cat[0],
    /** "+ perfect oracle" ceiling — slot 2 */
    perfect: cat[1],
    /** simulated-error oracles — one amber hue, two ordinal lightness steps */
    sim20: '#c98500',
    sim30: theme === 'dark' ? '#8f5e00' : '#8a5f00',
  };
}

export interface ChartColors {
  text: string;
  text2: string;
  muted: string;
  axis: string;
  split: string;
  surface: string;
  tipBg: string;
  tipBorder: string;
  tipShadow: string;
  ceiling: string;
  panelRing: string;
  frontier: string;
}

export function chartColors(theme: Theme): ChartColors {
  return theme === 'dark'
    ? {
        text: '#ededf0', text2: '#a1a1aa', muted: '#8f8f98',
        axis: '#34343c', split: '#222227', surface: '#17171b',
        tipBg: '#26262c', tipBorder: '#3f3f49',
        tipShadow: '0 8px 24px rgba(0, 0, 0, 0.55)',
        ceiling: '#75757f', panelRing: '#ededf0', frontier: '#6e6e78',
      }
    : {
        text: '#18181b', text2: '#52525b', muted: '#6a6a73',
        axis: '#d4d4d8', split: '#eeeef0', surface: '#ffffff',
        tipBg: '#ffffff', tipBorder: '#e4e4e7',
        tipShadow: '0 4px 16px rgba(9, 9, 11, 0.12)',
        ceiling: '#85858f', panelRing: '#18181b', frontier: '#85858f',
      };
}

/** status red — reserved for "this is bad" (never a series identity) */
export function statusBad(theme: Theme): string {
  return theme === 'dark' ? '#f87171' : '#b91c1c';
}

/* Diverging cost-performance spectrum: RdBu poles + a VISIBLE neutral gray
   midpoint (the old #cfd3d8 vanished on white and glowed in dark). */
export function spectrumStops(theme: Theme): [string, string, string] {
  // midpoints hold >= 3:1 non-text contrast on their card surface while staying neutral
  return theme === 'dark' ? ['#4f94d4', '#74747e', '#d95757'] : ['#2166ac', '#8c8c94', '#b2182b'];
}

/** continuous colour along the diverging spectrum for t in [0,1] */
export function spectrumColor(t: number, theme: Theme): string {
  const hex = (h: string): number[] => [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16));
  const stops = spectrumStops(theme).map(hex);
  const x = Math.max(0, Math.min(1, t));
  const seg = x < 0.5 ? 0 : 1;
  const local = (x - seg * 0.5) / 0.5;
  const a = stops[seg];
  const b = stops[seg + 1];
  const mix = (i: number) => Math.round(a[i] + (b[i] - a[i]) * local);
  return `rgb(${mix(0)}, ${mix(1)}, ${mix(2)})`;
}

/** shared ECharts tooltip base — surface card, hairline border, soft pop shadow */
export function tooltipBase(c: ChartColors) {
  return {
    backgroundColor: c.tipBg,
    borderColor: c.tipBorder,
    borderWidth: 1,
    borderRadius: 8,
    padding: [10, 12] as [number, number],
    textStyle: { color: c.text, fontSize: 12, fontFamily: FONT_UI },
    extraCssText: `box-shadow: ${c.tipShadow};`,
  };
}

/** escape CSV-sourced strings before interpolating into tooltip HTML */
export function escapeHtml(s: string): string {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

/** shared axis-label style: mono ticks in muted ink */
export function tickStyle(c: ChartColors) {
  return { color: c.muted, fontSize: 11, fontFamily: FONT_MONO };
}

export function prefersReducedMotion(): boolean {
  return typeof window !== 'undefined' && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
}

/** animation base for every option — canvas ignores the CSS reduced-motion rule */
export function animBase() {
  const reduce = prefersReducedMotion();
  return reduce
    ? { animation: false as const }
    : { animationDuration: 300, animationDurationUpdate: 220, animationEasing: 'cubicOut' as const };
}

/* Sequential heatmap ramps (config-sweep cells). Single-hue magnitude scales,
   tuned to hold contrast against each card surface; every cell also prints its
   value, so colour is a secondary (never sole) encoding. 'quality' = iris (more
   is better), 'fail' = status red (more is worse). Low→high order. */
export function heatRamp(theme: Theme, kind: 'quality' | 'fail'): string[] {
  if (kind === 'fail') {
    return theme === 'dark'
      ? ['#211a1c', '#5c2b2b', '#9a3d3d', '#cf5555', '#f6a3a3']
      : ['#f7ecec', '#e6b3b3', '#d47a7a', '#c04141', '#a01414'];
  }
  return theme === 'dark'
    ? ['#20222c', '#33375c', '#4a538f', '#6470c4', '#9aa4ee']
    : ['#eef0fb', '#c7cdf1', '#9aa3e6', '#6d78d9', '#4450b4'];
}

/** interpolate an N-stop hex ramp at t in [0,1] -> [r,g,b] */
function rampRgb(stops: string[], t: number): [number, number, number] {
  const hex = (h: string): number[] => [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16));
  const x = Math.max(0, Math.min(1, t)) * (stops.length - 1);
  const i = Math.min(stops.length - 2, Math.floor(x));
  const f = x - i;
  const a = hex(stops[i]);
  const b = hex(stops[i + 1]);
  return [0, 1, 2].map((k) => Math.round(a[k] + (b[k] - a[k]) * f)) as [number, number, number];
}

/** high-contrast ink (near-black or near-white) for a value label printed on a heatmap cell,
    chosen from the cell's own interpolated colour so it stays legible at both ramp ends. */
export function heatLabelInk(t: number, theme: Theme, kind: 'quality' | 'fail'): string {
  const [r, g, b] = rampRgb(heatRamp(theme, kind), t);
  const luma = (0.299 * r + 0.587 * g + 0.114 * b) / 255;
  return luma > 0.62 ? '#141417' : '#ffffff';
}

/** distinguishable qualitative line palette, ≥3:1 on both card surfaces in both themes
    (avoids the two sub-3:1 light categorical slots, which fail as single-encoding lines). */
export function linePalette(theme: Theme): string[] {
  return theme === 'dark'
    ? ['#7b87e8', '#1ea578', '#2b91d4', '#e66767', '#c98500', '#c266a0', '#3ea03e']
    : ['#5e6ad2', '#1a9e74', '#0e8bd1', '#d83a39', '#9a6a00', '#b0407e', '#046a34'];
}

/** processing time / latency: seconds, trimmed */
export const fmtSec = (v: number): string => (v < 10 ? `${v.toFixed(1)}s` : `${Math.round(v)}s`);

export const fmtUsd = (v: number): string =>
  v < 0.1 ? `$${v.toFixed(3)}` : v < 10 ? `$${v.toFixed(2)}` : `$${v.toFixed(1)}`;
/** axis ticks: one consistent trimmed format ($0.001 · $0.01 · $0.1 · $1 · $10) */
export const fmtUsdTick = (v: number): string => `$${Number(v.toPrecision(2))}`;
/** price per 1M tokens, trimmed of trailing zeros */
export const fmtPer1m = (v: number): string => `$${Number(v.toFixed(3))}`;
export const fmtPct = (v: number): string => `${Math.round(v * 100)}%`;
