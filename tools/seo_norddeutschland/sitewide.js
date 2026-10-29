// Seitenübergreifend: Website-Titel/Untertitel und Alt-Texte relevanter Bilder (REST)
const fs = require('fs'); const { open } = require('./api');
const ALTS = {
  1220: 'Elektronischer Türbeschlag und digitaler Schließzylinder von SimonsVoss',
  3364: 'Elektronischer Türbeschlag einer digitalen Schließanlage',
  3649: 'ProVision-Infra-Support: fester Ansprechpartner für deine elektronische Schließanlage',
  309: 'ProVision Infra GmbH Logo', 335: 'ProVision Infra GmbH Logo', 3317: 'ProVision Infra GmbH Logo', 3351: 'ProVision Infra GmbH Logo',
  3319: 'Google-Bewertung: 5 von 5 Sternen',
};
(async () => {
  const { browser, rest } = await open();
  const before = await rest('/wp/v2/settings');
  console.log('settings vorher:', before.status, JSON.stringify({ title: before.body.title, description: before.body.description }));
  if (before.status !== 200) throw new Error('settings nicht lesbar');
  const s = await rest('/wp/v2/settings', 'POST', { title: 'ProVision Infra', description: 'Digitale Schließanlagen, elektronische Schließsysteme und Videoüberwachung für Unternehmen in Norddeutschland' });
  console.log('settings nachher:', s.status, JSON.stringify({ title: s.body.title, description: s.body.description }));
  for (const [id, alt] of Object.entries(ALTS)) {
    const r = await rest(`/wp/v2/media/${id}`, 'POST', { alt_text: alt });
    console.log('alt', id, r.status, r.body.alt_text || JSON.stringify(r.body).slice(0, 100));
  }
  await browser.close();
})().catch(e => { console.error('FAILED', e); process.exit(1); });
