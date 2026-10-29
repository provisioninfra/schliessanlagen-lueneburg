// Kundenstimme Vincent Oswald: je Seite Vorschau (Autosave) speichern -> Funktion prüfen -> nur bei Erfolg veröffentlichen
const fs = require('fs'); const { execFileSync } = require('child_process'); const { open } = require('./api'); const { check } = require('./carousel_check');
const PATCH = '/home/user/schliessanlagen-lueneburg/tools/seo_norddeutschland/patch_testimonial.py';
const PAGES = [[31, 'https://provision-infra.de/'], [4313, 'https://provision-infra.de/kamerasysteme/'], [4496, 'https://provision-infra.de/lueneburg/'], [4605, 'https://provision-infra.de/uelzen/']];
(async () => {
  const { browser, ajax, html } = await open();
  const results = {};
  for (const [id, url] of PAGES) {
    console.log(`=== Seite ${id} ${url}`);
    try {
      const h = await html(`/wp-admin/post.php?post=${id}&action=elementor`);
      if (h.length < 1000 || /id="loginform"/.test(h)) throw new Error('nicht eingeloggt');
      const eNonce = (h.match(/"ajax":\{"url":"[^"]*","nonce":"([a-f0-9]+)"/) || [])[1];
      let preview = ((h.match(/"wp_preview":"([^"]+)"/) || [])[1] || '').replace(/\\\//g, '/');
      const r = await ajax({ action: 'elementor_ajax', _nonce: eNonce, actions: JSON.stringify({ c: { action: 'get_document_config', data: { id } } }) });
      const d = r.body?.data?.responses?.c?.data; if (!d) throw new Error('get_document_config fehlgeschlagen');
      fs.writeFileSync(`dump/tlive_${id}.json`, JSON.stringify({ elements: d.elements, settings: d.settings.settings }));
      const out = execFileSync('python3', ['-I', PATCH, `dump/tlive_${id}.json`, `dump/tpatched_${id}.json`], { encoding: 'utf8' }).trim();
      console.log('  patch:', out);
      if (/bereits vorhanden/.test(out)) { results[id] = 'bereits vorhanden'; continue; }
      const p = JSON.parse(fs.readFileSync(`dump/tpatched_${id}.json`, 'utf8'));
      const save = async (status) => {
        const s = await ajax({ action: 'elementor_ajax', _nonce: eNonce, editor_post_id: String(id), initial_document_id: String(id),
          actions: JSON.stringify({ save_builder: { action: 'save_builder', data: { status, elements: p.elements, settings: p.settings } } }) });
        const res = s.body?.data?.responses?.save_builder;
        if (!res?.success) throw new Error(`save ${status} fehlgeschlagen: ` + JSON.stringify(s.body).slice(0, 200));
        return res;
      };
      const auto = await save('autosave');
      preview = ((auto.data?.config?.document?.urls?.wp_preview) || preview);
      console.log('  Vorschau gespeichert:', preview.replace(/preview_nonce=[a-f0-9]+/, 'preview_nonce=…'));
      const c = await check(preview, { auth: true, tag: `preview_${id}` });
      c.report.forEach(l => console.log('  ' + l.split('\n').join('\n  ')));
      if (!c.ok) { results[id] = 'Vorschau-Prüfung fehlgeschlagen, NICHT veröffentlicht'; console.log('  -> NICHT veröffentlicht'); continue; }
      const pub = await save('publish');
      console.log('  veröffentlicht:', pub.data?.status);
      results[id] = 'veröffentlicht';
    } catch (e) { results[id] = 'Fehler: ' + e.message; console.log('  FEHLER', e.message); }
  }
  console.log('ERGEBNIS', JSON.stringify(results));
  await browser.close();
})().catch(e => { console.error('FAILED', e); process.exit(1); });
