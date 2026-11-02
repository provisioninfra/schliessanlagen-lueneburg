#!/usr/bin/env python3
"""Stadtseiten aus der Live-Vorlage Lüneburg bauen.
   python3 -I build_city.py <cfg_4496.json> <out-dir> [key ...]
Element-IDs bleiben erhalten (Elementor-CSS ist je Beitrag gescoped; Uelzen teilt bereits 344 IDs mit Lüneburg)."""
import json, copy, random, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cities import CITIES, GENERIC, MOBILE_TWIN, TIMELINE_TWIN, FAQ_GENERIC, ALL_CITY_LINKS
SITE = 'https://provision-infra.de'
tpl = json.load(open(sys.argv[1], encoding='utf-8'))
OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
only = set(sys.argv[3:])

def walk(e):
    yield e
    for c in e.get('elements', []): yield from walk(c)
tpl_ix = {e['id']: e for r in tpl['elements'] for e in walk(r)}
assert tpl['settings'].get('post_title') == 'Schließanlagen & Videoüberwachung Lüneburg', tpl['settings'].get('post_title')

def build(city, idx):
    d = copy.deepcopy({'elements': tpl['elements'], 'settings': tpl['settings']})
    ix = {e['id']: e for r in d['elements'] for e in walk(r)}
    for e in ix.values(): e.pop('htmlCache', None)  # Editor-Vorschau-HTML der Vorlage nicht mitschicken
    name, kurz, V = city['name'], city['kurz'], idx % 3
    fmt = lambda s: s.format(name=kurz, kreis_in=city['kreis_in'], zeit=city['zeit'])
    changed = set()
    def field(eid): return 'title' if ix[eid].get('widgetType') == 'heading' else 'editor'
    def setf(eid, key, val, expect=None):
        el = ix[eid]; old = el['settings'].get(key, '')
        if expect is not None: assert expect in old, (eid, key, expect, old[:80])
        el['settings'][key] = val; changed.add((eid, key))
    def rep(eid, key, old, new):
        v = ix[eid]['settings'].get(key, ''); assert old in v, (eid, key, old, v[:100])
        ix[eid]['settings'][key] = v.replace(old, new); changed.add((eid, key))
    d['settings']['post_title'] = f'Schließanlagen & Videoüberwachung {name}'
    d['settings']['post_status'] = 'publish'
    rep('9dcea29', 'title', 'in Lüneburg', f'in {name}')
    setf('e429076', 'title', city['hero'], 'Lüneburger Betriebe')
    setf('34dc7fa', '_title', f'Region {kurz} + Film', 'Lüneburg')
    setf('d05eab3', 'title', city['region_h'], 'Lüneburg'); setf('d05eab3', '_title', city['region_h'])
    setf('7df04ae', 'editor', f"<p>{city['region_p1']}</p>", 'Lüneburg')
    setf('d38dec5', 'editor', f"<p>{city['region_p2']}</p>", 'Lüneburger Altstadt')
    setf('d7f768f', '_title', f'Schließanlagen {kurz}', 'Lüneburg')
    setf('74b6d54', 'title', f'Schließanlagen &amp; Zutrittskontrolle in {name}: <span style="font-weight: 700; ">{city["schliess_span"]}</span>', 'Lüneburg')
    setf('74b6d54', '_title', f'Schließanlagen {kurz}')
    setf('43e5085', 'editor', f"<p>{city['schliess_intro']}</p>", 'Lüneburg')
    setf('3ac3e9e', 'editor', f"<p>{city['begehung']}</p>", 'Lüneburg')
    setf('d70fb3d', '_title', f'Videoüberwachung {kurz}', 'Lüneburg')
    setf('c869af6', 'title', city['kamera_h2'], 'Lüneburg'); setf('c869af6', '_title', city['kamera_h2'])
    setf('8b353e8', 'title', city['kamera_sub'], 'Lüneburg')
    setf('aed8a2d', '_title', f'Leistungen {kurz}', 'Lüneburg')
    rep('8e89b3c', 'title', 'in Lüneburg', f'in {name}')
    setf('187d473', 'editor', f"<p>{city['wartung']}</p>", 'Lüneburg'); setf('88a3173', 'editor', f"<p>{city['wartung']}</p>", 'Lüneburg')
    setf('f1a5d3e', '_title', f'Zielgruppen {kurz}', 'Lüneburg')
    setf('cfa4bb1', 'title', f'Für wen wir in {name} arbeiten', 'Lüneburg'); setf('cfa4bb1', '_title', f'Für wen wir in {name} arbeiten')
    setf('8754a23', 'editor', f"<p>{city['zielgruppen_p']}</p>", 'Lüneburg')
    setf('51f3331', 'title', f'ProVision Infra <br><span style="font-weight: 700; ">{city["standort_span"]}</span>', 'Lüneburg')
    old = ix['5c65e03']['settings']['editor']
    m = re.search(r'<p><strong>ProVision Infra GmbH</strong>[\s\S]*$', old); assert m and 'Adendorf' in old
    links = ', '.join(f'<a href="{u}">{n}</a>' for u, n in ALL_CITY_LINKS if u != f"/{city['key']}/")
    p3 = f'<p>Weitere Einsatzgebiete zwischen Hamburg und Hannover: {links}. Mehr zu <a href="/">digitalen Schließanlagen</a> findest du auf unserer Startseite.</p>'
    setf('5c65e03', 'editor', f"<p>{city['standort_p1']}</p>" + fmt(GENERIC['standort_p2'][V]) + p3 + m.group(0))
    rep('7983242', 'title', '<b>Lüneburg</b>', f'<b>{name}</b>'); rep('45eaf1f', 'title', '<b>Lüneburg</b>', f'<b>{name}</b>')
    for eid, variants in GENERIC.items():
        if eid == 'standort_p2': continue
        val = fmt(variants[V]); setf(eid, field(eid), val)
        if eid in MOBILE_TWIN: setf(MOBILE_TWIN[eid], field(MOBILE_TWIN[eid]), val)
    # mobile Timeline: Auszüge entsprechen den Desktop-Texten der Vorlage
    tl = ix['756a14f']['settings']['eael_coustom_content_posts']; hit = 0
    for it in tl:
        for eid in TIMELINE_TWIN:
            if it.get('eael_custom_excerpt') == tpl_ix[eid]['settings']['editor']:
                it['eael_custom_excerpt'] = ix[eid]['settings']['editor']; hit += 1
    assert hit == 5, hit
    # FAQ (10 Einträge)
    proto = ix['ed852c3']['settings']['eael_adv_accordion_tab'][0]
    def item(q, a):
        it = copy.deepcopy(proto); it['_id'] = '%07x' % random.randrange(16 ** 7)
        it['eael_adv_accordion_tab_title'] = q; it['eael_adv_accordion_tab_content'] = a; return it
    g = lambda k: (fmt(FAQ_GENERIC[k][V][0]), fmt(FAQ_GENERIC[k][V][1]))
    faq = [(f'Was kostet eine Schließanlage in {name}?', city['faq_kosten']), g('mech'), g('umruesten'), city['faq_anfahrt'],
           city['faq_kamera'], g('verbinden'), g('hersteller'), g('danach'), g('dauer'), city['faq_extra']]
    ix['ed852c3']['settings']['eael_adv_accordion_tab'] = [item(q, a) for q, a in faq]
    # Schema
    h = ix['f058554']['settings']['html']; mm = re.search(r'<script type="application/ld\+json">([\s\S]*?)</script>', h)
    j = json.loads(mm.group(1)); org, s1, s2 = j['@graph']; assert s1['@type'] == 'Service' and s2['@type'] == 'Service'
    area = [{'@type': t, 'name': n} for t, n in city['area']]; base = f"{SITE}/{city['key']}/"
    org['areaServed'] = area
    s1.update({'@id': base + '#schliessanlagen', 'url': base + '#schliessanlagen', 'name': f'Mechanische und elektronische Schließanlagen in {name}',
               'description': f"Planung, Montage und Betreuung mechanischer und elektronischer Schließanlagen (EVVA, SimonsVoss, Keyota, Keyrent, NUKI) für Unternehmen in {name} und {city['kreis_in']}.", 'areaServed': area[:2]})
    s2.update({'@id': base + '#kamera', 'url': base + '#kamera', 'name': f'Video- und Kameraüberwachung in {name}',
               'description': f'Planung und Installation von Kamerasystemen (TP-Link VIGI) mit App-Zugriff und lokaler Aufzeichnung für Betriebe in {name} und Umgebung.', 'areaServed': area[:2]})
    ix['f058554']['settings']['html'] = '<script type="application/ld+json">' + json.dumps(j, ensure_ascii=False) + '</script>'
    # Restekontrolle
    s = json.dumps(d, ensure_ascii=False); prof = json.dumps(city, ensure_ascii=False) + ' '.join(n for _, n in ALL_CITY_LINKS)
    tokens = ['Lüneburger Betriebe', 'Lüneburger Altstadt', 'Adendorf', 'Bardowick', 'Reppenstedt', 'Scharnebeck', 'Region Lüneburg', 'in Lüneburg', 'für Lüneburg', 'nach Lüneburg', 'Raum Lüneburg', 'Landkreis Lüneburg', 'Lüneburg', 'Lüneburger']
    rest = {t: (s.count(t), prof.count(t)) for t in tokens if s.count(t) > prof.count(t) + (1 if t == 'Lüneburg' else 0)}
    where = [(e['id'], e.get('widgetType') or e['elType'], k, str(v).count('Lüneburg')) for e in ix.values() for k, v in e['settings'].items() if 'Lüneburg' in json.dumps(v, ensure_ascii=False) and not (k == 'editor' and e['id'] == '5c65e03')]
    if rest: print('   Fundstellen:', where)
    seo = {'post_title': d['settings']['post_title'], 'title': city['title'], 'description': city['desc'], 'focuskw': f'Schließanlagen {kurz}', 'slug': city['key']}
    assert len(seo['title']) <= 60 and len(seo['description']) <= 160, (len(seo['title']), len(seo['description']))
    out = {'key': city['key'], 'variant': V, 'elements': d['elements'], 'settings': d['settings'], 'seo': seo}
    json.dump(out, open(f"{OUT}/{city['key']}.elementor.json", 'w', encoding='utf-8'), ensure_ascii=False)
    words = len(re.findall(r'[A-Za-zÄÖÜäöüß][A-Za-zÄÖÜäöüß\-]+', re.sub('<[^>]+>', ' ', ' '.join(str(e['settings'].get(k, '')) for e in ix.values() for k in ('title', 'editor')))))
    print(f"{city['key']:15} V={V} Felder={len(changed)} FAQ={len(faq)} Wörter≈{words} Reste={rest or 'keine'} title={len(seo['title'])} desc={len(seo['description'])}")

for i, c in enumerate(CITIES):
    if only and c['key'] not in only: continue
    build(c, i)
