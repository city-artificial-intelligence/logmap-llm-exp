import { useMemo } from 'react';
import type { EChartsOption } from 'echarts';
import type { Data, Theme } from '../types';
import { EChart } from '../components/EChart';
import { animBase, category, chartColors, escapeHtml, tickStyle, tooltipBase, FONT_UI } from '../chart';
import { FigureData } from '../components/FigureData';

export function Overview({ data, theme }: { data: Data; theme: Theme }) {
  const c = chartColors(theme);
  const cat = category(theme);

  const stats = useMemo(() => {
    const costs = data.leader.map((l) => l.cost);
    const f1s = data.leader.map((l) => l.f1);
    const costFactor = Math.round(Math.max(...costs) / Math.min(...costs));
    const f1span = (Math.max(...f1s) - Math.min(...f1s)) * 100;
    const helped = data.oracle.filter((o) => o.delta > 0).length;
    const meanDelta = data.oracle.reduce((s, o) => s + o.delta, 0) / data.oracle.length;
    const genRatio = data.gen[data.gen.length - 1].yi / data.gen[0].yi;
    const reasMax = Math.round(Math.max(...data.costDrivers.map((d) => d.reasoning)) * 100);
    return { costFactor, f1span, helped, meanDelta, genRatio, reasMax };
  }, [data]);

  const genOption: EChartsOption = useMemo(() => {
    const last = data.gen.length - 1;
    return {
      ...animBase(),
      textStyle: { fontFamily: FONT_UI },
      grid: { left: 48, right: 24, top: 36, bottom: 40 },
      tooltip: {
        trigger: 'axis',
        ...tooltipBase(c),
        valueFormatter: (v) => (typeof v === 'number' ? v.toFixed(3) : String(v)),
      },
      xAxis: {
        type: 'category',
        data: data.gen.map((g) => g.generation.replace('Flash.', '')),
        axisLine: { lineStyle: { color: c.axis } },
        axisTick: { show: false },
        axisLabel: tickStyle(c),
        name: 'Gemini Flash generation',
        nameLocation: 'middle',
        nameGap: 28,
        nameTextStyle: { color: c.text2, fontSize: 11, fontFamily: FONT_UI },
      },
      yAxis: {
        type: 'value',
        min: 0,
        max: 0.6,
        name: 'Mean oracle YI',
        axisLine: { show: false },
        splitLine: { lineStyle: { color: c.split, width: 1 } },
        axisLabel: tickStyle(c),
        nameTextStyle: { color: c.text2, fontSize: 11, fontFamily: FONT_UI, align: 'left' },
      },
      series: [
        {
          type: 'line',
          smooth: false,
          symbol: 'circle',
          symbolSize: 8,
          data: data.gen.map((g, i) => ({
            value: +g.yi.toFixed(3),
            // selective labels: endpoints only, not a number on every point
            label: {
              show: i === 0 || i === last,
              color: c.text2,
              fontSize: 11,
              position: i === last ? ('left' as const) : ('top' as const),
              formatter: (p: { value: unknown }) => String(p.value),
            },
          })),
          lineStyle: { width: 2, color: cat[0] },
          itemStyle: { color: cat[0], borderColor: c.surface, borderWidth: 2 },
        },
      ],
    };
  }, [data.gen, c, cat]);

  const cdOption: EChartsOption = useMemo(() => {
    const cd = [...data.costDrivers].sort((a, b) => a.reasoning - b.reasoning);
    return {
      ...animBase(),
      textStyle: { fontFamily: FONT_UI },
      grid: { left: 150, right: 32, top: 12, bottom: 40 },
      tooltip: {
        // axis trigger so measured-0% rows (zero-length bars) are still hoverable
        trigger: 'axis',
        axisPointer: { type: 'line', lineStyle: { color: c.axis, width: 1 } },
        ...tooltipBase(c),
        formatter: (p: unknown) => {
          const o = (p as { name: string; value: number }[])[0];
          return o.value === 0
            ? `${escapeHtml(o.name)}<br/><b>$0</b> billed for reasoning tokens (measured, not missing)`
            : `${escapeHtml(o.name)}<br/><b>${o.value}%</b> of cost is reasoning`;
        },
      },
      xAxis: {
        type: 'value',
        max: 100,
        name: 'Reasoning share of cost (%)',
        nameLocation: 'middle',
        nameGap: 28,
        axisLine: { show: false },
        axisLabel: tickStyle(c),
        splitLine: { lineStyle: { color: c.split, width: 1 } },
        nameTextStyle: { color: c.text2, fontSize: 11, fontFamily: FONT_UI },
      },
      yAxis: {
        type: 'category',
        data: cd.map((d) => d.model),
        axisLabel: { ...tickStyle(c), fontSize: 10.5 },
        axisTick: { show: false },
        axisLine: { lineStyle: { color: c.axis } },
      },
      series: [
        {
          type: 'bar',
          data: cd.map((d) => {
            const v = Math.round(d.reasoning * 100);
            return {
              value: v,
              // label the exceptional zeros explicitly: these runs billed no
              // reasoning tokens — a bare "0%" reads as missing or an error
              label: v === 0
                ? { show: true, position: 'right' as const, formatter: 'none billed', color: c.text2, fontSize: 11 }
                : { show: false },
            };
          }),
          barMaxWidth: 14,
          // reasoning share is a neutral magnitude, not an alarm — slot-1, not red
          itemStyle: { color: cat[0], borderRadius: [0, 3, 3, 0] },
        },
      ],
    };
  }, [data.costDrivers, c, cat]);

  return (
    <div className="stack">
      <section className="hero">
        <span className="kicker">Oracle cost/benefit study · 18 models · 9 tasks</span>
        <h1>Choosing the LLM oracle for LogMapLLM</h1>
        <p className="lead">
          LogMapLLM asks a language model to accept or reject the handful of correspondences LogMap is unsure about (the <code>M_ask</code> set) — so which LLM should validate them? 
          This explorer our benchmark &amp; cost/benefit study: a performance leaderboard with latency, reliability, and cost-efficiency trade-offs.
          How do various parameter combinations effect quality, and the oracle&apos;s affect on the final alignment?
        </p>
      </section>

      <section className="stat-strip card" aria-label="Headline statistics">
        {[
          { label: 'Cost range', v: `${stats.costFactor}×`, d: `for only ${stats.f1span.toFixed(1)} pt of oracle F1` },
          { label: 'Tasks improved', v: `${stats.helped}/${data.oracle.length}`, d: `mean +${stats.meanDelta.toFixed(3)} F1 with the oracle` },
          { label: 'Generation gain', v: `${stats.genRatio.toFixed(2)}×`, d: `oracle quality, Gemini Flash ${data.gen[0].generation.replace('Flash.', '')} → ${data.gen[data.gen.length - 1].generation.replace('Flash.', '')}` },
          { label: 'Reasoning share', v: `${stats.reasMax}%`, d: 'of cost on the top models' },
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
            <span className="figure-kicker">Table 1</span>
            <h2>Selected oracle panel</h2>
          </div>
          <span className="meta">4 cloud + 5 local · 6 labs · fits one 192&nbsp;GB node</span>
        </div>
        <div className="table-wrap" tabIndex={0} role="region" aria-label="Selected oracle panel table">
          <table className="data">
            <thead>
              <tr>
                <th>Tier</th><th>Model</th><th>Lab</th><th>Role</th><th>Why</th>
              </tr>
            </thead>
            <tbody>
              {data.shortlist.map((r) => (
                <tr key={r.model}>
                  <td>
                    <span className={`badge tier${r.tier.trim().toLowerCase() === 'cloud' ? ' cloud' : ''}`}>
                      {r.tier}
                    </span>
                  </td>
                  <td><code className="model-id">{r.model}</code></td>
                  <td>{r.lab}</td>
                  <td>{r.role}</td>
                  <td className="wrap">{r.justification}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <section className="grid grid-2">
        <div className="card">
          <div className="card-head">
            <div>
              <span className="figure-kicker">Figure 1</span>
              <h2>Generation dominates prompts</h2>
            </div>
          </div>
          <EChart option={genOption} height={280} ariaLabel="Mean oracle Youden's J by Gemini Flash generation; data table below" />
          <p className="caption">
            Sweeping only the model generation lifts mean oracle YI {stats.genRatio.toFixed(2)}× —
            far more than any prompt change.
          </p>
          <FigureData
            summary="View Figure 1 data"
            columns={['Generation', 'Mean oracle YI']}
            numeric={[1]}
            rows={data.gen.map((g) => [g.generation.replace('Flash.', ''), g.yi.toFixed(3)])}
          />
        </div>
        <div className="card">
          <div className="card-head">
            <div>
              <span className="figure-kicker">Figure 2</span>
              <h2>Reasoning tokens drive cost</h2>
            </div>
          </div>
          <EChart option={cdOption} height={280} ariaLabel="Reasoning share of cost per model; data table below" />
          <p className="caption">
            On the higher-cost models, reasoning is most of the bill — capping it moves a model
            down-cost cheaply. “None billed” rows are measured billing zeros: the itemised cost
            breakdown records $0 of reasoning tokens for those runs (they are not missing values).
          </p>
          <FigureData
            summary="View Figure 2 data"
            columns={['Model', 'Reasoning share of cost']}
            numeric={[1]}
            rows={[...data.costDrivers]
              .sort((a, b) => b.reasoning - a.reasoning)
              .map((d) => [<code className="model-id" key={d.model}>{d.model}</code>, `${Math.round(d.reasoning * 100)}%`])}
          />
        </div>
      </section>
    </div>
  );
}
