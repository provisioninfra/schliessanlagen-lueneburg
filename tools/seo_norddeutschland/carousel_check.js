// Funktionsprüfung des Kundenstimmen-Karussells. Export: check(url, {auth, tag}) -> {ok, report}
const { chromium } = require('playwright');
const NAMES = ['Andre Küster', 'Pia-Theresa', 'Mia Manikati', 'Vincent Oswald'];
async function check(url, { auth = false, tag = 'x' } = {}) {
  const browser = await chromium.launch();
  const report = []; let ok = true;
  const fail = m => { ok = false; report.push('FEHLER: ' + m); };
  for (const vp of [{ width: 1440, height: 900 }, { width: 390, height: 844 }]) {
    const ctx = await browser.newContext({ viewport: vp, ignoreHTTPSErrors: true, isMobile: vp.width < 500, ...(auth ? { storageState: __dirname + '/state.json' } : {}) });
    const page = await ctx.newPage();
    const bad = [];
    page.on('response', r => { const u = r.url(); if (/\.(css|js)(\?|$)/.test(u) && /provision-infra\.de/.test(u) && ![200, 304].includes(r.status())) bad.push(r.status() + ' ' + u.split('/').pop()); });
    page.on('requestfailed', q => { const u = q.url(); if (/\.(css|js)(\?|$)/.test(u) && /provision-infra\.de/.test(u)) bad.push('FAILED ' + u.split('/').pop()); });
    let st = 0;
    for (let i = 0; i < 8; i++) { bad.length = 0; const r = await page.goto(url, { waitUntil: 'load', timeout: 120000 }).catch(() => null); st = r ? r.status() : 0; if (st === 200 && !bad.length) break; report.push(`${vp.width}px: Ladeversuch ${i + 1} unvollständig (Status ${st}, ${bad.slice(0, 3).join(', ')})`); await page.waitForTimeout(6000); }
    if (bad.length) { fail(`${vp.width}px: Dateien wiederholt nicht geladen: ${bad.slice(0, 4).join(', ')}`); await ctx.close(); continue; }
    if (st !== 200) { fail(`${vp.width}px: Seite nicht ladbar (Status ${st})`); await ctx.close(); continue; }
    await page.addStyleTag({ content: '#BorlabsCookieBox, .brlbs-cmpnt-container, #BorlabsCookieDebugConsole, #wpadminbar, #pe-badge-fixed { display:none !important; } html{margin-top:0!important}' });
    const sec = page.locator('.elementor-element-7cfc047c').first();
    await sec.scrollIntoViewIfNeeded(); await page.waitForTimeout(2500);
    const info = await page.evaluate((NAMES) => {
      const sec = document.querySelector('.elementor-element-7cfc047c');
      const real = Array.from(sec.querySelectorAll('.swiper-slide')).filter(s => !s.classList.contains('swiper-slide-duplicate'));
      const nameOf = s => (s.querySelector('.elementor-image-box-title') || {}).textContent?.replace(/​/g, '').trim() || '';
      const css = (el, props, pseudo) => { if (!el) return null; const c = getComputedStyle(el, pseudo || null); return Object.fromEntries(props.map(p => [p, c.getPropertyValue(p)])); };
      const sig = s => s && ({
        quote: css(s.querySelector('.elementor-icon-box-description'), ['font-family', 'font-size', 'font-weight', 'line-height', 'color', 'text-align']),
        name: css(s.querySelector('.elementor-image-box-title'), ['font-family', 'font-size', 'font-weight', 'line-height', 'color']),
        role: css(s.querySelector('.elementor-image-box-description'), ['font-family', 'font-size', 'font-weight', 'line-height', 'color']),
        card: css(s.querySelector('.e-con') || s, ['background-color', 'border-radius', 'padding-top', 'padding-left', 'min-height']),
        icon: css(s.querySelector('.elementor-icon-box-icon svg, .elementor-icon-box-icon img'), ['width', 'height']),
        quoteMark: css(s.querySelector('.elementor-image-box-content'), ['background-image'], '::after'),
      });
      const byName = n => real.find(s => nameOf(s).startsWith(n));
      return { count: real.length, names: real.map(nameOf), bullets: sec.querySelectorAll('.swiper-pagination-bullet').length,
               sigMia: sig(byName('Mia Manikati')), sigVin: sig(byName('Vincent Oswald')), sigPia: sig(byName('Pia-Theresa')),
               vinText: (byName('Vincent Oswald')?.querySelector('.elementor-icon-box-description')?.textContent || '').trim(),
               vinRole: (byName('Vincent Oswald')?.querySelector('.elementor-image-box-description')?.textContent || '').replace(/​/g, '').trim() };
    }, NAMES);
    report.push(`${vp.width}px: ${info.count} Slides ${JSON.stringify(info.names)} | Punkte: ${info.bullets}`);
    if (info.count !== 4) fail(`${vp.width}px: erwartet 4 Slides, gefunden ${info.count}`);
    for (const n of NAMES) if (!info.names.some(x => x.startsWith(n))) fail(`${vp.width}px: ${n} fehlt`);
    if (info.bullets && info.bullets !== 4) fail(`${vp.width}px: ${info.bullets} Punkte statt 4`);
    if (!info.vinText.startsWith('"Super Service und sehr gutes Produkt!') || !info.vinText.endsWith('gerne wieder!"')) fail('Zitattext abweichend: ' + info.vinText.slice(0, 80));
    if (info.vinRole !== 'Inhaber / Geschäftsführer Studio Lüüd') fail('Funktion abweichend: ' + info.vinRole);
    const a = JSON.stringify(info.sigMia), b = JSON.stringify(info.sigVin);
    if (a !== b) fail(`${vp.width}px: Formatierung weicht ab\n  Mia: ${a}\n  Vin: ${b}`); else report.push(`${vp.width}px: Formatierung identisch mit bestehendem Slide (Schrift, Farben, Karte, Icon, Anführungszeichen)`);
    // Navigation: Weiter-Pfeil klicken, hervorgehobener Slide muss alle vier Namen durchlaufen
    const seen = new Set(); let vinHighlighted = null;
    const next = page.locator('.elementor-element-7cfc047c .elementor-swiper-button-next').first();
    for (let i = 0; i < 9; i++) {
      const cur = await page.evaluate((w) => {
        const sec = document.querySelector('.elementor-element-7cfc047c');
        const s = sec.querySelector(w > 767 ? '.swiper-slide-next' : '.swiper-slide-active');
        if (!s) return null;
        const t = (s.querySelector('.elementor-image-box-title') || {}).textContent?.replace(/​/g, '').trim();
        const c = getComputedStyle(s);
        return { name: t, border: c.borderTopColor + ' ' + c.borderTopWidth, opacity: c.opacity, transform: c.transform };
      }, vp.width);
      if (cur && cur.name) { seen.add(cur.name); if (cur.name.startsWith('Vincent') && !vinHighlighted) { vinHighlighted = cur; await page.waitForTimeout(600); await sec.screenshot({ path: `dump/carousel_${tag}_${vp.width}.png` }); } }
      if (await next.count()) await next.click({ force: true }).catch(() => {}); await page.waitForTimeout(900);
    }
    report.push(`${vp.width}px: per Pfeil durchlaufen: ${JSON.stringify([...seen])}`);
    if (!NAMES.every(n => [...seen].some(x => x.startsWith(n)))) fail(`${vp.width}px: Navigation erreicht nicht alle Slides`);
    if (!vinHighlighted) fail(`${vp.width}px: Vincent-Slide nie aktiv`);
    else { report.push(`${vp.width}px: Vincent aktiv: ${JSON.stringify(vinHighlighted)}`); if (vp.width > 767 && !/251, 201, 27/.test(vinHighlighted.border)) fail('Hervorhebung (gelber Rahmen) fehlt beim Vincent-Slide'); }
    await ctx.close();
  }
  await browser.close();
  return { ok, report };
}
module.exports = { check };
if (require.main === module) {
  check(process.argv[2], { auth: process.argv[3] === 'auth', tag: process.argv[4] || 'cli' }).then(r => { console.log(r.report.join('\n')); console.log(r.ok ? 'PRUEFUNG OK' : 'PRUEFUNG FEHLGESCHLAGEN'); process.exit(r.ok ? 0 : 3); });
}
