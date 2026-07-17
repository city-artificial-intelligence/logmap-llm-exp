import { useEffect, useRef, useState, type KeyboardEvent as ReactKeyboardEvent } from 'react';
import { loadData } from './data';
import type { Data, Theme } from './types';
import { Overview } from './views/Overview';
import { Tradeoffs } from './views/Tradeoffs';
import { OracleValue } from './views/OracleValue';
import { Leaderboard } from './views/Leaderboard';
import { PricingLandscape } from './views/PricingLandscape';
import { Configuration } from './views/Configuration';

const TABS = [
  { id: 'overview', label: 'Overview' },
  { id: 'leaderboard', label: 'Leaderboard' },
  { id: 'tradeoffs', label: 'Trade-offs' },
  { id: 'config', label: 'Configuration' },
  { id: 'oracle', label: 'Value' },
  { id: 'pricing', label: 'Pricing' },
] as const;
type TabId = (typeof TABS)[number]['id'];

const BASE_TITLE = 'LogMapLLM Oracle — Cost/Benefit Explorer';
const isTabId = (v: string): v is TabId => TABS.some((t) => t.id === v);
const tabFromHash = (): TabId => {
  const h = window.location.hash.replace(/^#\/?/, '');
  return isTabId(h) ? h : 'overview';
};

function useTheme(): [Theme, () => void] {
  const [theme, setTheme] = useState<Theme>(() => {
    let saved: string | null = null;
    try {
      saved = localStorage.getItem('theme'); // throws when storage is blocked
    } catch {
      saved = null;
    }
    if (saved === 'light' || saved === 'dark') return saved;
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  });
  useEffect(() => {
    document.documentElement.dataset.theme = theme;
    document
      .querySelector('meta[name="theme-color"]')
      ?.setAttribute('content', theme === 'dark' ? '#0e0e11' : '#fafafa');
    try {
      localStorage.setItem('theme', theme);
    } catch {
      // storage blocked — the in-session theme still works
    }
  }, [theme]);
  return [theme, () => setTheme((t) => (t === 'dark' ? 'light' : 'dark'))];
}

const SunIcon = () => (
  <svg width="15" height="15" viewBox="0 0 15 15" fill="none" aria-hidden="true">
    <circle cx="7.5" cy="7.5" r="3.1" stroke="currentColor" strokeWidth="1.3" />
    <g stroke="currentColor" strokeWidth="1.3" strokeLinecap="round">
      <path d="M7.5 0.9v1.6M7.5 12.5v1.6M0.9 7.5h1.6M12.5 7.5h1.6M2.8 2.8l1.2 1.2M11 11l1.2 1.2M12.2 2.8L11 4M4 11l-1.2 1.2" />
    </g>
  </svg>
);
const MoonIcon = () => (
  <svg width="15" height="15" viewBox="0 0 15 15" fill="none" aria-hidden="true">
    <path
      d="M13 9.3A5.9 5.9 0 0 1 5.7 2 5.9 5.9 0 1 0 13 9.3Z"
      stroke="currentColor"
      strokeWidth="1.3"
      strokeLinejoin="round"
    />
  </svg>
);

export function App() {
  const [theme, toggleTheme] = useTheme();
  // deep-linkable views: #leaderboard, #tradeoffs, … survive reload and sharing
  const [tab, setTabState] = useState<TabId>(tabFromHash);
  const [data, setData] = useState<Data | null>(null);
  const [error, setError] = useState<string | null>(null);
  const tabRefs = useRef<Map<TabId, HTMLButtonElement>>(new Map());

  const setTab = (id: TabId) => {
    setTabState(id);
    if (tabFromHash() !== id) window.history.pushState(null, '', `#${id}`);
  };

  // back/forward (and hand-edited hashes) drive the view
  useEffect(() => {
    const onHash = () => setTabState(tabFromHash());
    window.addEventListener('hashchange', onHash);
    return () => window.removeEventListener('hashchange', onHash);
  }, []);

  // keep the document title and the scrolled-into-view tab in sync with the view.
  // scroll the strip directly (not scrollIntoView, which also moves the browser's
  // sequential-focus starting point and would make Tab skip the skip link)
  useEffect(() => {
    const label = TABS.find((t) => t.id === tab)?.label;
    document.title = tab === 'overview' ? BASE_TITLE : `${label} · ${BASE_TITLE}`;
    const btn = tabRefs.current.get(tab);
    const strip = btn?.closest('.tabs');
    if (btn && strip && strip.scrollWidth > strip.clientWidth) {
      const b = btn.getBoundingClientRect();
      const s = strip.getBoundingClientRect();
      if (b.left < s.left) strip.scrollLeft += b.left - s.left - 24;
      else if (b.right > s.right) strip.scrollLeft += b.right - s.right + 24;
    }
  }, [tab]);

  // complete the ARIA tabs contract: roving tabindex + arrow-key navigation
  const onTabKeyDown = (e: ReactKeyboardEvent) => {
    const idx = TABS.findIndex((t) => t.id === tab);
    let next = -1;
    if (e.key === 'ArrowRight') next = (idx + 1) % TABS.length;
    else if (e.key === 'ArrowLeft') next = (idx + TABS.length - 1) % TABS.length;
    else if (e.key === 'Home') next = 0;
    else if (e.key === 'End') next = TABS.length - 1;
    if (next < 0) return;
    e.preventDefault();
    const id = TABS[next].id;
    setTab(id);
    tabRefs.current.get(id)?.focus();
  };

  useEffect(() => {
    let alive = true;
    loadData(import.meta.env.BASE_URL)
      .then((d) => alive && setData(d))
      .catch((e: unknown) => alive && setError(e instanceof Error ? e.message : String(e)));
    return () => {
      alive = false;
    };
  }, []);

  return (
    <div className="app">
      {/* focus #main directly — letting the default #main navigation run would
          collide with the #<view> hash routing and bounce the view to Overview */}
      <a
        className="skip-link"
        href="#main"
        onClick={(e) => {
          e.preventDefault();
          document.getElementById('main')?.focus();
        }}
      >
        Skip to content
      </a>
      {/* the classic report view is the site's landing page (root index.html);
          a plain static page outside the SPA, so a real anchor, not hash routing */}
      <a className="classic-banner" href="./">
        <span className="classic-banner-text">Open in the classical view</span>
        <span className="classic-banner-arrow" aria-hidden="true">→</span>
      </a>
      <header className="header">
        <div className="header-inner">
          <div className="brand">
            <span className="logo-mark" aria-hidden="true" />
            <span className="brand-title">LogMapLLM Oracle</span>
            <span className="brand-dim">· Cost/Benefit Explorer</span>
          </div>
          <nav aria-label="Views">
            <div className="tabs" role="tablist" onKeyDown={onTabKeyDown}>
              {TABS.map((t) => (
                <button
                  key={t.id}
                  ref={(el) => {
                    if (el) tabRefs.current.set(t.id, el);
                    else tabRefs.current.delete(t.id);
                  }}
                  id={`tab-${t.id}`}
                  role="tab"
                  aria-selected={tab === t.id}
                  aria-controls={`panel-${t.id}`}
                  tabIndex={tab === t.id ? 0 : -1}
                  className="tab"
                  onClick={() => setTab(t.id)}
                >
                  {t.label}
                </button>
              ))}
            </div>
          </nav>
          <button
            className="icon-btn"
            onClick={toggleTheme}
            aria-label={`Switch to ${theme === 'dark' ? 'light' : 'dark'} theme`}
            title="Toggle theme"
          >
            {theme === 'dark' ? <SunIcon /> : <MoonIcon />}
          </button>
        </div>
      </header>

      <main className="main" id="main" tabIndex={-1}>
        {/* persistent live region: mounts empty, so state changes are announced */}
        <div className="sr-only" role="status" aria-live="polite">
          {error ? 'Failed to load the oracle data.' : !data ? 'Loading oracle data…' : 'Oracle data loaded.'}
        </div>
        {error ? (
          <div className="error card">
            <strong>Could not load the data.</strong>
            <span className="muted">{error}</span>
            <span className="note">
              Run <code>npm run dev</code> (or <code>npm run build &amp;&amp; npm run preview</code>) so the
              CSVs under <code>public/data/</code> are served.
            </span>
          </div>
        ) : !data ? (
          <div className="loading">
            <div className="skeleton skel-hero" aria-hidden="true" />
            <div className="skeleton skel-strip" aria-hidden="true" />
            <div className="skeleton skel-card" aria-hidden="true" />
          </div>
        ) : (
          <div
            className="view"
            key={tab}
            role="tabpanel"
            id={`panel-${tab}`}
            aria-labelledby={`tab-${tab}`}
            tabIndex={0}
          >
            {tab === 'overview' ? (
              <Overview data={data} theme={theme} />
            ) : tab === 'tradeoffs' ? (
              <Tradeoffs data={data} theme={theme} />
            ) : tab === 'oracle' ? (
              <OracleValue data={data} theme={theme} />
            ) : tab === 'leaderboard' ? (
              <Leaderboard data={data} />
            ) : tab === 'pricing' ? (
              <PricingLandscape data={data} theme={theme} />
            ) : (
              <Configuration data={data} theme={theme} />
            )}
          </div>
        )}
      </main>

      <footer className="footer">
        <div className="footer-inner">
          <p>
            Data: Sviatoslav Lushnei, Dmytro Shumskyi, &amp; Severyn Shykula oracle cost/benefit study (9 Bio-ML / anatomy / largebio tasks). 
            Cost = hosted API $/run on human-mouse; YI = Youden&apos;s J. The measured-cost board is 18 models.
            The trade-off &amp; configuration boards span wider than Anatomy human-mouse.
          </p>
          <p>
            Figures &amp; CSVs regenerable from{' '}
            <span className="path-chip">http://city-artificial-intelligence.github.io/logmap-llm-exp</span>
          </p>
        </div>
      </footer>
    </div>
  );
}
