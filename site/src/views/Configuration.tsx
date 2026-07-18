import { useMemo, useState } from 'react';
import type { EChartsOption } from 'echarts';
import type { ConfigCell, Data, Theme } from '../types';
import { EChart } from '../components/EChart';
import { FigureData } from '../components/FigureData';
import {
  animBase, chartColors, escapeHtml, heatLabelInk, heatRamp, linePalette,
  tickStyle, tooltipBase, FONT_UI, FONT_MONO,
} from '../chart';

type ThinkMetric = 'yi' | 'fail';

/** short model label for a dense y-axis (drop bedrock-style version suffixes) */
const shortModel = (m: string) => m.replace(/-v\d+:\d+$/, '').replace(/^.*\|/, '');

/** distinct levels in cell order (numeric knobs sort by `order`, nominal keep first-seen) */
function levelsOf(cells: ConfigCell[]): string[] {
  const seen = new Map<string, number>();
  for (const c of cells) if (!seen.has(c.level)) seen.set(c.level, c.order);
  const arr = [...seen.entries()];
  const numeric = arr.every(([, o]) => Number.isFinite(o));
  if (numeric) arr.sort((a, b) => a[1] - b[1]);
  return arr.map(([l]) => l);
}

export function Configuration({ data, theme }: { data: Data; theme: Theme }) {
  const c = chartColors(theme);
  const line = linePalette(theme);
  const [thinkMetric, setThinkMetric] = useState<ThinkMetric>('yi');

  /* generic heatmap: models (rows) × knob levels (cols) → metric */
  function heatmap(
    cells: ConfigCell[],
    metric: 'yi' | 'fail',
    opts: { levelLabel?: (l: string) => string; rotate?: number; leftPad?: number } = {},
  ): { option: EChartsOption; nModels: number; nLevels: number } {
    const get = (x: ConfigCell) => (metric === 'yi' ? x.yi : x.fail);
    const active = cells.filter((x) => get(x) != null);
    const levels = levelsOf(active);
    // rank models by mean of the shown metric (best at the top of the heatmap)
    const byModel = new Map<string, ConfigCell[]>();
    for (const x of active) {
      const k = x.model;
      (byModel.get(k) ?? byModel.set(k, []).get(k)!).push(x);
    }
    // rank best-to-weakest on the shown metric — lower is better for fail, higher for YI
    const sign = metric === 'fail' ? -1 : 1;
    const models = [...byModel.keys()].sort((a, b) => {
      const mean = (rows: ConfigCell[]) => rows.reduce((s, r) => s + (get(r) as number), 0) / rows.length;
      return sign * (mean(byModel.get(b)!) - mean(byModel.get(a)!));
    });
    const yData = [...models].reverse(); // category index 0 sits at the bottom

    const vals = active.map((x) => get(x) as number);
    const vmin = metric === 'fail' ? 0 : Math.max(0, Math.floor(Math.min(...vals) * 20) / 20);
    const vmax = metric === 'fail' ? 1 : Math.min(1, Math.ceil(Math.max(...vals) * 20) / 20);
    const span = vmax - vmin || 1;
    const kind = metric === 'fail' ? 'fail' : 'quality';

    // each cell carries its own high-contrast label ink (legible at both ramp ends)
    const points = [];
    for (const x of active) {
      const xi = levels.indexOf(x.level);
      const yi = yData.indexOf(x.model);
      if (xi < 0 || yi < 0) continue;
      const v = get(x) as number;
      points.push({ value: [xi, yi, v], label: { color: heatLabelInk((v - vmin) / span, theme, kind) } });
    }
    const fmt = (v: number) => (metric === 'fail' ? `${Math.round(v * 100)}%` : v.toFixed(2).replace(/^0\./, '.'));

    const option: EChartsOption = {
      ...animBase(),
      textStyle: { fontFamily: FONT_UI },
      grid: { left: opts.leftPad ?? 150, right: 20, top: 12, bottom: (opts.rotate ? 92 : 48) + 30 },
      tooltip: {
        ...tooltipBase(c),
        formatter: (p: unknown) => {
          const o = p as { value: [number, number, number] };
          const [xi, yi, v] = o.value;
          const mono = (s: string) => `<span style="font-family:${FONT_MONO};font-size:11.5px">${s}</span>`;
          return [
            `<b>${escapeHtml(yData[yi])}</b>`,
            `${escapeHtml(opts.levelLabel ? opts.levelLabel(levels[xi]) : levels[xi])}`,
            `${metric === 'yi' ? 'YI' : 'fail rate'} ${mono(`<b>${metric === 'fail' ? `${(v * 100).toFixed(1)}%` : v.toFixed(3)}</b>`)}`,
          ].join('<br/>');
        },
      },
      xAxis: {
        type: 'category',
        data: levels.map((l) => (opts.levelLabel ? opts.levelLabel(l) : l)),
        splitArea: { show: true, areaStyle: { color: ['transparent'] } },
        axisLine: { lineStyle: { color: c.axis } },
        axisTick: { show: false },
        axisLabel: { ...tickStyle(c), rotate: opts.rotate ?? 0, interval: 0 },
      },
      yAxis: {
        type: 'category',
        data: yData.map(shortModel),
        splitArea: { show: true, areaStyle: { color: ['transparent'] } },
        axisLine: { lineStyle: { color: c.axis } },
        axisTick: { show: false },
        axisLabel: { ...tickStyle(c), fontSize: 10.5 },
      },
      visualMap: {
        min: vmin,
        max: vmax,
        calculable: true,
        orient: 'horizontal',
        left: 'center',
        bottom: 4,
        itemWidth: 12,
        itemHeight: 120,
        inRange: { color: heatRamp(theme, metric === 'fail' ? 'fail' : 'quality') },
        textStyle: { color: c.muted, fontSize: 10, fontFamily: FONT_MONO },
        text: [metric === 'fail' ? 'fails' : 'better', metric === 'fail' ? 'clean' : 'weaker'],
        formatter: (v: unknown) => (metric === 'fail' ? `${Math.round(Number(v) * 100)}%` : Number(v).toFixed(2)),
      },
      series: [
        {
          type: 'heatmap',
          data: points,
          label: {
            show: true,
            fontSize: 10,
            fontFamily: FONT_MONO,
            formatter: (p: unknown) => fmt((p as { value: [number, number, number] }).value[2]),
          },
          itemStyle: { borderColor: c.surface, borderWidth: 2 },
          emphasis: { itemStyle: { borderColor: c.panelRing, borderWidth: 1 } },
        },
      ],
    };
    return { option, nModels: models.length, nLevels: levels.length };
  }

  const reasoning = useMemo(
    () => heatmap(data.config.reasoning, 'yi', { leftPad: 205 }),
    [data.config.reasoning, c, theme],
  );
  const thinking = useMemo(
    () => heatmap(data.config.thinking, thinkMetric, { levelLabel: (l) => `${l} tok`, leftPad: 165 }),
    [data.config.thinking, thinkMetric, c, theme],
  );
  const prompt = useMemo(
    () => heatmap(data.config.prompt, 'yi', { rotate: 24, leftPad: 210, levelLabel: (l) => l.replace(/_/g, ' ') }),
    [data.config.prompt, c, theme],
  );

  /* Figure 6 — few-shot as a trend line (models with the richest sweeps) */
  const fewshot = useMemo(() => {
    const byModel = new Map<string, ConfigCell[]>();
    for (const x of data.config.fewshot) {
      if (x.yi == null) continue;
      (byModel.get(x.model) ?? byModel.set(x.model, []).get(x.model)!).push(x);
    }
    const chosen = [...byModel.entries()]
      .map(([m, rows]) => ({ m, rows: [...rows].sort((a, b) => a.order - b.order) }))
      .sort((a, b) => b.rows.length - a.rows.length)
      .slice(0, line.length); // one distinguishable colour per line
    const maxN = Math.max(...data.config.fewshot.map((x) => x.order).filter(Number.isFinite));
    const option: EChartsOption = {
      ...animBase(),
      textStyle: { fontFamily: FONT_UI },
      legend: {
        type: 'scroll', top: 0, left: 0, icon: 'roundRect', itemWidth: 14, itemHeight: 4, itemGap: 14,
        textStyle: { color: c.text2, fontSize: 11, fontFamily: FONT_UI },
      },
      grid: { left: 48, right: 20, top: 44, bottom: 44 },
      tooltip: {
        trigger: 'axis',
        ...tooltipBase(c),
        valueFormatter: (v) => (typeof v === 'number' ? v.toFixed(3) : String(v)),
      },
      xAxis: {
        type: 'value',
        min: 0,
        max: maxN,
        name: '# few-shot examples',
        nameLocation: 'middle',
        nameGap: 28,
        axisLine: { lineStyle: { color: c.axis } },
        axisTick: { show: false },
        axisLabel: tickStyle(c),
        splitLine: { lineStyle: { color: c.split, width: 1 } },
        nameTextStyle: { color: c.text2, fontSize: 11, fontFamily: FONT_UI },
      },
      yAxis: {
        type: 'value',
        name: 'Mean oracle YI',
        axisLine: { show: false },
        splitLine: { lineStyle: { color: c.split, width: 1 } },
        axisLabel: tickStyle(c),
        nameTextStyle: { color: c.text2, fontSize: 11, fontFamily: FONT_UI, align: 'left' },
      },
      series: chosen.map((s, i) => ({
        name: shortModel(s.m),
        type: 'line' as const,
        showSymbol: true,
        symbolSize: 5,
        smooth: false,
        data: s.rows.map((r) => [r.order, r.yi as number]),
        lineStyle: { width: 2, color: line[i % line.length] },
        itemStyle: { color: line[i % line.length] },
      })),
    };
    return { option, chosen };
  }, [data.config.fewshot, c, line, theme]);

  return (
    <div className="stack">
      <section className="hero">
        <span className="kicker">Figures 6–9 · configuration sensitivity</span>
        <h1>How much do the knobs matter?</h1>
        <p className="lead">
          Beyond which model to pick, each candidate exposes tuning knobs — reasoning effort,
          thinking budget, prompt template, few-shot examples. These sweeps show how far each knob
          moves oracle quality (Youden&apos;s J) on human-mouse, so effort goes where it pays off.
        </p>
      </section>

      <section className="stack">

        <div className="card">
          <div className="card-head">
            <div>
              <span className="figure-kicker">Figure 6</span>
              <h2>Few-shot examples → quality</h2>
            </div>
            <span className="meta">richest {fewshot.chosen.length} sweeps</span>
          </div>
          <EChart option={fewshot.option} height={330} ariaLabel="Mean oracle YI versus number of few-shot examples per model; data table below" />
          <p className="caption">
            More examples rarely help past a handful: most curves plateau or drift down after ~3–5
            shots. Spending the context window on demonstrations is usually not worth it.
          </p>
          <FigureData
            summary="View Figure 6 data"
            columns={['Model', '# shots', 'Mean YI']}
            numeric={[1, 2]}
            rows={data.config.fewshot
              .filter((r) => r.yi != null)
              .map((r) => [<code className="model-id" key={`${r.model}-${r.level}`}>{r.model}</code>, r.level, (r.yi as number).toFixed(3)])}
          />
        </div>

      </section>

      <section className="stack">

        <div className="card">
          <div className="card-head">
            <div>
              <span className="figure-kicker">Figure 7</span>
              <h2>Reasoning effort → quality</h2>
            </div>
            <span className="meta">{reasoning.nModels} models</span>
          </div>
          <EChart option={reasoning.option} height={300} ariaLabel="Youden's J by reasoning-effort level per model; data table below" />
          <p className="caption">
            Turning reasoning up helps some models and hurts others — there is no universal “more is
            better”. Each model has its own sweet spot.
          </p>
          <FigureData
            summary="View Figure 7 data"
            columns={['Model', 'Effort', 'YI']}
            numeric={[2]}
            rows={data.config.reasoning
              .filter((r) => r.yi != null)
              .map((r) => [<code className="model-id" key={`${r.model}-${r.level}`}>{r.model}</code>, r.level, (r.yi as number).toFixed(3)])}
          />
        </div>

        <div className="card">
          <div className="card-head">
            <div>
              <span className="figure-kicker">Figure 8 · <em>Interactive</em></span>
              <h2>Thinking budget → quality &amp; reliability</h2>
            </div>
          </div>
          <div className="controls">
            <div className="control">
              <span className="control-label" id="think-metric">Cell metric</span>
              <div className="segmented" role="group" aria-labelledby="think-metric">
                <button aria-pressed={thinkMetric === 'yi'} onClick={() => setThinkMetric('yi')}>Youden&apos;s J</button>
                <button aria-pressed={thinkMetric === 'fail'} onClick={() => setThinkMetric('fail')}>Fail rate</button>
              </div>
            </div>
          </div>
          <EChart
            option={thinking.option}
            height={300}
            ariaLabel="Youden's J or failure rate by thinking-token budget per model; data table below"
          />
          <p className="caption">
            More thinking tokens can lift quality, but for several models a <em>zero</em> budget
            flips them into constant failure — the reliability view (fail rate) exposes those cliffs.
          </p>
          <FigureData
            summary="View Figure 8 data"
            columns={['Model', 'Budget (tok)', 'YI', 'Fail rate']}
            numeric={[1, 2, 3]}
            rows={data.config.thinking.map((r) => [
              <code className="model-id" key={`${r.model}-${r.level}`}>{r.model}</code>,
              r.level,
              r.yi != null ? (r.yi as number).toFixed(3) : '—',
              r.fail != null ? `${((r.fail as number) * 100).toFixed(1)}%` : '—',
            ])}
          />
        </div>

        <div className="card">
          <div className="card-head">
            <div>
              <span className="figure-kicker">Figure 9</span>
              <h2>Prompt template → quality</h2>
            </div>
            <span className="meta">baseline models</span>
          </div>
          <EChart option={prompt.option} height={330} ariaLabel="Youden's J by prompt template per baseline model; data table below" />
          <p className="caption">
            Prompt wording matters most on the weaker baselines and washes out on the strong ones —
            adding ontological context or synonyms helps unevenly, so it is not a free win.
          </p>
          <FigureData
            summary="View Figure 9 data"
            columns={['Model', 'Prompt', 'YI']}
            numeric={[2]}
            rows={data.config.prompt
              .filter((r) => r.yi != null)
              .map((r) => [<code className="model-id" key={`${r.model}-${r.level}`}>{r.model}</code>, r.level.replace(/_/g, ' '), (r.yi as number).toFixed(3)])}
          />
        </div>

      </section>

      <p className="footnote">
        Configuration sweeps from the human-mouse study. Blank cells were not measured for that
        model. Values are oracle Youden&apos;s J unless the failure-rate view is selected; heatmap
        rows are ordered best-to-weakest on the shown metric.
      </p>
    </div>
  );
}
