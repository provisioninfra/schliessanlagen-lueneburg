// Nach vollständigem Durchscrollen (Lazy-Backgrounds): alle Elemente mit Hintergrundbild (auch ::before-Overlays), Position im Dokument, Höhe, Stapelung der Kinder
const { chromium } = require('playwright');
const pages = process.argv[2].split(','); const widths = (process.argv[3] || '390,768,1440').split(',').map(Number);
(async () => {
  const browser = await chromium.launch();
  for (const slug of pages) for (const w of widths) {
    const ctx = await browser.newContext({ viewport: { width: w, height: 900 }, ignoreHTTPSErrors: true }); const page = await ctx.newPage();
    await page.goto('https://provision-infra.de/' + slug, { waitUntil: 'load', timeout: 120000 }); await page.waitForTimeout(2000);
    const H = await page.evaluate(() => document.body.scrollHeight);
    for (let y = 0; y < H; y += 600) { await page.evaluate(yy => window.scrollTo(0, yy), y); await page.waitForTimeout(120); }
    await page.waitForTimeout(1500); await page.evaluate(() => window.scrollTo(0, 0)); await page.waitForTimeout(300);
    const r = await page.evaluate(() => {
      const out = []; const name = bi => (bi.match(/\/([^\/]+?)(?:\?[^)"']*)?["')]/) || [])[1];
      for (const el of document.querySelectorAll('[data-element_type="container"]')) {
        const b = el.getBoundingClientRect(); if (b.height < 40 || !b.width) continue;
        const layers = [];
        for (const [lab, cs] of [['bg', getComputedStyle(el)], ['before', getComputedStyle(el, '::before')]]) {
          const bi = cs.backgroundImage; if (bi && bi !== 'none' && /\.(png|webp|jpg|svg)/i.test(bi)) layers.push({ layer: lab, img: name(bi)?.slice(0, 36), pos: cs.backgroundPosition, size: cs.backgroundSize, repeat: cs.backgroundRepeat, opacity: lab === 'before' ? cs.opacity : '' });
        }
        if (!layers.length) continue;
        const kids = [...el.children].filter(c => c.offsetHeight > 0 && !c.classList.contains('elementor-background-overlay'));
        const stacked = kids.length > 1 && kids.every((c, i) => i === 0 || c.getBoundingClientRect().top >= kids[i - 1].getBoundingClientRect().bottom - 2);
        const top = el.closest('[data-element_type="container"]') === el && !el.parentElement.closest('[data-element_type="container"]');
        out.push({ id: el.dataset.id, top, y: Math.round(b.top + scrollY), h: Math.round(b.height), kids: kids.length, stacked, title: (el.querySelector('h1,h2,h3,.elementor-heading-title')?.innerText || '').replace(/\s+/g, ' ').slice(0, 38), layers });
      }
      return { H: document.body.scrollHeight, out };
    });
    console.log(`\n=== ${slug || 'startseite'} @ ${w}px (Seitenhöhe ${r.H}px) ===`);
    for (const x of r.out) console.log(`${x.top ? 'TOP' : '   '} ${x.id} y=${x.y} h=${x.h} kids=${x.kids}${x.stacked ? ' gestapelt' : ''} "${x.title}" ` + x.layers.map(l => `[${l.layer}:${l.img} ${l.size} ${l.pos} ${l.repeat}${l.opacity ? ' op=' + l.opacity : ''}]`).join(' '));
    await ctx.close();
  }
  await browser.close();
})().catch(e => { console.error('FAILED', e); process.exit(1); });
