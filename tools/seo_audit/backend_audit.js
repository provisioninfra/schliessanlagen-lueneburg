// Nur-Lese-Audit des WordPress-Backends (gespeicherte Session, keine Zugangsdaten)
const { open } = require('/tmp/claude-0/-home-user-schliessanlagen-lueneburg/cd47d989-0a04-53d8-a4fc-151e73fb6ebc/scratchpad/wp/api');
const fs = require('fs'); const OUT = __dirname + '/admin/';
const PAGES = [
  ['plugins', '/wp-admin/plugins.php'],
  ['updates', '/wp-admin/update-core.php'],
  ['general', '/wp-admin/options-general.php'],
  ['reading', '/wp-admin/options-reading.php'],
  ['permalink', '/wp-admin/options-permalink.php'],
  ['yoast_settings', '/wp-admin/admin.php?page=wpseo_page_settings'],
  ['wprocket', '/wp-admin/options-general.php?page=wprocket'],
  ['elementor_settings', '/wp-admin/admin.php?page=elementor-settings'],
  ['themes', '/wp-admin/themes.php'],
  ['media_count', '/wp-admin/upload.php?mode=list'],
  ['pages_all', '/wp-admin/edit.php?post_type=page&post_status=all&posts_per_page=100'],
  ['posts_all', '/wp-admin/edit.php?post_type=post&post_status=all'],
  ['redirects', '/wp-admin/admin.php?page=wpseo_redirects'],
  ['site_health', '/wp-admin/site-health.php?tab=debug'],
];
(async () => {
  const { browser, call } = await open();
  for (const [name, path] of PAGES) {
    try {
      const r = await call('GET', path, { pause: 25000 });
      const t = await r.text();
      fs.writeFileSync(OUT + name + '.html', t);
      console.log(new Date().toISOString(), name, r.status(), 'len', t.length, 'title:', (t.match(/<title>([^<]*)/) || [])[1], /id="loginform"/.test(t) ? 'LOGIN-FORM!' : '');
    } catch (e) { console.log(name, 'ERROR', e.message.slice(0, 120)); }
  }
  await browser.close(); console.log('BACKEND_DONE');
})().catch(e => { console.error('FAILED', e); process.exit(1); });
