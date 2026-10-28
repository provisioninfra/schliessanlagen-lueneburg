// Startseite (Post 31): Yoast-SEO-Titel aendern, alle anderen Yoast-Felder unveraendert mitsenden
const fs = require('fs'); const { open } = require('./api');
const NEW_TITLE = 'Schließanlagen & digitale Zutrittssysteme | ProVision Infra';
(async () => {
  const { browser, ajax, html, parseForm } = await open();
  const h = await html('/wp-admin/post.php?post=31&action=elementor');
  if (h.length < 1000 || /id="loginform"/.test(h)) throw new Error('Nicht eingeloggt oder leere Antwort (len ' + h.length + ')');
  const form = await parseForm(h, '#yoast-form');
  const keys = Object.keys(form).filter(k => k.startsWith('yoast_wpseo_'));
  console.log('Yoast-Felder gelesen:', keys.length, '| alter Titel:', JSON.stringify(form.yoast_wpseo_title), '| metadesc:', (form.yoast_wpseo_metadesc || '').slice(0, 60), '| focuskw:', form.yoast_wpseo_focuskw);
  if (!keys.length || !form._wpseo_elementor_nonce) { fs.writeFileSync('dump/editor_31.html', h); throw new Error('Yoast-Formular nicht gefunden'); }
  fs.writeFileSync('dump/yoast_31_before.json', JSON.stringify(form, null, 1));
  const payload = { action: form.action || 'wpseo_elementor_save', post_id: form.post_id || '31', _wpseo_elementor_nonce: form._wpseo_elementor_nonce };
  for (const k of keys) payload[k] = form[k];
  payload.yoast_wpseo_title = NEW_TITLE;
  const r = await ajax(payload);
  console.log('yoast save (Startseite):', r.status, JSON.stringify(r.body).slice(0, 160));
  await browser.close();
})().catch(e => { console.error('FAILED', e); process.exit(1); });
