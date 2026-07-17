// Headless smoke test: serve dist/, load every view, fail on any console/page error, screenshot.
import http from 'node:http';
import { readFile } from 'node:fs/promises';
import { existsSync, mkdirSync } from 'node:fs';
import { join, extname, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import puppeteer from 'puppeteer';

const here = dirname(fileURLToPath(import.meta.url));
const dist = join(here, '..', 'dist');
const shots = join(here, '..', 'screenshots');
mkdirSync(shots, { recursive: true });
if (!existsSync(join(dist, 'index.html'))) {
  console.error('dist/ not built — run `npm run build` first.');
  process.exit(1);
}

const MIME = {
  '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css',
  '.json': 'application/json', '.csv': 'text/csv', '.svg': 'image/svg+xml', '.ico': 'image/x-icon',
};
const server = http.createServer(async (req, res) => {
  let p = decodeURIComponent((req.url || '/').split('?')[0]);
  if (p === '/') p = '/index.html';
  let file = join(dist, p);
  if (!existsSync(file)) file = join(dist, 'index.html');
  try {
    const buf = await readFile(file);
    res.writeHead(200, { 'Content-Type': MIME[extname(file)] || 'application/octet-stream' });
    res.end(buf);
  } catch {
    res.writeHead(404); res.end('not found');
  }
});
const PORT = 4178;
await new Promise((r) => server.listen(PORT, r));
const base = `http://localhost:${PORT}/`;

const browser = await puppeteer.launch({ headless: true, args: ['--no-sandbox', '--disable-setuid-sandbox'] });
const page = await browser.newPage();
await page.setViewport({ width: 1320, height: 920, deviceScaleFactor: 2 });

const errors = [];
page.on('console', (m) => { if (m.type() === 'error') errors.push('console: ' + m.text()); });
page.on('pageerror', (e) => errors.push('pageerror: ' + e.message));

const clickTab = (label) =>
  page.evaluate((lbl) => {
    const b = [...document.querySelectorAll('[role=tab]')].find((x) => x.textContent.trim() === lbl);
    if (b) b.click();
    return !!b;
  }, label);
const wait = (ms) => new Promise((r) => setTimeout(r, ms));

// tab order matches the app: light shots 1-6, dark shots 7-12
const TABS = ['Overview', 'Leaderboard', 'Trade-offs', 'Configuration', 'Value', 'Pricing'];
const slug = (label) => label.toLowerCase().replace(/ /g, '-');

try {
  // the interactive explorer now lives at app.html (index.html is the classic view)
  await page.goto(base + 'app.html', { waitUntil: 'networkidle0', timeout: 30000 });
  await page.waitForSelector('table.data', { timeout: 20000 }); // data loaded
  await page.waitForSelector('canvas', { timeout: 20000 }); // a chart rendered
  await wait(700);

  const rendered = [];
  for (const [themeIdx, themeName] of [[0, ''], [1, '-dark']]) {
    if (themeIdx === 1) {
      await clickTab('Overview');
      await wait(300);
      await page.click('.icon-btn'); // toggle to dark
      await wait(800);
    }
    for (const [i, label] of TABS.entries()) {
      const ok = await clickTab(label);
      if (!ok) throw new Error(`tab not found: ${label}`);
      await wait(900);
      const n = themeIdx * TABS.length + i + 1;
      await page.screenshot({ path: join(shots, `${n}-${slug(label)}${themeName}.png`), fullPage: true });
      rendered.push(slug(label) + themeName);
    }
  }

  console.log('views rendered:', rendered.join(', '));
} finally {
  await browser.close();
  server.close();
}

if (errors.length) {
  console.error('SMOKE FAILED — console/page errors:\n' + errors.map((e) => '  • ' + e).join('\n'));
  process.exit(1);
}
console.log('SMOKE OK — screenshots in screenshots/');
