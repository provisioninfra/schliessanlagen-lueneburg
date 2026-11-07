// Zweite Glas-Logo-Instanz (nur Smartphone ≤ 767 px) als Custom-CSS auf dem Overlay-Container; ein Config-Abruf für alle Seiten, dann je Seite ein save_builder
const fs = require('fs'); const { open } = require('/tmp/claude-0/-home-user-schliessanlagen-lueneburg/cd47d989-0a04-53d8-a4fc-151e73fb6ebc/scratchpad/wp/api');
const state = JSON.parse(fs.readFileSync('/tmp/claude-0/-home-user-schliessanlagen-lueneburg/cd47d989-0a04-53d8-a4fc-151e73fb6ebc/scratchpad/wp/wpstate.json'));
const TARGETS = { 31: ['f86d566', '75%'], 4313: ['74b6d54', '72%'], 4496: ['4a79ecb', '72%'], 4605: ['4a79ecb', '72%'] };
for (const id of Object.values(state.staedte)) TARGETS[id] = ['4a79ecb', '72%'];
const MARK = '/* pv-glaslogo-2 */';
const only = process.argv.slice(2).map(Number);
const ids = Object.keys(TARGETS).map(Number).filter(i => !only.length || only.includes(i));
const walk = function* (e) { yield e; for (const c of e.elements || []) yield* walk(c); };
(async () => {
  const { browser, ajax, html } = await open();
  const h = await html('/wp-admin/post.php?post=31&action=elementor');
  if (h.length < 1000 || /id="loginform"/.test(h)) throw new Error('nicht eingeloggt');
  const eNonce = (h.match(/"ajax":\{"url":"[^"]*","nonce":"([a-f0-9]+)"/) || [])[1]; if (!eNonce) throw new Error('kein Nonce');
  const actions = {}; for (const id of ids) actions['c' + id] = { action: 'get_document_config', data: { id } };
  const r = await ajax({ action: 'elementor_ajax', _nonce: eNonce, actions: JSON.stringify(actions) });
  const log = [];
  for (const id of ids) {
    const res = r.body?.data?.responses?.['c' + id]; const d = res?.data;
    if (!res?.success || !d) { console.log(id, 'CONFIG FEHLER', JSON.stringify(res).slice(0, 150)); continue; }
    const [cid, pos2] = TARGETS[id]; const elements = d.elements; const settings = d.settings.settings;
    let el = null; for (const root of elements) for (const e of walk(root)) { e.htmlCache && delete e.htmlCache; if (e.id === cid) el = e; }
    if (!el) { console.log(id, 'ELEMENT FEHLT', cid); continue; }
    const img = el.settings?.background_overlay_image?.url;
    if (!img || !/Frame-2147224855/.test(img)) { console.log(id, 'KEIN GLAS-LOGO-OVERLAY', cid, img); continue; }
    const cur = el.settings.custom_css || '';
    if (cur.includes(MARK)) { console.log(id, 'bereits gesetzt', cid); continue; }
    const css = `${MARK}\n@media (max-width: 767px) {\n  selector::before {\n    background-image: url("${img}"), url("${img}");\n    background-size: contain, contain;\n    background-position: center top, center ${pos2};\n    background-repeat: no-repeat, no-repeat;\n  }\n}`;
    el.settings.custom_css = cur ? cur.trimEnd() + '\n\n' + css : css;
    if (process.env.DRY) { console.log(id, 'DRY', cid, 'pos2', pos2, 'img', img.split('/').pop(), 'css-len', el.settings.custom_css.length); continue; }
    const s = await ajax({ action: 'elementor_ajax', _nonce: eNonce, editor_post_id: String(id), initial_document_id: String(id),
      actions: JSON.stringify({ save_builder: { action: 'save_builder', data: { status: settings.post_status || 'publish', elements, settings } } }) });
    const sr = s.body?.data?.responses?.save_builder;
    console.log(new Date().toISOString(), id, cid, 'save', s.status, sr?.success, sr?.data?.status, settings.post_title);
    if (!sr?.success) throw new Error('save fehlgeschlagen ' + id + ' ' + JSON.stringify(s.body).slice(0, 200));
    log.push(id);
  }
  console.log('LOGO_DONE', log.join(','));
  await browser.close();
})().catch(e => { console.error('FAILED', e); process.exit(1); });
