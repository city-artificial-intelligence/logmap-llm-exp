import type { ReactNode } from 'react';

interface Props {
  summary: string;
  columns: string[];
  /** column indexes that are numeric (right-aligned, tabular) */
  numeric?: number[];
  rows: ReactNode[][];
}

/** Collapsible data twin for a figure — every charted value, reachable without hover. */
export function FigureData({ summary, columns, numeric = [], rows }: Props) {
  const numSet = new Set(numeric);
  return (
    <details className="table-twin">
      <summary>{summary}</summary>
      {/* focusable region: the table can overflow horizontally, and a scrollable
          area must be reachable and scrollable from the keyboard */}
      <div className="table-wrap" tabIndex={0} role="region" aria-label={summary}>
        <table className="data">
          <thead>
            <tr>
              {columns.map((col, i) => (
                <th key={col} className={numSet.has(i) ? 'num' : undefined}>{col}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((r, ri) => (
              <tr key={ri}>
                {r.map((cell, ci) => (
                  <td key={ci} className={numSet.has(ci) ? 'num' : undefined}>{cell}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </details>
  );
}
