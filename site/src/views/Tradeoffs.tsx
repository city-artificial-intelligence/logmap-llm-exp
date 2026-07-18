import { useMemo, useState, type CSSProperties } from 'react';
import type { EChartsOption } from 'echarts';
import type { Data, TradeoffRow, ReliabilityRow, Theme } from '../types';
import { EChart } from '../components/EChart';
import { FigureData } from '../components/FigureData';
import {
  animBase, category, chartColors, escapeHtml, fmtSec, fmtUsd, spectrumColor, spectrumStops,
  statusBad, tickStyle, tooltipBase, FONT_UI, FONT_MONO,
} from '../chart';

type Metric = 'yi' | 'f1';
type Reli = 'fail' | 'retries';

const metricLabel = (m: Metric) => (m === 'yi' ? "Youden's J" : 'Oracle F1');

/** short config annotation ("base" is the norm and shown dim) */
function cfgTag(config: string): string {
  return config && config !== 'base' ? config : '';
}

/** small square colour key used in the reliability key-bar */
const swatch = (color: string): CSSProperties => ({
  display: 'inline-block', width: 9, height: 9, borderRadius: 2,
  background: color, verticalAlign: 'middle',
});

export function Tradeoffs({ data, theme }: { data: Data; theme: Theme }) {
  const c = chartColors(theme);
  const cat = category(theme);
  const [metric, setMetric] = useState<Metric>('yi');
  const [logX, setLogX] = useState(true);
  const [showFrontier, setShowFrontier] = useState(true);
  const [lab, setLab] = useState('all');
  const [reli, setReli] = useState<Reli>('fail');
  const [effMetric, setEffMetric] = useState<Metric>('yi');

  const t = data.tradeoffs;
  const val = (r: TradeoffRow): number => (metric === 'yi' ? r.yi : (r.f1 as number));

  const labs = useMemo(
    () => ['all', ...Array.from(new Set(t.map((r) => r.lab))).sort()],
    [t],
  );

  const stats = useMemo(() => {
    const procs = t.map((r) => r.proc);
    const minProc = Math.min(...procs);
    const maxProc = Math.max(...procs);
    const eff = t.map((r) => ({ r, e: r.cost / r.yi })).sort((a, b) => a.e - b.e);
    const best = eff[0];
    const worst = eff[eff.length - 1];
    const reliableConfigs = data.reliability.filter((r) => r.fail === 0).length;
    return {
      minProc, maxProc, procSpan: maxProc / minProc,
      bestEff: best, effSpan: worst.e / best.e,
      reliableConfigs, totalConfigs: data.reliability.length,
    };
  }, [t, data.reliability]);

  /* -------------------- Figure 3 · quality vs latency -------------------- */
  const speed = useMemo(() => {
    const pts = metric === 'f1' ? t.filter((r) => r.f1 != null) : t;

    // upper-left frontier: minimise processing time, maximise quality
    const front = [...pts]
      .sort((a, b) => a.proc - b.proc)
      .reduce<TradeoffRow[]>((acc, r) => {
        if (!acc.length || val(r) > val(acc[acc.length - 1])) acc.push(r);
        return acc;
      }, []);
    const frontSet = new Set(front.map((r) => r.model));

    // cost drives both bubble size and hue: a monotone log-cost ramp (rank-preserving,
    // compressed so the ~900× cost spread stays on-canvas), hue on the neutral→warm
    // (grey→red) half of the spectrum so it reads as "spend".
    const costs = pts.map((r) => r.cost);
    const lcMin = Math.log(Math.min(...costs));
    const lcMax = Math.log(Math.max(...costs));
    const costT = (v: number) => (lcMax > lcMin ? (Math.log(v) - lcMin) / (lcMax - lcMin) : 0.5);
    // area-true sizing: bubble AREA (what the eye reads) is linear in the log-cost
    // ramp — sizing the diameter instead exaggerates the cheap end and flattens
    // the costly end
    const D_MIN = 4;
    const D_MAX = 20;
    const size = (v: number) => Math.sqrt(D_MIN * D_MIN + (D_MAX * D_MAX - D_MIN * D_MIN) * costT(v));
    const costHue = (v: number) => spectrumColor(0.5 + 0.5 * costT(v), theme);

    const vals = pts.map(val);
    const lo = Math.min(...vals);
    const hi = Math.max(...vals);
    const pad = (hi - lo) * 0.14 || 0.02;

    const ordered = [...pts].sort(
      (a, b) => (frontSet.has(a.model) ? 1 : 0) - (frontSet.has(b.model) ? 1 : 0),
    );
    const scatter = ordered.map((r) => {
      const onFront = frontSet.has(r.model);
      const dimmed = lab !== 'all' && r.lab !== lab;
      return {
        value: [r.proc, +val(r).toFixed(4)],
        name: r.model,
        meta: r,
        symbolSize: size(r.cost),
        itemStyle: {
          color: costHue(r.cost),
          borderColor: onFront ? c.panelRing : c.surface,
          borderWidth: onFront ? 2 : 1.5,
          opacity: dimmed ? 0.14 : 0.95,
        },
        label: {
          show: onFront && !dimmed,
          position: 'right' as const,
          color: c.text,
          fontSize: 11,
          fontFamily: FONT_UI,
          fontWeight: 500 as const,
          formatter: () => r.model,
        },
      };
    });

    const option: EChartsOption = {
      ...animBase(),
      textStyle: { fontFamily: FONT_UI },
      grid: { left: 60, right: 140, top: 24, bottom: 52 },
      tooltip: {
        trigger: 'item',
        ...tooltipBase(c),
        formatter: (p: unknown) => {
          const r = (p as { data: { meta: TradeoffRow } }).data.meta;
          const mono = (s: string) => `<span style="font-family:${FONT_MONO};font-size:11.5px">${s}</span>`;
          const tag = cfgTag(r.config);
          return [
            `<b>${escapeHtml(r.model)}</b> <span style="color:${c.muted}">${escapeHtml(r.lab)}</span>`,
            `YI ${mono(`<b>${r.yi.toFixed(3)}</b>`)}${r.f1 != null ? ` &nbsp; F1 ${mono(`<b>${r.f1.toFixed(3)}</b>`)}` : ''}`,
            `Speed ${mono(`<b>${fmtSec(r.proc)}</b>`)}/run &nbsp; cost ${mono(`<b>${fmtUsd(r.cost)}</b>`)}`,
            frontSet.has(r.model) ? `<span style="color:${c.muted}">speed–quality frontier</span>` : '',
            tag ? `<span style="color:${c.muted}">${escapeHtml(tag)}</span>` : '',
          ].filter(Boolean).join('<br/>');
        },
      },
      xAxis: {
        type: logX ? 'log' : 'value',
        ...(logX
          ? {
              min: +(Math.min(...pts.map((r) => r.proc)) * 0.8).toPrecision(2),
              max: +(Math.max(...pts.map((r) => r.proc)) * 1.25).toPrecision(2),
            }
          : {}),
        name: 'Avg processing time (s / run)',
        nameLocation: 'middle',
        nameGap: 34,
        nameTextStyle: { color: c.text2, fontSize: 11, fontFamily: FONT_UI },
        axisLine: { lineStyle: { color: c.axis } },
        axisTick: { show: false },
        axisLabel: { ...tickStyle(c), formatter: (v: number) => `${+v.toPrecision(2)}s` },
        splitLine: { lineStyle: { color: c.split, width: 1 } },
      },
      yAxis: {
        type: 'value',
        min: +(lo - pad).toFixed(3),
        max: +(hi + pad).toFixed(3),
        name: metric === 'yi' ? "Oracle Youden's J" : 'Oracle F1',
        nameLocation: 'middle',
        nameGap: 48,
        nameTextStyle: { color: c.text2, fontSize: 11, fontFamily: FONT_UI },
        axisLine: { show: false },
        axisTick: { show: false },
        axisLabel: { ...tickStyle(c), showMinLabel: false, showMaxLabel: false },
        splitLine: { lineStyle: { color: c.split, width: 1 } },
      },
      series: [
        ...(showFrontier
          ? [
              {
                type: 'line' as const,
                data: front.map((r) => [r.proc, +val(r).toFixed(4)]),
                showSymbol: false,
                lineStyle: { color: c.frontier, width: 1.5 },
                z: 1,
                silent: true,
                tooltip: { show: false },
              },
            ]
          : []),
        { type: 'scatter' as const, data: scatter, z: 3, labelLayout: { hideOverlap: true } },
      ],
    };
    // real endpoints for the size/hue key, from the same points the chart plots
    return { option, costMin: Math.min(...costs), costMax: Math.max(...costs) };
  }, [t, metric, logX, showFrontier, lab, c, theme]);

  /* -------------------- Figure 4 · cost efficiency -------------------- */
  const effRows = useMemo(() => {
    const rows = t
      .filter((r) => (effMetric === 'f1' ? r.f1 != null : true))
      .map((r) => ({ r, e: r.cost / (effMetric === 'yi' ? r.yi : (r.f1 as number)) }))
      .sort((a, b) => a.e - b.e); // most efficient first
    return rows;
  }, [t, effMetric]);

  const effOption: EChartsOption = useMemo(() => {
    // dot plot on a log axis: position (not bar length) encodes $ per quality-point,
    // honest across the ~600× spread. best (cheapest) at the top.
    const rows = [...effRows].reverse(); // category axis draws index 0 at the bottom
    const es = rows.map((x) => x.e);
    return {
      ...animBase(),
      textStyle: { fontFamily: FONT_UI },
      grid: { left: 168, right: 64, top: 14, bottom: 42 },
      tooltip: {
        trigger: 'item',
        ...tooltipBase(c),
        formatter: (p: unknown) => {
          const o = p as { dataIndex: number };
          const { r, e } = rows[o.dataIndex];
          const mono = (s: string) => `<span style="font-family:${FONT_MONO};font-size:11.5px">${s}</span>`;
          return [
            `<b>${escapeHtml(r.model)}</b> <span style="color:${c.muted}">${escapeHtml(r.lab)}</span>`,
            `${mono(`<b>${fmtUsd(e)}</b>`)} per ${metricLabel(effMetric)} point`,
            `cost ${mono(fmtUsd(r.cost))}/run &nbsp; ${effMetric === 'yi' ? 'YI' : 'F1'} ${mono((effMetric === 'yi' ? r.yi : (r.f1 as number)).toFixed(3))}`,
          ].join('<br/>');
        },
      },
      xAxis: {
        type: 'log',
        name: `USD per ${metricLabel(effMetric)} point (log)`,
        nameLocation: 'middle',
        nameGap: 28,
        min: +(Math.min(...es) * 0.7).toPrecision(2),
        max: +(Math.max(...es) * 1.4).toPrecision(2),
        axisLine: { show: false },
        axisTick: { show: false },
        axisLabel: { ...tickStyle(c), formatter: (v: number) => fmtUsd(v) },
        splitLine: { lineStyle: { color: c.split, width: 1 } },
        nameTextStyle: { color: c.text2, fontSize: 11, fontFamily: FONT_UI },
      },
      yAxis: {
        type: 'category',
        data: rows.map((x) => x.r.model),
        axisLabel: { ...tickStyle(c), fontSize: 10.5, width: 150, overflow: 'truncate' },
        axisTick: { show: false },
        axisLine: { lineStyle: { color: c.axis } },
      },
      series: [
        {
          type: 'scatter' as const,
          symbolSize: 11,
          data: rows.map((x, i) => ({
            value: [x.e, i],
            itemStyle: {
              color: x.r.costPareto ? cat[0] : c.frontier,
              // cost-Pareto models get a surface ring (a non-colour channel for the flag)
              borderColor: x.r.costPareto ? c.panelRing : c.surface,
              borderWidth: x.r.costPareto ? 2 : 1.5,
              opacity: 0.95,
            },
          })),
          labelLayout: { hideOverlap: true },
          label: {
            show: true,
            position: 'right' as const,
            color: c.text2,
            fontSize: 10.5,
            fontFamily: FONT_MONO,
            formatter: (p: { dataIndex: number }) => fmtUsd(rows[p.dataIndex].e),
          },
        },
      ],
    };
  }, [effRows, effMetric, c, cat]);

  /* -------------------- Figure 5 · reliability -------------------- */
  const reliRows = useMemo(() => {
    // keep null (unmeasured) distinct from a measured 0 — don't silently drop failing configs
    const rows = data.reliability
      .filter((r) => (reli === 'fail' ? (r.fail ?? 0) > 0 : r.retries != null && r.retries > 0))
      .sort((a, b) => (reli === 'fail' ? (b.fail ?? 0) - (a.fail ?? 0) : (b.retries ?? 0) - (a.retries ?? 0)));
    return rows;
  }, [data.reliability, reli]);

  const reliOption: EChartsOption = useMemo(() => {
    const rows = [...reliRows].reverse(); // worst at the top of a horizontal bar
    const bad = statusBad(theme);
    // three hue-distinct, theme-token classes: red (fails) / grey (reliable) / iris (best)
    const color = (r: ReliabilityRow) =>
      r.cls === 'unreliable' ? bad : r.cls === 'pareto' ? cat[0] : c.frontier;
    return {
      ...animBase(),
      textStyle: { fontFamily: FONT_UI },
      grid: { left: 210, right: 52, top: 14, bottom: 42 },
      tooltip: {
        trigger: 'item',
        ...tooltipBase(c),
        formatter: (p: unknown) => {
          const o = p as { dataIndex: number };
          const r = rows[o.dataIndex];
          const mono = (s: string) => `<span style="font-family:${FONT_MONO};font-size:11.5px">${s}</span>`;
          return [
            `<b>${escapeHtml(r.model)}</b> <span style="color:${c.muted}">${escapeHtml(r.lab)}</span>`,
            reli === 'fail'
              ? `fail rate ${mono(`<b>${((r.fail ?? 0) * 100).toFixed(1)}%</b>`)}`
              : `retries ${mono(`<b>${(r.retries ?? 0).toFixed(2)}</b>`)}/call`,
            cfgTag(r.config) ? `<span style="color:${c.muted}">${escapeHtml(cfgTag(r.config))}</span>` : '',
          ].filter(Boolean).join('<br/>');
        },
      },
      xAxis: {
        type: 'value',
        min: 0,
        max: reli === 'fail' ? 1 : undefined,
        name: reli === 'fail' ? 'Failure rate' : 'Retries per call',
        nameLocation: 'middle',
        nameGap: 28,
        axisLine: { show: false },
        axisTick: { show: false },
        axisLabel: { ...tickStyle(c), formatter: (v: number) => (reli === 'fail' ? `${Math.round(v * 100)}%` : String(v)) },
        splitLine: { lineStyle: { color: c.split, width: 1 } },
        nameTextStyle: { color: c.text2, fontSize: 11, fontFamily: FONT_UI },
      },
      yAxis: {
        type: 'category',
        data: rows.map((r) => (cfgTag(r.config) ? `${r.model} · ${cfgTag(r.config)}` : r.model)),
        axisLabel: { ...tickStyle(c), fontSize: 10, width: 196, overflow: 'truncate' },
        axisTick: { show: false },
        axisLine: { lineStyle: { color: c.axis } },
      },
      series: [
        {
          type: 'bar',
          barMaxWidth: 13,
          data: rows.map((r) => ({
            value: reli === 'fail' ? +(r.fail ?? 0).toFixed(4) : +(r.retries ?? 0).toFixed(3),
            itemStyle: { color: color(r), borderRadius: [0, 3, 3, 0] },
          })),
        },
      ],
    };
  }, [reliRows, reli, c, cat, theme]);

  const stops = spectrumStops(theme);

  return (
    <div className="stack">
      <section className="hero">
        <span className="kicker">Figures 3–5 · cost · speed · reliability</span>
        <h1>The other axes of the choice</h1>
        <p className="lead">
          A good oracle is not just accurate — it has to be affordable <em>per unit of quality</em>,
          fast enough to sit in the pipeline, and reliable enough to answer every call. This board
          re-scores the human-mouse field on those three axes (best configuration per model).
        </p>
      </section>

      <section className="stat-strip card" aria-label="Trade-off headline statistics">
        {[
          { label: 'Latency span', v: `${stats.procSpan.toFixed(0)}×`, d: `${fmtSec(stats.minProc)} to ${fmtSec(stats.maxProc)} per run` },
          { label: 'Best value', v: `${fmtUsd(stats.bestEff.e)}`, d: `per YI point · ${stats.bestEff.r.model}` },
          { label: 'Value spread', v: `${stats.effSpan.toFixed(0)}×`, d: 'cheapest vs dearest $/YI point' },
          { label: 'Reliable configs', v: `${stats.reliableConfigs}/${stats.totalConfigs}`, d: 'never fail a call (0% failure)' },
        ].map((s) => (
          <div key={s.label} className="stat-cell">
            <span className="stat-label">{s.label}</span>
            <span className="stat-value">{s.v}</span>
            <span className="stat-detail">{s.d}</span>
          </div>
        ))}
      </section>

      <section className="card">
        <div className="card-head">
          <div>
            <span className="figure-kicker">Figure 3 · <em>Interactive</em></span>
            <h2>Quality vs latency</h2>
          </div>
          <span className="meta">
            {metric === 'f1' ? t.filter((r) => r.f1 != null).length : t.length} models · bubble = cost/run · up-and-left is best
          </span>
        </div>
        <div className="controls">
          <div className="control">
            <span className="control-label" id="to-metric">Y metric</span>
            <div className="segmented" role="group" aria-labelledby="to-metric">
              <button aria-pressed={metric === 'yi'} onClick={() => setMetric('yi')}>Youden&apos;s J</button>
              <button aria-pressed={metric === 'f1'} onClick={() => setMetric('f1')}>Oracle F1</button>
            </div>
          </div>
          <div className="control">
            <span className="control-label" id="to-scale">Time axis</span>
            <div className="segmented" role="group" aria-labelledby="to-scale">
              <button aria-pressed={logX} onClick={() => setLogX(true)}>Log</button>
              <button aria-pressed={!logX} onClick={() => setLogX(false)}>Linear</button>
            </div>
          </div>
          <div className="control">
            <label className="control-label" htmlFor="to-lab">Highlight lab</label>
            <select id="to-lab" className="ctrl" value={lab} onChange={(e) => setLab(e.target.value)}>
              {labs.map((l) => (
                <option key={l} value={l}>{l === 'all' ? 'All labs' : l}</option>
              ))}
            </select>
          </div>
          <div className="control">
            <span className="control-label">Frontier</span>
            <label className="check">
              <input type="checkbox" checked={showFrontier} onChange={(e) => setShowFrontier(e.target.checked)} />
              Show frontier
            </label>
          </div>
        </div>
        <EChart option={speed.option} height={460} ariaLabel="Oracle quality versus average processing time; bubble size is cost per run; data table below" />
        <div className="key-bar">
          <span>
            <span
              className="spectrum-chip"
              aria-hidden="true"
              style={{ background: `linear-gradient(90deg, ${stops[1]}, ${stops[2]})` }}
            />
            &nbsp; bubble size &amp; hue = cost per run ({fmtUsd(speed.costMin)} → {fmtUsd(speed.costMax)})
          </span>
          <span><b>ring + label</b> = on the speed–quality frontier · line = frontier</span>
        </div>
        <p className="caption">
          Latency and cost travel together: the biggest, warmest bubbles cluster at the slow, costly
          end. The frontier is the set of models that are Pareto-optimal on speed vs quality — no
          model is both faster and better.
        </p>
        <FigureData
          summary="View Figure 3 data"
          columns={['Model', 'Lab', 'YI', 'F1', '$/run', 'Time (s)']}
          numeric={[2, 3, 4, 5]}
          rows={[...t]
            .sort((a, b) => a.proc - b.proc)
            .map((r) => [
              <code className="model-id" key={r.model}>{r.model}</code>,
              r.lab,
              r.yi.toFixed(3),
              r.f1 != null ? r.f1.toFixed(3) : '—',
              fmtUsd(r.cost),
              r.proc.toFixed(1),
            ])}
        />
      </section>

      <section className="grid grid-2">
        <div className="card">
          <div className="card-head">
            <div>
              <span className="figure-kicker">Figure 4 · <em>Interactive</em></span>
              <h2>Cost per unit of quality</h2>
            </div>
          </div>
          <div className="controls">
            <div className="control">
              <span className="control-label" id="eff-metric">Quality metric</span>
              <div className="segmented" role="group" aria-labelledby="eff-metric">
                <button aria-pressed={effMetric === 'yi'} onClick={() => setEffMetric('yi')}>$ / YI</button>
                <button aria-pressed={effMetric === 'f1'} onClick={() => setEffMetric('f1')}>$ / F1</button>
              </div>
            </div>
          </div>
          <EChart option={effOption} height={560} ariaLabel="US dollars per quality point per model, cheapest at top; data table below" />
          <p className="caption">
            Cost per run divided by {metricLabel(effMetric)} — a spend-efficiency ranking. Dot
            position (log axis) is the value; <b>ringed iris</b> dots are cost–quality Pareto-optimal
            models. Cheaper (left) is better.
          </p>
          <FigureData
            summary="View Figure 4 data"
            columns={['Model', `$/${effMetric === 'yi' ? 'YI' : 'F1'} point`, '$/run', 'Pareto']}
            numeric={[1, 2]}
            rows={effRows.map(({ r, e }) => [
              <code className="model-id" key={r.model}>{r.model}</code>,
              fmtUsd(e),
              fmtUsd(r.cost),
              r.costPareto ? '✓' : '—',
            ])}
          />
        </div>

        <div className="card">
          <div className="card-head">
            <div>
              <span className="figure-kicker">Figure 5 · <em>Interactive</em></span>
              <h2>Reliability — who fails or retries</h2>
            </div>
            <div className="chips" aria-label="Reliability summary">
              <span className="chip"><b>{stats.reliableConfigs}/{stats.totalConfigs}</b> never fail</span>
            </div>
          </div>
          <div className="controls">
            <div className="control">
              <span className="control-label" id="reli-metric">Measure</span>
              <div className="segmented" role="group" aria-labelledby="reli-metric">
                <button aria-pressed={reli === 'fail'} onClick={() => setReli('fail')}>Failure rate</button>
                <button aria-pressed={reli === 'retries'} onClick={() => setReli('retries')}>Retries / call</button>
              </div>
            </div>
          </div>
          <EChart option={reliOption} height={560} ariaLabel="Models ranked by failure rate or retries per call, coloured by reliability class; data table below" />
          <div className="key-bar">
            <span>
              <span aria-hidden="true" style={swatch(statusBad(theme))} /> unreliable (fails calls)
              &nbsp;·&nbsp; <span aria-hidden="true" style={swatch(c.frontier)} /> reliable
              &nbsp;·&nbsp; <span aria-hidden="true" style={swatch(cat[0])} /> best / Pareto
            </span>
            <span>only configs with a non-zero {reli === 'fail' ? 'failure rate' : 'retry count'} are shown</span>
          </div>
          <p className="caption">
            {reli === 'fail'
              ? `The ${reliRows.length} configurations that fail some calls — the rest answer every call cleanly.`
              : `The ${reliRows.length} configurations that retry — the rest need no retries or were not measured (see the table).`}{' '}
            Red models fail outright (unusable as an oracle); iris marks otherwise-strong models.
          </p>
          <FigureData
            summary="View Figure 5 data"
            columns={['Model', 'Class', 'Fail rate', 'Retries/call', 'Config']}
            numeric={[2, 3]}
            rows={[...data.reliability]
              .sort((a, b) => (b.fail ?? 0) - (a.fail ?? 0))
              .map((r) => [
                <code className="model-id" key={`${r.model}-${r.config}`}>{r.model}</code>,
                r.cls,
                r.fail != null ? `${(r.fail * 100).toFixed(1)}%` : '—',
                r.retries != null ? r.retries.toFixed(2) : '—',
                cfgTag(r.config) || '—',
              ])}
          />
        </div>
      </section>

      {/* <p className="footnote">
        Trade-off board from the human-mouse cost/speed/reliability study — one point per model at
        its best-scoring configuration, so it spans a broader, newer candidate field than the
        18-model measured-cost board on the Leaderboard. Cost = hosted API $/run;
        processing time = mean wall-clock per run; failure rate &amp; retries are measured over the
        same runs.
      </p> */}
    </div>
  );
}
