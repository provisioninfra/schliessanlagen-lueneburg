"""Gemeinsame Bausteine für die SEO-Optimierung Norddeutschland (Patches auf live geladene Elementor-Daten)."""
import copy, json, random, re

SITE = 'https://provision-infra.de'
ORG_ID = f'{SITE}/#organisation'
# Einsatzgebiet: Achse Hamburg – Lüneburger Heide – Hannover
CITIES = ['Hamburg', 'Lüneburg', 'Winsen (Luhe)', 'Buchholz in der Nordheide', 'Uelzen', 'Bad Bevensen',
          'Soltau', 'Celle', 'Hannover']
AREA_SERVED = [{'@type': 'City', 'name': c} for c in CITIES] + [
    {'@type': 'State', 'name': 'Niedersachsen'}, {'@type': 'Country', 'name': 'Deutschland'}]
CITY_TEXT = 'Hamburg, Lüneburg, Winsen, Buchholz, Uelzen, Soltau, Celle und Hannover'


def load(path):
    return json.load(open(path, encoding='utf-8'))


def save(d, path):
    json.dump(d, open(path, 'w', encoding='utf-8'), ensure_ascii=False)


def walk(e):
    yield e
    for c in e.get('elements', []):
        yield from walk(c)


def index(d):
    return {e['id']: e for r in d['elements'] for e in walk(r)}


def get(d, eid):
    ix = index(d)
    assert eid in ix, f'Element {eid} fehlt im Live-Stand'
    return ix[eid]


def new_id(d, taken=set()):
    ids = set(index(d)) | taken
    while True:
        i = '%07x' % random.randrange(16 ** 7)
        if i not in ids:
            taken.add(i)
            return i


def clone_new_ids(el, d):
    el = copy.deepcopy(el)
    for e in walk(el):
        e['id'] = new_id(d)
        e.pop('htmlCache', None)
    return el


def replace_exact(el, key, old, new):
    v = el['settings'].get(key, '')
    assert old in v, f"{el['id']}.{key}: erwarteter Text nicht gefunden: {old[:60]!r}"
    el['settings'][key] = v.replace(old, new, 1)


def set_exact(el, key, expected_old, new):
    """Nur ersetzen, wenn der Live-Wert noch dem geprüften Stand entspricht (Schutz vor parallelen Änderungen)."""
    v = el['settings'].get(key, '')
    assert v == expected_old, f"{el['id']}.{key} wurde zwischenzeitlich geändert, Abbruch: {v[:80]!r}"
    el['settings'][key] = new


def org_node():
    return {
        '@type': ['LocalBusiness', 'Locksmith'], '@id': ORG_ID, 'name': 'ProVision Infra GmbH', 'url': f'{SITE}/',
        'logo': f'{SITE}/wp-content/uploads/2026/10/kamera-logo-provision-infra-1032.png',
        'image': f'{SITE}/wp-content/uploads/2026/05/provision_header_02-1.png',
        'telephone': '+49 5821 4049040', 'email': 'info@provision-infra.de',
        'address': {'@type': 'PostalAddress', 'streetAddress': 'Klein Hesebecker Straße 11', 'postalCode': '29549',
                    'addressLocality': 'Bad Bevensen', 'addressRegion': 'Niedersachsen', 'addressCountry': 'DE'},
        'geo': {'@type': 'GeoCoordinates', 'latitude': 53.0779485, 'longitude': 10.5903962},
        'openingHoursSpecification': [
            {'@type': 'OpeningHoursSpecification', 'dayOfWeek': ['Monday', 'Tuesday', 'Wednesday', 'Thursday'], 'opens': '09:00', 'closes': '18:00'},
            {'@type': 'OpeningHoursSpecification', 'dayOfWeek': 'Friday', 'opens': '09:00', 'closes': '14:00'}],
        'areaServed': AREA_SERVED,
        'knowsAbout': ['Schließanlagen', 'elektronische Schließanlagen', 'digitale Schließsysteme', 'Zutrittskontrolle',
                       'Videoüberwachung', 'Kameraüberwachung'],
        'sameAs': ['https://www.instagram.com/provision_infra_gmbh/', 'https://www.facebook.com/share/1CWs2rohMt/',
                   'https://www.linkedin.com/company/provision-infra-gmbh-i-g/'],
    }


def schema_html(graph):
    return '<script type="application/ld+json">' + json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False) + '</script>'


def schema_container(d, graph, title='Strukturierte Daten (SEO)'):
    """Unsichtbarer Container ohne Abstände mit einem HTML-Widget für JSON-LD."""
    zero = {'unit': 'px', 'top': '0', 'right': '0', 'bottom': '0', 'left': '0', 'isLinked': False}
    return {'id': new_id(d), 'elType': 'container', 'isInner': False,
            'settings': {'content_width': 'full', 'padding': zero, 'margin': copy.deepcopy(zero),
                         'min_height': {'unit': 'px', 'size': 0, 'sizes': []},
                         'flex_gap': {'column': '0', 'row': '0', 'isLinked': True, 'unit': 'px', 'size': 0},
                         '_title': title},
            'elements': [{'id': new_id(d), 'elType': 'widget', 'widgetType': 'html', 'isInner': False,
                          'settings': {'html': schema_html(graph), '_title': title}, 'elements': []}]}


def faq_item(template, d, q, a):
    it = copy.deepcopy(template)
    it['_id'] = new_id(d)
    it['eael_adv_accordion_tab_title'] = q
    it['eael_adv_accordion_tab_content'] = a
    return it


def remove_existing_schema_container(d, title='Strukturierte Daten (SEO)'):
    """Idempotenz: eigenen Schema-Container entfernen, falls ein früherer Lauf ihn schon angelegt hat."""
    d['elements'] = [e for e in d['elements'] if e.get('settings', {}).get('_title') != title or e.get('elType') != 'container']
