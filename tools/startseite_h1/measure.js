// Misst die Hero-H1 der Startseite je Viewport: Schriftgröße, Zeilenhöhe, Zeilenzahl, Box, Überlauf, Abstand zur nächsten Zeile
const { chromium } = require('playwright'); const fs = require('fs');
const URL = process.argv[2] || 'https://provision-infra.de/';
const DESKTOP_UA = !!process.env.DESKTOP_UA;
const VIEWS = [['pc-1920', 1920, 1080, false], ['pc-1440', 1440, 900, false], ['laptop-1366', 1366, 768, false], ['laptop-1280', 1280, 720, false], ['tablet-quer-1024', 1024, 768, true], ['tablet-hoch-768', 768, 1024, true], ['tablet-hoch-820', 820, 1180, true], ['phone-hoch-390', 390, 844, true], ['phone-hoch-430', 430, 932, true], ['phone-hoch-360', 360, 780, true], ['phone-quer-844', 844, 390, true], ['phone-quer-932', 932, 430, true]];
(async () => {
  const browser = await chromium.launch(); const out = {};
  for (const [name, w, h, mobile] of VIEWS) {
    const ctx = await browser.newContext({ viewport: { width: w, height: h }, isMobile: mobile && !DESKTOP_UA, hasTouch: mobile && !DESKTOP_UA, deviceScaleFactor: 1, ignoreHTTPSErrors: true,
      userAgent: (mobile && !DESKTOP_UA) ? 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1' : undefined });
    const page = await ctx.newPage();
    try { await page.goto(URL, { waitUntil: 'load', timeout: 120000 }); } catch (e) { out[name] = { error: e.message.slice(0, 80) }; await ctx.close(); continue; }
    await page.waitForTimeout(3500);
    await page.evaluate(() => { const b = document.querySelector('#BorlabsCookieBox'); if (b) b.style.display = 'none'; });
    const r = await page.evaluate(() => {
      const h1s = [...document.querySelectorAll('h1')].filter(e => e.offsetParent !== null || e.getClientRects().length);
      const h1 = h1s[0]; if (!h1) return { noH1: true, count: document.querySelectorAll('h1').length };
      const cs = getComputedStyle(h1); const box = h1.getBoundingClientRect();
      const lines = Math.round(box.height / parseFloat(cs.lineHeight));
      // nächstes sichtbares Element unterhalb der H1 (Subline)
      let next = h1.closest('.elementor-element'); let nextBox = null, nextText = '';
      let sib = next && next.nextElementSibling; while (sib && !(sib.offsetWidth || sib.offsetHeight)) sib = sib.nextElementSibling;
      if (sib) { nextBox = sib.getBoundingClientRect(); nextText = sib.innerText.trim().slice(0, 40); }
      const wrapper = h1.closest('.elementor-widget-heading');
      return { text: h1.innerText.replace(/\s+/g, ' ').trim(), fontSize: cs.fontSize, lineHeight: cs.lineHeight, fontWeight: cs.fontWeight, lines, width: Math.round(box.width), height: Math.round(box.height), top: Math.round(box.top), right: Math.round(box.right), vw: innerWidth,
        overflowX: document.documentElement.scrollWidth > document.documentElement.clientWidth, h1ScrollOverflow: h1.scrollWidth > h1.clientWidth + 1, widgetId: wrapper && wrapper.dataset.id, widgetClasses: wrapper && wrapper.className.slice(0, 120),
        gapToNext: nextBox ? Math.round(nextBox.top - box.bottom) : null, nextText, animated: h1.closest('.animated, .elementor-invisible') ? h1.closest('.animated, .elementor-invisible').className.split(' ').filter(c => /animated|elementor-invisible|fadeIn/.test(c)).join(' ') : '' };
    });
    fs.mkdirSync(__dirname + '/shots', { recursive: true });
    await page.screenshot({ path: `${__dirname}/shots/${process.argv[3] || 'vorher'}_${name}.png`, clip: { x: 0, y: 0, width: w, height: Math.min(h, 900) } }).catch(() => {});
    out[name] = r; console.log(name.padEnd(17), JSON.stringify(r));
    await ctx.close();
  }
  fs.writeFileSync(`${__dirname}/measure_${process.argv[3] || 'vorher'}.json`, JSON.stringify(out, null, 1));
  await browser.close();
})().catch(e => { console.error('FAILED', e); process.exit(1); });
