import { useMemo, useState } from 'react';
import type { EChartsOption } from 'echarts';
import type { Data, PricingRow, Theme } from '../types';
import { EChart } from '../components/EChart';
import { FigureData } from '../components/FigureData';
import {
  animBase, category, chartColors, escapeHtml, fmtPer1m, fmtUsdTick,
  tickStyle, tooltipBase, FONT_UI, FONT_MONO,
} from '../chart';

export function PricingLandscape({ data, theme }: { data: Data; theme: Theme }) {
  const c = chartColors(theme);
  const cat = category(theme);
  const [showPriceOnly, setShowPriceOnly] = useState(true);

  const counts = useMemo(() => {
    const tested = data.pricing.filter((p) => p.tested).length;
    const ins = data.pricing.map((p) => p.inputPer1m);
    const outs = data.pricing.map((p) => p.outputPer1m);
    const spanIn = Math.max(...ins) / Math.min(...ins);
    const maxOut = Math.max(...outs);
    return { total: data.pricing.length, tested, priceOnly: data.pricing.length - tested, spanIn, maxOut };
  }, [data.pricing]);

  const option: EChartsOption = useMemo(() => {
    const tested = data.pricing.filter((p) => p.tested);
    const priceOnly = data.pricing.filter((p) => !p.tested);

    const pt = (p: PricingRow, colr: string, ring: boolean) => ({
      value: [p.inputPer1m, p.outputPer1m],
      name: p.model,
      meta: p,
      symbolSize: p.panel ? 15 : 10,
      itemStyle: {
        color: colr,
        borderColor: ring ? c.panelRing : c.surface,
        borderWidth: ring ? 2 : 1.5,
        opacity: 0.95,
      },
      // label only the 3 selected-panel models — 66 labels would be chaos
      label: {
        show: p.panel,
        position: 'right' as const,
        color: c.text,
        fontSize: 11,
        fontWeight: 600 as const,
        fontFamily: FONT_UI,
        formatter: () => p.model,
      },
    });

    const fmtTip = (p: PricingRow, kind: string) => {
      const mono = (s: string) => `<span style="font-family:${FONT_MONO};font-size:11.5px">${s}</span>`;
      return [
        `<b>${escapeHtml(p.model)}</b> <span style="color:${c.muted}">${escapeHtml(p.lab)}</span>`,
        `in ${mono(`<b>${fmtPer1m(p.inputPer1m)}</b>`)}/1M &nbsp; out ${mono(`<b>${fmtPer1m(p.outputPer1m)}</b>`)}/1M`,
        p.tested && p.f1 != null
          ? `oracle ${mono(`F1 ${p.f1.toFixed(3)}`)}${p.yi != null ? ` &nbsp; ${mono(`YI ${p.yi.toFixed(3)}`)}` : ''}`
          : `<span style="color:${c.muted}">${kind}</span>`,
        p.panel ? `<span style="color:${c.muted}">selected panel</span>` : '',
      ].filter(Boolean).join('<br/>');
    };

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
        data: ['Performance-tested', 'Price-only'],
        selected: { 'Price-only': showPriceOnly },
        selectedMode: false,
      },
      grid: { left: 66, right: 130, top: 44, bottom: 52 },
      tooltip: {
        trigger: 'item',
        ...tooltipBase(c),
        formatter: (raw: unknown) => {
          const p = (raw as { data: { meta: PricingRow } }).data.meta;
          return fmtTip(p, p.tested ? 'performance-tested' : 'price-only (no oracle score)');
        },
      },
      xAxis: {
        type: 'log',
        name: 'Input price (USD / 1M tokens)',
        nameLocation: 'middle',
        nameGap: 34,
        nameTextStyle: { color: c.text2, fontSize: 11, fontFamily: FONT_UI },
        axisLine: { lineStyle: { color: c.axis } },
        axisTick: { show: false },
        axisLabel: { ...tickStyle(c), formatter: (v: number) => fmtUsdTick(v) },
        splitLine: { lineStyle: { color: c.split, width: 1 } },
      },
      yAxis: {
        type: 'log',
        name: 'Output price (USD / 1M tokens)',
        nameLocation: 'middle',
        nameGap: 50,
        nameTextStyle: { color: c.text2, fontSize: 11, fontFamily: FONT_UI },
        axisLine: { show: false },
        axisTick: { show: false },
        axisLabel: { ...tickStyle(c), formatter: (v: number) => fmtUsdTick(v) },
        splitLine: { lineStyle: { color: c.split, width: 1 } },
      },
      series: [
        {
          name: 'Price-only',
          type: 'scatter' as const,
          // series color drives the legend swatch; per-point itemStyle draws the marks
          color: c.frontier,
          data: priceOnly.map((p) => pt(p, c.frontier, false)),
          z: 2,
        },
        {
          name: 'Performance-tested',
          type: 'scatter' as const,
          color: cat[0],
          data: tested.map((p) => pt(p, cat[0], p.panel)),
          labelLayout: { hideOverlap: true },
          z: 3,
        },
      ],
    };
  }, [data.pricing, c, cat, showPriceOnly]);

  return (
    <div className="stack">
      <section className="card">
        <div className="card-head">
          <div>
            <span className="figure-kicker">Figure 12 · <em>Interactive</em></span>
            <h1>Pricing landscape</h1>
          </div>
          <div className="chips" aria-label="Summary statistics">
            <span className="chip"><b>{counts.total}</b> priced models</span>
            <span className="chip"><b>{counts.tested}</b> performance-tested</span>
            <span className="chip"><b>{Math.round(counts.spanIn)}×</b> input-price spread</span>
          </div>
        </div>
        <p className="lead" style={{ marginBottom: 12 }}>
          The full candidate field the study drew from: input vs output token price for every model
          with a published price. Only <b>{counts.tested}</b> of the <b>{counts.total}</b> carry a
          measured oracle score (iris); the rest are shown in grey as <em>price-only</em> — they
          have no performance number, so they never appear on a quality axis.
        </p>
        <div className="controls">
          <label className="check">
            <input
              type="checkbox"
              checked={showPriceOnly}
              onChange={(e) => setShowPriceOnly(e.target.checked)}
            />
            Show price-only models (no oracle score)
          </label>
        </div>
        <EChart
          option={option}
          height={460}
          ariaLabel="Input versus output token price for all priced candidate models; data table below"
        />
        <div className="key-bar">
          <span>Log–log axes · both prices in USD per 1M tokens</span>
          <span>
            <b>ring</b> = selected oracle panel · most models charge more for output than input
          </span>
        </div>
        <FigureData
          summary={`View pricing data (${data.pricing.length} models)`}
          columns={['Model', 'Lab', 'Input $/1M', 'Output $/1M', 'Tested', 'Oracle F1']}
          numeric={[2, 3, 5]}
          rows={[...data.pricing]
            .sort((a, b) => a.inputPer1m - b.inputPer1m)
            .map((p) => [
              <code className="model-id" key={p.model}>{p.model}</code>,
              p.lab,
              fmtPer1m(p.inputPer1m),
              fmtPer1m(p.outputPer1m),
              p.tested ? '✓' : '—',
              p.f1 != null ? p.f1.toFixed(3) : '—',
            ])}
        />
      </section>
    </div>
  );
}
