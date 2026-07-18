import { useEffect, useMemo, useState } from 'react';
import type { EChartsOption } from 'echarts';
import type { Data, Theme } from '../types';
import { EChart } from '../components/EChart';
import { FigureData } from '../components/FigureData';
import { animBase, chartColors, escapeHtml, seriesColors, statusBad, tickStyle, tooltipBase, FONT_UI } from '../chart';

/** re-render when the viewport crosses the narrow breakpoint (dot clusters shrink) */
function useNarrow(): boolean {
  const [narrow, setNarrow] = useState(() => window.matchMedia('(max-width: 760px)').matches);
  useEffect(() => {
    const mq = window.matchMedia('(max-width: 760px)');
    const onChange = (e: MediaQueryListEvent) => setNarrow(e.matches);
    mq.addEventListener('change', onChange);
    return () => mq.removeEventListener('change', onChange);
  }, []);
  return narrow;
}

export function OracleValue({ data, theme }: { data: Data; theme: Theme }) {
  const c = chartColors(theme);
  const sc = seriesColors(theme);
  const [showSim, setShowSim] = useState(true);
  const narrow = useNarrow();

  const summary = useMemo(() => {
    const helped = data.oracle.filter((o) => o.delta > 0).length;
    const meanDelta = data.oracle.reduce((s, o) => s + o.delta, 0) / data.oracle.length;
    const meanCap = data.oracle.reduce((s, o) => s + o.capture, 0) / data.oracle.length;
    return { helped, meanDelta, meanCap, n: data.oracle.length };
  }, [data.oracle]);

  const dotOption: EChartsOption = useMemo(() => {
    const tasks = data.oracle.map((o) => o.task);
    const defs = [
      { name: 'LogMap (no oracle)', key: 'logmap' as const, color: sc.baseline },
      { name: '+ LLM oracle (GF2.5)', key: 'llm' as const, color: sc.llm },
      { name: '+ perfect oracle (ceiling)', key: 'perfect' as const, color: sc.perfect },
      ...(showSim
        ? [
            { name: '+ simulated 20% error', key: 'err20' as const, color: sc.sim20 },
            { name: '+ simulated 30% error', key: 'err30' as const, color: sc.sim30 },
          ]
        : []),
    ];
    // grouped dot plot: position (not bar length) encodes F1, so the zoomed
    // 0.55–0.95 window is honest; each series keeps a fixed slot in the cluster
    const step = narrow ? 8 : 11;
    const series = defs.map((d, i) => ({
      name: d.name,
      type: 'scatter' as const,
      symbol: 'circle',
      symbolSize: narrow ? 7 : 9,
      symbolOffset: [(i - (defs.length - 1) / 2) * step, 0] as [number, number],
      data: data.oracle.map((o) => +o[d.key].toFixed(3)),
      itemStyle: { color: d.color, borderColor: c.surface, borderWidth: 2 },
      z: 3 + i,
    }));
    return {
      ...animBase(),
      textStyle: { fontFamily: FONT_UI },
      legend: {
        top: 0,
        left: 0,
        icon: 'circle',
        itemWidth: 10,
        itemHeight: 10,
        itemGap: 16,
        textStyle: { color: c.text2, fontSize: 12, fontFamily: FONT_UI },
        type: 'scroll',
      },
      grid: { left: 52, right: 16, top: 56, bottom: 84 },
      tooltip: {
        trigger: 'axis',
        axisPointer: { type: 'line', lineStyle: { color: c.axis, width: 1 } },
        ...tooltipBase(c),
        valueFormatter: (v) => (typeof v === 'number' ? v.toFixed(3) : String(v)),
      },
      xAxis: {
        type: 'category',
        data: tasks,
        axisLine: { lineStyle: { color: c.axis } },
        axisTick: { show: false },
        axisLabel: { ...tickStyle(c), fontSize: 10, rotate: 32 },
      },
      yAxis: {
        type: 'value',
        min: 0.55,
        max: 0.95,
        name: 'Global F1',
        axisLine: { show: false },
        splitLine: { lineStyle: { color: c.split, width: 1 } },
        axisLabel: tickStyle(c),
        nameTextStyle: { color: c.text2, fontSize: 11, fontFamily: FONT_UI, align: 'left' },
      },
      series,
    };
  }, [data.oracle, showSim, c, sc, narrow]);

  const capOption: EChartsOption = useMemo(() => {
    const sorted = [...data.oracle].sort((a, b) => a.capture - b.capture);
    // gain captured wears the LLM-oracle series color; net-harm wears status red
    // (not the Figure-3 cost spectrum — warm there means "costly+high", not "bad")
    const gain = sc.llm;
    const harm = statusBad(theme);
    return {
      ...animBase(),
      textStyle: { fontFamily: FONT_UI },
      grid: { left: 150, right: 44, top: 26, bottom: 44 },
      tooltip: {
        trigger: 'item',
        ...tooltipBase(c),
        formatter: (p: unknown) => {
          const o = p as { name: string; value: number; dataIndex: number };
          const row = sorted[o.dataIndex];
          return `${escapeHtml(row.task)}<br/>captures <b>${o.value}%</b> of ceiling<br/><span style="color:${c.muted}">Δ ${row.delta >= 0 ? '+' : ''}${row.delta.toFixed(3)} F1</span>`;
        },
      },
      xAxis: {
        type: 'value',
        // fixed bounds + 25-step keep one tick rhythm AND the 100% ceiling in-plot
        min: -50,
        max: 100,
        interval: 25,
        name: '% of perfect-oracle gain captured',
        nameLocation: 'middle',
        nameGap: 28,
        axisLine: { show: false },
        axisLabel: tickStyle(c),
        splitLine: { lineStyle: { color: c.split, width: 1 } },
        nameTextStyle: { color: c.text2, fontSize: 11, fontFamily: FONT_UI },
      },
      yAxis: {
        type: 'category',
        data: sorted.map((o) => o.task),
        axisLabel: { ...tickStyle(c), fontSize: 10.5 },
        axisTick: { show: false },
        axisLine: { lineStyle: { color: c.axis } },
      },
      series: [
        {
          type: 'bar',
          barMaxWidth: 14,
          data: sorted.map((o) => {
            const v = Math.round(o.capture * 100);
            return {
              value: v,
              // rounded at the data end only, square at the zero baseline
              itemStyle: {
                color: o.capture < 0 ? harm : gain,
                borderRadius: v < 0 ? ([3, 0, 0, 3] as number[]) : ([0, 3, 3, 0] as number[]),
              },
            };
          }),
          markLine: {
            silent: true,
            symbol: 'none',
            data: [{ xAxis: 100 }],
            lineStyle: { color: c.ceiling, type: 'solid', width: 1 },
            label: { formatter: 'ceiling', color: c.muted, fontSize: 11, fontFamily: FONT_UI },
          },
        },
      ],
    };
  }, [data.oracle, c, sc, theme]);

  return (
    <div className="stack">
      <section className="card">
        <div className="card-head">
          <div>
            <span className="figure-kicker">Figure 10 · <em>Interactive</em></span>
            <h1>Does the oracle actually help?</h1>
          </div>
          <div className="chips" aria-label="Summary statistics">
            <span className="chip">helps <b>{summary.helped}/{summary.n}</b> tasks</span>
            <span className="chip">mean <b>+{summary.meanDelta.toFixed(3)}</b> F1</span>
            <span className="chip">captures <b>{Math.round(summary.meanCap * 100)}%</b> of ceiling</span>
          </div>
        </div>
        <p className="lead" style={{ marginBottom: 12 }}>
          End-to-end global F1 with no oracle, with the real Gemini-Flash-2.5 oracle, and with a{' '}
          <em>perfect</em> oracle (the achievable ceiling). Simulated oracles at 20% / 30% error
          calibrate the scale: the real model behaves like a moderately-erroring human validator.
        </p>
        <div className="controls">
          <label className="check">
            <input type="checkbox" checked={showSim} onChange={(e) => setShowSim(e.target.checked)} />
            Show simulated-error oracles (20% / 30%)
          </label>
        </div>
        <EChart option={dotOption} height={400} ariaLabel="Global F1 by task for LogMap, LLM oracle, and perfect oracle; data table below" />
        <p className="caption">
          Dot position (not bar length) encodes F1, so the zoomed 0.55–0.95 window compares
          conditions without distorting them. Within each task the dots keep a fixed order:
          no&nbsp;oracle · LLM · perfect{showSim ? ' · sim 20% · sim 30%' : ''}.
        </p>
        <FigureData
          summary="View Figure 10 data"
          columns={['Task', 'LogMap', '+ LLM', '+ perfect', '+ sim 20%', '+ sim 30%']}
          numeric={[1, 2, 3, 4, 5]}
          rows={data.oracle.map((o) => [
            o.task,
            o.logmap.toFixed(3),
            o.llm.toFixed(3),
            o.perfect.toFixed(3),
            o.err20.toFixed(3),
            o.err30.toFixed(3),
          ])}
        />
      </section>

      <section className="card">
        <div className="card-head">
          <div>
            <span className="figure-kicker">Figure 11</span>
            <h2>Capture ratio — how much of the ceiling the oracle realises</h2>
          </div>
        </div>
        <EChart option={capOption} height={330} ariaLabel="Fraction of the perfect-oracle gain captured, per task; data table below" />
        <p className="caption">
          Δ(LLM) as a fraction of Δ(perfect). Iris bars are captured gain; leftward red bars mark
          tasks where the oracle net-hurts (the sign travels in the data, not just the color).
        </p>
        <FigureData
          summary="View Figure 11 data"
          columns={['Task', 'Ceiling captured', 'Δ F1 (LLM)']}
          numeric={[1, 2]}
          rows={[...data.oracle]
            .sort((a, b) => b.capture - a.capture)
            .map((o) => [
              o.task,
              `${Math.round(o.capture * 100)}%`,
              `${o.delta >= 0 ? '+' : ''}${o.delta.toFixed(3)}`,
            ])}
        />
      </section>
    </div>
  );
}
