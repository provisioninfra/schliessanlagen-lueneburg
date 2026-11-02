// Stadtseiten anlegen: REST (Entwurf) -> Elementor save_builder (publish) -> Yoast. Idempotent über wpstate.json.
const fs = require('fs'); const { open } = require('/tmp/claude-0/-home-user-schliessanlagen-lueneburg/cd47d989-0a04-53d8-a4fc-151e73fb6ebc/scratchpad/wp/api');
const BUILD = __dirname + '/build'; const statePath = '/tmp/claude-0/-home-user-schliessanlagen-lueneburg/cd47d989-0a04-53d8-a4fc-151e73fb6ebc/scratchpad/wp/wpstate.json';
const state = JSON.parse(fs.readFileSync(statePath)); state.staedte = state.staedte || {}; state.staedteDone = state.staedteDone || {};
const save = () => fs.writeFileSync(statePath, JSON.stringify(state, null, 1));
const argKeys = process.argv.slice(2);
const keys = argKeys.length ? argKeys : fs.readdirSync(BUILD).filter(f => f.endsWith('.elementor.json')).map(f => f.replace('.elementor.json', ''));
(async () => {
  const { browser, rest, ajax, html } = await open();
  const h = await html('/wp-admin/post.php?post=4496&action=elementor');
  if (h.length < 1000 || /id="loginform"/.test(h)) throw new Error('nicht eingeloggt (len ' + h.length + ')');
  const eNonce = (h.match(/"ajax":\{"url":"[^"]*","nonce":"([a-f0-9]+)"/) || [])[1];
  const yNonce = (h.match(/name="_wpseo_elementor_nonce"\s+value="([a-f0-9]+)"/) || h.match(/id="_wpseo_elementor_nonce"[^>]*value="([a-f0-9]+)"/) || [])[1];
  const yAction = (h.match(/id="yoast-form"[\s\S]*?name="action"\s+value="([a-z_]+)"/) || [])[1] || 'wpseo_elementor_save';
  console.log(new Date().toISOString(), 'nonces', !!eNonce, !!yNonce, yAction);
  if (!eNonce || !yNonce) throw new Error('Nonce fehlt');
  for (const key of keys) {
    if (state.staedteDone[key] && !argKeys.length && !process.env.SAVE_ONLY) { console.log('skip (fertig)', key, state.staedte[key]); continue; }
    const data = JSON.parse(fs.readFileSync(`${BUILD}/${key}.elementor.json`, 'utf8'));
    let id = state.staedte[key];
    if (!id && process.env.CHECK_EXISTING) {
      const ex = await rest(`/wp/v2/pages?slug=${key}&status=any&_fields=id,slug,status`);
      if (ex.status === 200 && Array.isArray(ex.body) && ex.body.length) { id = ex.body[0].id; console.log('vorhanden', key, ex.body[0]); }
    }
    if (!id) {
      const r = await rest('/wp/v2/pages', 'POST', { title: data.seo.post_title, slug: key, status: 'draft', comment_status: 'closed' });
      if (r.status !== 201) throw new Error('create failed ' + key + ' ' + r.status + ' ' + JSON.stringify(r.body).slice(0, 200));
      id = r.body.id; console.log(new Date().toISOString(), 'angelegt', key, id, r.body.slug);
    }
    state.staedte[key] = id; save();
    if (process.env.SAVE_ONLY) {
      if (!id) throw new Error('SAVE_ONLY ohne ID: ' + key);
      const actions0 = JSON.stringify({ save_builder: { action: 'save_builder', data: { status: 'publish', elements: data.elements, settings: data.settings } } });
      const s0 = await ajax({ action: 'elementor_ajax', _nonce: eNonce, editor_post_id: String(id), initial_document_id: String(id), actions: actions0 });
      const r0 = s0.body?.data?.responses?.save_builder;
      console.log(new Date().toISOString(), 'resave', key, id, s0.status, r0?.success, r0?.data?.status);
      if (!s0.body?.success || !r0?.success) throw new Error('resave failed ' + key + ' ' + JSON.stringify(s0.body).slice(0, 300));
      state.staedteResaved = state.staedteResaved || {}; state.staedteResaved[key] = new Date().toISOString(); save(); continue;
    }
    // Editor der neuen Seite einmal laden: markiert den Beitrag als Elementor-Dokument (wie bei der Lüneburg-Anlage im Oktober)
    const eh = await html(`/wp-admin/post.php?post=${id}&action=elementor`);
    const eNonce2 = (eh.match(/"ajax":\{"url":"[^"]*","nonce":"([a-f0-9]+)"/) || [])[1] || eNonce;
    console.log(new Date().toISOString(), 'editor geladen', key, id, 'len', eh.length, 'nonce', !!eNonce2, /id="loginform"/.test(eh) ? 'LOGIN!' : '');
    const actions = JSON.stringify({ save_builder: { action: 'save_builder', data: { status: 'publish', elements: data.elements, settings: data.settings } } });
    const s = await ajax({ action: 'elementor_ajax', _nonce: eNonce2, editor_post_id: String(id), initial_document_id: String(id), actions });
    const res = s.body?.data?.responses?.save_builder;
    console.log(new Date().toISOString(), 'elementor', key, id, s.status, res?.success, res?.data?.status);
    if (!s.body?.success || !res?.success) throw new Error('save failed ' + key + ' ' + JSON.stringify(s.body).slice(0, 300));
    const form = { action: yAction, post_id: String(id), _wpseo_elementor_nonce: yNonce,
      yoast_wpseo_focuskw: data.seo.focuskw, yoast_wpseo_title: data.seo.title, yoast_wpseo_metadesc: data.seo.description,
      'yoast_wpseo_meta-robots-noindex': '0', 'yoast_wpseo_meta-robots-nofollow': '0',
      'yoast_wpseo_opengraph-title': data.seo.title, 'yoast_wpseo_opengraph-description': data.seo.description,
      'yoast_wpseo_twitter-title': data.seo.title, 'yoast_wpseo_twitter-description': data.seo.description, yoast_wpseo_slug: key };
    const y = await ajax(form);
    console.log(new Date().toISOString(), 'yoast', key, y.status, JSON.stringify(y.body).slice(0, 100));
    state.staedteDone[key] = new Date().toISOString(); save();
  }
  const ids = Object.values(state.staedte).join(',');
  const chk = await rest(`/wp/v2/pages?include=${ids}&status=any&per_page=50&_fields=id,slug,status,link,title`);
  for (const p of (chk.body || [])) console.log('CHECK', p.id, p.slug, p.status, p.link, '|', p.title?.rendered);
  console.log('CITIES_DONE'); await browser.close();
})().catch(e => { console.error('FAILED', e); process.exit(1); });
