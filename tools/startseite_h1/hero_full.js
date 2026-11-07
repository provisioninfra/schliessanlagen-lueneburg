const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  for (const [name, w, h, clipH] of [['pc-1920', 1920, 1080, 1500], ['pc-1440', 1440, 900, 1300]]) {
    const ctx = await browser.newContext({ viewport: { width: w, height: h }, ignoreHTTPSErrors: true }); const page = await ctx.newPage();
    await page.goto('https://provision-infra.de/', { waitUntil: 'load', timeout: 120000 }); await page.waitForTimeout(4000);
    await page.evaluate(() => { const b = document.querySelector('#BorlabsCookieBox'); if (b) b.style.display = 'none'; window.scrollTo(0, 400); });
    await page.waitForTimeout(1500); await page.evaluate(() => window.scrollTo(0, 0)); await page.waitForTimeout(800);
    const r = await page.evaluate(() => { const hero = document.querySelector('h1').closest('[data-element_type="container"]'); let top = hero; while (top.parentElement && top.parentElement.closest('[data-element_type="container"]')) top = top.parentElement.closest('[data-element_type="container"]');
      const b = top.getBoundingClientRect(); const next = top.nextElementSibling; const nb = next ? next.getBoundingClientRect() : null;
      return { heroTopId: top.dataset.id, heroHeight: Math.round(b.height), heroBottom: Math.round(b.bottom + scrollY), nextId: next && next.dataset.id, nextTop: nb && Math.round(nb.top + scrollY), overflowX: document.documentElement.scrollWidth > document.documentElement.clientWidth }; });
    await page.screenshot({ path: `${__dirname}/shots/nachher-hero-full_${name}.png`, fullPage: true, clip: { x: 0, y: 0, width: w, height: clipH } });
    console.log(name, JSON.stringify(r)); await ctx.close();
  }
  await browser.close();
})().catch(e => { console.error('FAILED', e); process.exit(1); });
