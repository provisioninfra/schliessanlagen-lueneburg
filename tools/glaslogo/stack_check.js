const { chromium } = require('playwright');
const targets = [['', 'f86d566'], ['lueneburg/', '4a79ecb'], ['zutrittssystem/', '14d56a01'], ['kamerasysteme/', '74b6d54']];
(async () => {
  const browser = await chromium.launch();
  for (const w of [390, 430, 768, 820, 844, 1024, 1280]) {
    const ctx = await browser.newContext({ viewport: { width: w, height: 900 }, ignoreHTTPSErrors: true }); const page = await ctx.newPage(); const row = [];
    for (const [slug, cid] of targets) {
      await page.goto('https://provision-infra.de/' + slug, { waitUntil: 'load', timeout: 120000 }); await page.waitForTimeout(1200);
      const r = await page.evaluate(id => { const el = document.querySelector(`[data-id="${id}"]`); if (!el) return null; const kids = [...el.children].filter(c => c.offsetHeight > 0); const boxes = kids.map(c => c.getBoundingClientRect());
        const stacked = boxes.length > 1 && boxes.every((b, i) => i === 0 || b.top >= boxes[i - 1].bottom - 2); const cs = getComputedStyle(el, '::before');
        return { h: Math.round(el.getBoundingClientRect().height), kids: kids.length, stacked, pos: cs.backgroundPosition, size: cs.backgroundSize, op: cs.opacity }; }, cid);
      row.push(`${(slug || 'start').padEnd(15)} h=${r && r.h} kids=${r && r.kids} ${r && r.stacked ? 'GESTAPELT' : 'nebeneinander'} pos=${r && r.pos} size=${r && r.size} op=${r && r.op}`);
    }
    console.log(`--- ${w}px ---\n  ` + row.join('\n  ')); await ctx.close();
  }
  await browser.close();
})().catch(e => { console.error('FAILED', e); process.exit(1); });
