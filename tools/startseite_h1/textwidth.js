const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch(); const ctx = await browser.newContext({ viewport: { width: 1920, height: 1080 }, ignoreHTTPSErrors: true }); const page = await ctx.newPage();
  await page.goto('https://provision-infra.de/', { waitUntil: 'load', timeout: 120000 }); await page.waitForTimeout(3000);
  const r = await page.evaluate(async () => {
    await document.fonts.ready;
    const h1 = document.querySelector('h1'); const html = h1.innerHTML;
    const c = document.createElement('canvas').getContext('2d');
    const parts = { bold: 'Wir installieren in deinem Unternehmen', rest: 'ein digitales Schließsystem', all: 'Wir installieren in deinem Unternehmen ein digitales Schließsystem' };
    const out = { html: html.slice(0, 200), widths: {} };
    for (const px of [22, 24, 25, 26, 27, 35, 37, 40, 42, 52, 53, 54, 55]) {
      c.font = `700 ${px}px Poppins`; const wb = c.measureText(parts.bold).width;
      c.font = `400 ${px}px Poppins`; const wr = c.measureText(parts.rest).width; const wa = c.measureText(parts.all).width;
      out.widths[px] = { bold: Math.round(wb), rest: Math.round(wr), all_regular: Math.round(wa) };
    }
    const cs = getComputedStyle(h1); out.h1Width = Math.round(h1.getBoundingClientRect().width); out.fontCheck = document.fonts.check('700 52px Poppins');
    return out;
  });
  console.log(JSON.stringify(r)); await browser.close();
})().catch(e => { console.error('FAILED', e); process.exit(1); });
