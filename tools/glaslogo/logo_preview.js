// Vorschau ohne Serveränderung: zweite Glas-Logo-Instanz per injiziertem CSS, Screenshot des Abschnitts
const { chromium } = require('playwright'); const fs = require('fs');
const [slug, cid, pos2, w] = [process.argv[2] || '', process.argv[3] || 'f86d566', process.argv[4] || '60%', Number(process.argv[5] || 390)];
(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: w, height: 844 }, deviceScaleFactor: Number(process.env.DSF || 1), ignoreHTTPSErrors: true }); const page = await ctx.newPage();
  await page.goto('https://provision-infra.de/' + slug, { waitUntil: 'load', timeout: 120000 }); await page.waitForTimeout(2000);
  const H = await page.evaluate(() => document.body.scrollHeight);
  for (let y = 0; y < H; y += 600) { await page.evaluate(yy => window.scrollTo(0, yy), y); await page.waitForTimeout(100); }
  await page.waitForTimeout(1200);
  const info = await page.evaluate(id => { const el = document.querySelector(`[data-id="${id}"]`); const cs = getComputedStyle(el, '::before'); const b = el.getBoundingClientRect(); return { img: cs.backgroundImage.slice(0, 160), pos: cs.backgroundPosition, size: cs.backgroundSize, op: cs.opacity, top: Math.round(b.top + scrollY), h: Math.round(b.height), w: Math.round(b.width) }; }, cid);
  const url = (info.img.match(/url\("?([^")]+)"?\)/) || [])[1];
  if (process.argv[6] !== 'ohne') await page.addStyleTag({ content: `@media (max-width: 1024px) { .elementor-element.elementor-element-${cid}::before { background-image: url("${url}"), url("${url}") !important; background-size: contain, contain !important; background-position: center top, center ${pos2} !important; background-repeat: no-repeat, no-repeat !important; } }` });
  await page.waitForTimeout(500);
  await page.evaluate(() => { const b = document.querySelector('#BorlabsCookieBox'); if (b) b.style.display = 'none'; });
  fs.mkdirSync('shots', { recursive: true });
  const name = `shots/logo_${slug.replace('/', '') || 'start'}_${cid}_${w}_${process.argv[6] === 'ohne' ? 'vorher' : 'vorschau'}.png`;
  await page.screenshot({ path: name, fullPage: true, clip: { x: 0, y: info.top - 60, width: w, height: info.h + 120 } });
  console.log(JSON.stringify({ ...info, img: url && url.split('/').pop(), shot: name }));
  await browser.close();
})().catch(e => { console.error('FAILED', e); process.exit(1); });
