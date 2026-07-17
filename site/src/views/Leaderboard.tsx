import { useEffect, useMemo, useRef, useState } from 'react';
import type { Data, ModelRow } from '../types';
import { fmtUsd } from '../chart';

type SortKey = 'model' | 'lab' | 'yi' | 'f1' | 'cost' | 'reasoning' | 'fail';
type Dir = 'asc' | 'desc';

const COLS: { key: SortKey; label: string; num: boolean }[] = [
  { key: 'model', label: 'Model', num: false },
  { key: 'lab', label: 'Lab', num: false },
  { key: 'yi', label: 'YI', num: true },
  { key: 'f1', label: 'F1', num: true },
  { key: 'cost', label: '$/run', num: true },
  { key: 'reasoning', label: 'Reason.', num: true },
  { key: 'fail', label: 'Fail', num: true },
];

export function Leaderboard({ data }: { data: Data }) {
  const [q, setQ] = useState('');
  const [sortKey, setSortKey] = useState<SortKey>('yi');
  const [dir, setDir] = useState<Dir>('desc');
  const searchRef = useRef<HTMLInputElement | null>(null);

  // keyboard-first: "/" focuses the filter from anywhere in the view
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key !== '/' || e.ctrlKey || e.metaKey || e.altKey) return;
      const t = e.target as HTMLElement | null;
      if (t && (/^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName) || t.isContentEditable)) return;
      e.preventDefault();
      searchRef.current?.focus();
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, []);

  const maxYi = useMemo(() => Math.max(...data.models.map((m) => m.yi)), [data.models]);

  // stable YI rank per model — the "#" column doesn't renumber on sort or filter
  const yiRank = useMemo(() => {
    const byYi = [...data.models].sort((a, b) => b.yi - a.yi);
    return new Map(byYi.map((m, i) => [m.model, i + 1]));
  }, [data.models]);

  const rows = useMemo(() => {
    const needle = q.trim().toLowerCase();
    const filtered = data.models.filter(
      (m) => !needle || m.model.toLowerCase().includes(needle) || m.lab.toLowerCase().includes(needle),
    );
    const get = (m: ModelRow): string | number | null => m[sortKey];
    return [...filtered].sort((a, b) => {
      const av = get(a);
      const bv = get(b);
      if (av == null && bv == null) return 0;
      if (av == null) return 1; // nulls last
      if (bv == null) return -1;
      const cmp = typeof av === 'number' && typeof bv === 'number'
        ? av - bv
        : String(av).localeCompare(String(bv));
      return dir === 'asc' ? cmp : -cmp;
    });
  }, [data.models, q, sortKey, dir]);

  const onSort = (k: SortKey) => {
    if (k === sortKey) setDir((d) => (d === 'asc' ? 'desc' : 'asc'));
    else {
      setSortKey(k);
      setDir(k === 'model' || k === 'lab' ? 'asc' : 'desc');
    }
  };
  const arrow = (k: SortKey) => (k === sortKey ? (dir === 'asc' ? '▲' : '▼') : '');
  const numCls = (k: SortKey) => `num${k === sortKey ? ' sorted' : ''}`;

  return (
    <div className="stack">
      <section className="card">
        <div className="card-head">
          <div>
            <span className="figure-kicker">Table 2 · <em>Interactive</em></span>
            <h1>Oracle leaderboard</h1>
          </div>
          <span className="meta">
            {rows.length} of {data.models.length} models · <code>human-mouse</code>
          </span>
        </div>
        <span className="sr-only" aria-live="polite">
          {`Sorted by ${COLS.find((col) => col.key === sortKey)?.label ?? sortKey}, ${dir === 'asc' ? 'ascending' : 'descending'}. ${rows.length} of ${data.models.length} models shown.`}
        </span>
        <div className="controls">
          <div className="control" style={{ flex: 1, minWidth: 220 }}>
            <label className="control-label" htmlFor="lb-search">Search</label>
            <div className="search-wrap">
              <svg className="search-icon" viewBox="0 0 14 14" fill="none" aria-hidden="true">
                <circle cx="6" cy="6" r="4.4" stroke="currentColor" strokeWidth="1.3" />
                <path d="M9.4 9.4 12.8 12.8" stroke="currentColor" strokeWidth="1.3" strokeLinecap="round" />
              </svg>
              <input
                id="lb-search"
                ref={searchRef}
                className="ctrl"
                type="search"
                placeholder="filter by model or lab…"
                value={q}
                onChange={(e) => setQ(e.target.value)}
              />
              <kbd aria-hidden="true">/</kbd>
            </div>
          </div>
        </div>
        <div className="table-wrap" tabIndex={0} role="region" aria-label="Oracle leaderboard table">
          <table className="data">
            <thead>
              <tr>
                <th className="rank" aria-label="Rank by Youden's J">#</th>
                {COLS.map((col) => (
                  <th
                    key={col.key}
                    className={col.num ? 'num' : undefined}
                    aria-sort={col.key === sortKey ? (dir === 'asc' ? 'ascending' : 'descending') : 'none'}
                  >
                    <button onClick={() => onSort(col.key)}>
                      {col.label} <span className="sort-arrow" aria-hidden="true">{arrow(col.key)}</span>
                    </button>
                  </th>
                ))}
                <th>Flags</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((m) => (
                <tr key={m.model} className={m.panel ? 'is-panel' : undefined}>
                  <td className="rank">{yiRank.get(m.model)}</td>
                  <td><code className="model-id">{m.model}</code></td>
                  <td>{m.lab}</td>
                  <td className={numCls('yi')}>
                    <span className="yi-wrap">
                      <span
                        className="yi-fill"
                        aria-hidden="true"
                        style={{ width: `${Math.max(0, (m.yi / maxYi) * 100)}%` }}
                      />
                      <span className="yi-num">{m.yi.toFixed(3)}</span>
                    </span>
                  </td>
                  <td className={numCls('f1')}>{m.f1 != null ? m.f1.toFixed(3) : '—'}</td>
                  <td className={numCls('cost')}>{fmtUsd(m.cost)}</td>
                  <td
                    className={numCls('reasoning')}
                    title={m.reasoning === 0 ? 'Measured billing zero: $0 of reasoning tokens itemised for this run' : undefined}
                  >
                    {m.reasoning != null ? `${Math.round(m.reasoning * 100)}%` : '—'}
                  </td>
                  <td className={numCls('fail')}>{m.fail != null ? `${(m.fail * 100).toFixed(1)}%` : '—'}</td>
                  <td>
                    {m.panel && <span className="badge panel">panel</span>}
                    {m.pareto && <span className="badge">Pareto</span>}
                    {m.efficiency && <span className="badge good">★ efficient</span>}
                    {m.poorValue && <span className="badge bad">✗ costly</span>}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
      <p className="footnote">
        YI/cost from Sviatoslav&apos;s <code>human-mouse</code> board (18 models with a measured
        oracle score). F1 / reasoning / fail-rate are available for the subset with a full cost
        breakdown. Highlighted rows are our selected panel models; <b>#</b> is the fixed YI rank
        and the <b>Pareto</b> badge marks the YI–cost frontier. A <b>0%</b> reasoning share is a
        measured billing zero (the itemised breakdown records $0 of reasoning tokens for that run);
        unmeasured values show as “—”.
      </p>
    </div>
  );
}
