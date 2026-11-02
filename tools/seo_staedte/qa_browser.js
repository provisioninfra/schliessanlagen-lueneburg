// Funktionstest je Stadtseite: Lottie gerendert, Karussell-Slides, Video spielt, Akkordeon klappt, Einblend-Animationen laufen, Konsolenfehler; Screenshots desktop/mobil
const { chromium } = require('playwright'); const fs = require('fs');
const slugs = process.argv.slice(2);
const SITE = 'https://provision-infra.de';
(async () => {
  const browser = await chromium.launch();
  const results = {};
  for (const slug of slugs) {
    results[slug] = {};
    for (const [label, vp, mobile] of [['desktop', { width: 1440, height: 900 }, false], ['mobil', { width: 390, height: 844 }, true]].filter(v => !process.env.QA_VIEWPORTS || process.env.QA_VIEWPORTS.split(',').includes(v[0]))) {
      const ctx = await browser.newContext({ viewport: vp, isMobile: mobile, hasTouch: mobile, deviceScaleFactor: 1, ignoreHTTPSErrors: true, userAgent: mobile ? 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1' : undefined });
      const page = await ctx.newPage(); const errors = []; const failed = [];
      page.on('console', m => { if (m.type() === 'error') errors.push(m.text().slice(0, 120)); });
      page.on('requestfailed', r => failed.push(r.url().slice(0, 100)));
      page.on('response', r => { if (r.status() >= 400 && r.url().includes('provision-infra.de')) failed.push(r.status() + ' ' + r.url().slice(0, 100)); });
      const t0 = Date.now();
      try { await page.goto(`${SITE}/${slug}/`, { waitUntil: 'load', timeout: 120000 }); } catch (e) { results[slug][label] = { error: 'goto: ' + e.message.slice(0, 80) }; await ctx.close(); continue; }
      await page.waitForTimeout(4000);
      // Borlabs-Box schließen, falls vorhanden (nur für Screenshots)
      await page.evaluate(() => { const b = document.querySelector('#BorlabsCookieBox'); if (b) b.style.display = 'none'; });
      const invisibleBefore = await page.evaluate(() => document.querySelectorAll('.elementor-invisible').length);
      // durchscrollen, damit Einblend-Animationen auslösen
      const h = await page.evaluate(() => document.body.scrollHeight);
      for (let y = 0; y < h; y += Math.round(vp.height * 0.7)) { await page.evaluate(yy => window.scrollTo(0, yy), y); await page.waitForTimeout(250); }
      await page.waitForTimeout(1500);
      const r = await page.evaluate(() => {
        const q = s => document.querySelectorAll(s).length;
        const vids = [...document.querySelectorAll('video')].map(v => ({ src: (v.currentSrc || v.src || '').split('/').pop(), ready: v.readyState, t: Math.round(v.currentTime * 10) / 10, paused: v.paused, visible: !!(v.offsetWidth || v.offsetHeight || v.getClientRects().length) }));
        return {
          h1: [...document.querySelectorAll('h1')].map(e => e.innerText.replace(/\s+/g, ' ').trim()),
          lottieWidgets: q('.elementor-widget-lottie'), lottieSvg: q('.elementor-widget-lottie svg'),
          slides: q('.e-n-carousel .swiper-slide'), slidesActive: q('.e-n-carousel .swiper-slide-active'),
          accordionItems: q('.eael-adv-accordion .eael-accordion-list'), faqHeaders: q('.eael-accordion-header'),
          videos: vids, invisibleAfter: q('.elementor-invisible'), animated: q('.animated'),
          timeline: q('.eael-content-timeline'), productSlider: q('.c7-slider-viewport'),
          ctaLinks: [...document.querySelectorAll('a[href*="anfrage-auswahl"]')].length,
          tel: q('a[href^="tel:"]'), schema: q('script[type="application/ld+json"]'),
          scrollH: document.body.scrollHeight, overflowX: document.documentElement.scrollWidth > document.documentElement.clientWidth,
        };
      });
      // Akkordeon: ersten Eintrag klicken
      let accordion = null;
      try {
        const hdr = page.locator('.eael-accordion-header').first(); await hdr.scrollIntoViewIfNeeded(); await hdr.click({ timeout: 5000 }); await page.waitForTimeout(800);
        accordion = await page.evaluate(() => { const c = document.querySelector('.eael-accordion-content'); const hd = document.querySelector('.eael-accordion-header'); return { open: !!(c && (c.offsetHeight > 0)), aria: hd && hd.getAttribute('aria-expanded') }; });
      } catch (e) { accordion = { error: e.message.slice(0, 60) }; }
      await page.evaluate(() => window.scrollTo(0, 0)); await page.waitForTimeout(500);
      fs.mkdirSync('shots', { recursive: true });
      await page.screenshot({ path: `shots/${slug}_${label}.png`, fullPage: true }).catch(() => {});
      results[slug][label] = { ...r, invisibleBefore, accordion, errors: [...new Set(errors)].slice(0, 5), failed: [...new Set(failed)].slice(0, 5), loadMs: Date.now() - t0 };
      console.log(slug, label, JSON.stringify(results[slug][label]));
      await ctx.close();
    }
  }
  fs.writeFileSync('qa_browser.json', JSON.stringify(results, null, 1));
  await browser.close();
})().catch(e => { console.error('FAILED', e); process.exit(1); });
