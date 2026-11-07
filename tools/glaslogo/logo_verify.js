// Prüft je Seite: ::before des Ziel-Containers bei 390 (2 Logos), 844 und 1440 (unverändert 1 Logo), horizontaler Überlauf
const { chromium } = require('playwright');
const pages = JSON.parse(process.argv[2]); // [[slug, cid], ...]
(async () => {
  const browser = await chromium.launch();
  for (const [slug, cid] of pages) {
    const row = [];
    for (const w of [390, 844, 1440]) {
      const ctx = await browser.newContext({ viewport: { width: w, height: 900 }, ignoreHTTPSErrors: true }); const page = await ctx.newPage();
      try {
        await page.goto('https://provision-infra.de/' + slug + '?pvcheck=' + Date.now(), { waitUntil: 'load', timeout: 120000 }); await page.waitForTimeout(800);
        const r = await page.evaluate(id => { const el = document.querySelector(`[data-id="${id}"]`); if (!el) return null; el.scrollIntoView(); return new Promise(res => setTimeout(() => { const cs = getComputedStyle(el, '::before'); res({ urls: (cs.backgroundImage.match(/url\(/g) || []).length, pos: cs.backgroundPosition, op: cs.opacity, h: Math.round(el.getBoundingClientRect().height), overflow: document.documentElement.scrollWidth > document.documentElement.clientWidth }); }, 900)); }, cid);
        row.push(`${w}: ${r ? `${r.urls} Logo(s) pos=${r.pos} op=${r.op} h=${r.h}${r.overflow ? ' ÜBERLAUF' : ''}` : 'Element fehlt'}`);
      } catch (e) { row.push(`${w}: FEHLER ${e.message.slice(0, 50)}`); }
      await ctx.close(); await new Promise(r => setTimeout(r, 3000));
    }
    console.log((slug || 'startseite').padEnd(16), row.join(' | '));
  }
  await browser.close();
})().catch(e => { console.error('FAILED', e); process.exit(1); });
