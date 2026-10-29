// Gezielte Änderung einer Seite auf Basis des AKTUELLEN Stands:
//   node pagepatch.js <postId> <patch.py|-> [yoast-overrides.json|-] [--status publish]
// 1) Editor-HTML laden (Elementor- + Yoast-Nonce, aktuelle Yoast-Felder)
// 2) get_document_config -> dump/live_<id>.json
// 3) python3 -I <patch.py> dump/live_<id>.json dump/patched_<id>.json  (nur wenn patch != '-')
// 4) save_builder mit patched elements + unveränderten settings
// 5) Yoast-Felder: aktuelle Werte + Overrides speichern (nur wenn overrides != '-')
const fs = require('fs'); const { execFileSync } = require('child_process'); const { open } = require('./api');
const [id, patch, yoastFile] = process.argv.slice(2);
if (!id) { console.error('usage'); process.exit(2); }
(async () => {
  const { browser, ajax, html, parseForm } = await open();
  const h = await html(`/wp-admin/post.php?post=${id}&action=elementor`);
  if (h.length < 1000 || /id="loginform"/.test(h)) throw new Error('nicht eingeloggt (len ' + h.length + ')');
  const eNonce = (h.match(/"ajax":\{"url":"[^"]*","nonce":"([a-f0-9]+)"/) || [])[1];
  if (!eNonce) throw new Error('kein Elementor-Nonce');
  if (patch && patch !== '-') {
    const r = await ajax({ action: 'elementor_ajax', _nonce: eNonce, actions: JSON.stringify({ c: { action: 'get_document_config', data: { id: Number(id) } } }) });
    const d = r.body?.data?.responses?.c?.data;
    if (!d || !Array.isArray(d.elements)) throw new Error('get_document_config fehlgeschlagen: ' + JSON.stringify(r.body).slice(0, 200));
    fs.writeFileSync(`dump/live_${id}.json`, JSON.stringify({ elements: d.elements, settings: d.settings.settings }, null, 1));
    console.log('live geladen', id, '| top-level', d.elements.length, '| status', d.settings.settings.post_status);
    const out = execFileSync('python3', ['-I', patch, `dump/live_${id}.json`, `dump/patched_${id}.json`], { encoding: 'utf8' });
    process.stdout.write(out.split('\n').map(l => l ? '  patch: ' + l : l).join('\n'));
    const p = JSON.parse(fs.readFileSync(`dump/patched_${id}.json`, 'utf8'));
    const status = p.settings.post_status || 'publish';
    const s = await ajax({ action: 'elementor_ajax', _nonce: eNonce, editor_post_id: String(id), initial_document_id: String(id),
      actions: JSON.stringify({ save_builder: { action: 'save_builder', data: { status, elements: p.elements, settings: p.settings } } }) });
    const res = s.body?.data?.responses?.save_builder;
    console.log('elementor save', id, s.status, res?.success, res?.data?.status);
    if (!res?.success) throw new Error('save fehlgeschlagen ' + JSON.stringify(s.body).slice(0, 300));
  }
  if (yoastFile && yoastFile !== '-') {
    const over = JSON.parse(fs.readFileSync(yoastFile, 'utf8'));
    const form = await parseForm(h, '#yoast-form');
    const keys = Object.keys(form).filter(k => k.startsWith('yoast_wpseo_'));
    if (!keys.length || !form._wpseo_elementor_nonce) throw new Error('Yoast-Formular nicht gefunden');
    fs.writeFileSync(`dump/yoast_${id}_before.json`, JSON.stringify(form, null, 1));
    const payload = { action: form.action || 'wpseo_elementor_save', post_id: form.post_id || String(id), _wpseo_elementor_nonce: form._wpseo_elementor_nonce };
    for (const k of keys) payload[k] = form[k];
    for (const [k, v] of Object.entries(over)) payload[k] = v;
    const y = await ajax(payload);
    console.log('yoast save', id, y.status, JSON.stringify(y.body).slice(0, 120), '| geändert:', Object.keys(over).join(', '));
  }
  await browser.close();
})().catch(e => { console.error('FAILED', e); process.exit(1); });
