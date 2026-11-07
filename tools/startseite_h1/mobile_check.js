// Echte Mobil-UA-Prüfung einzelner Viewports (ein Aufruf je Lauf, Abstand von außen)
const { chromium } = require('playwright'); const fs = require('fs');
const [name, w, h] = [process.argv[2], Number(process.argv[3]), Number(process.argv[4])];
(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: w, height: h }, isMobile: true, hasTouch: true, deviceScaleFactor: 2, ignoreHTTPSErrors: true, userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1' });
  const page = await ctx.newPage(); await page.goto('https://provision-infra.de/', { waitUntil: 'load', timeout: 120000 }); await page.waitForTimeout(4000);
  await page.evaluate(() => { const b = document.querySelector('#BorlabsCookieBox'); if (b) b.style.display = 'none'; });
  const r = await page.evaluate(() => { const h1 = document.querySelector('h1'); const cs = getComputedStyle(h1); const b = h1.getBoundingClientRect();
    const vid = [...document.querySelectorAll('video')].filter(v => v.offsetWidth).map(v => ({ src: (v.currentSrc || '').split('/').pop().slice(0, 30), ready: v.readyState }));
    return { title: document.title.slice(0, 40), font: cs.fontSize, lh: cs.lineHeight, lines: Math.round(b.height / parseFloat(cs.lineHeight)), w: Math.round(b.width), h: Math.round(b.height), overflowX: document.documentElement.scrollWidth > document.documentElement.clientWidth, video: vid, invisible: document.querySelectorAll('.elementor-invisible').length, animated: document.querySelectorAll('.animated').length }; });
  await page.screenshot({ path: `${__dirname}/shots/mobilua_${name}.png`, clip: { x: 0, y: 0, width: w, height: Math.min(h, 900) } });
  console.log(name, JSON.stringify(r)); await browser.close();
})().catch(e => { console.error('FAILED', e); process.exit(1); });
