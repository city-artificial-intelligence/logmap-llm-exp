import { useEffect, useRef, useState } from 'react';
import * as echarts from 'echarts/core';
import { BarChart, HeatmapChart, LineChart, ScatterChart } from 'echarts/charts';
import {
  GridComponent, LegendComponent, MarkLineComponent, TooltipComponent, VisualMapComponent,
} from 'echarts/components';
import { LabelLayout } from 'echarts/features';
import { CanvasRenderer } from 'echarts/renderers';
import type { EChartsOption } from 'echarts';

// Modular registration: only the chart/component types the views actually use
// ship in the bundle (the monolithic 'echarts' entry is ~65% dead weight here).
echarts.use([
  BarChart, HeatmapChart, LineChart, ScatterChart,
  GridComponent, LegendComponent, MarkLineComponent, TooltipComponent, VisualMapComponent,
  LabelLayout, CanvasRenderer,
]);

interface Props {
  option: EChartsOption;
  height?: number | string;
  ariaLabel?: string;
}

/** Thin, self-managing wrapper around an ECharts instance (init once, setOption on change,
 *  resize with the container, dispose on unmount). setOption uses notMerge so control
 *  toggles produce a clean redraw. Re-renders once the web fonts finish loading so canvas
 *  text picks them up. */
export function EChart({ option, height = 380, ariaLabel }: Props) {
  const ref = useRef<HTMLDivElement | null>(null);
  const inst = useRef<echarts.EChartsType | null>(null);
  const [fontsReady, setFontsReady] = useState(
    () => typeof document === 'undefined' || !('fonts' in document) || document.fonts.status === 'loaded',
  );

  useEffect(() => {
    if (!ref.current) return;
    const chart = echarts.init(ref.current, undefined, { renderer: 'canvas' });
    inst.current = chart;
    const ro = new ResizeObserver(() => chart.resize());
    ro.observe(ref.current);
    return () => {
      ro.disconnect();
      chart.dispose();
      inst.current = null;
    };
  }, []);

  useEffect(() => {
    if (fontsReady) return;
    let alive = true;
    document.fonts.ready.then(() => alive && setFontsReady(true));
    return () => {
      alive = false;
    };
  }, [fontsReady]);

  useEffect(() => {
    inst.current?.setOption(option, true);
  }, [option, fontsReady]);

  return (
    <div
      ref={ref}
      role="img"
      aria-label={ariaLabel}
      style={{ width: '100%', height }}
    />
  );
}
