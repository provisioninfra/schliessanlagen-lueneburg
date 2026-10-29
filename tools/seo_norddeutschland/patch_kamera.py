#!/usr/bin/env python3
"""Kamerasysteme (4313): Regionstext mit Querverlinkung, Einsatzgebiet im Schema. Aufruf: python3 -I patch_kamera.py live.json out.json"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seo_common import *

DESC = 'Kamera- & Videoüberwachung für Unternehmen zwischen Hamburg und Hannover: DSGVO-konform geplant, mit Alarm aufs Handy. ProVision Infra installiert vor Ort.'
d = load(sys.argv[1])

set_exact(get(d, '5c65e03'), 'editor',
          '<p>Wir sitzen in Bad Bevensen bei Lüneburg und sind vor allem im Raum Hamburg, Hannover und Niedersachsen unterwegs. Darüber hinaus sind wir bundesweit im Einsatz.</p><p>Für Beratung, Planung und Umsetzung kommen wir direkt zu dir vor Ort, schauen uns deine Situation an und setzen das System dort um, wo es gebraucht wird.</p>',
          f'<p>Wir sitzen in Bad Bevensen bei Lüneburg und sind vor allem zwischen Hamburg und Hannover unterwegs: in {CITY_TEXT} sowie in ganz Niedersachsen. Darüber hinaus sind wir bundesweit im Einsatz.</p>'
          '<p>Für Beratung, Planung und Umsetzung kommen wir direkt zu dir vor Ort, schauen uns deine Situation an und setzen das System dort um, wo es gebraucht wird. Kameras und Zutritt lassen sich kombinieren: Mehr zu <a href="/">digitalen Schließanlagen</a> und unserem <a href="/zutrittssystem/">Service für elektronische Schließanlagen</a>.</p>')

w = get(d, 'dca37dc')
m = re.fullmatch(r'\s*<script type="application/ld\+json">(.*)</script>\s*', w['settings']['html'], re.S)
assert m, 'Schema-Widget hat unerwartetes Format'
data = json.loads(m.group(1))
n = 0
for node in data['@graph']:
    if 'areaServed' in node:
        node['areaServed'] = AREA_SERVED; n += 1
    if node.get('@type') == 'Service':
        node['description'] = DESC
assert n == 2, f'erwartet 2 Knoten mit areaServed, gefunden {n}'
w['settings']['html'] = '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + '</script>'
save(d, sys.argv[2])
print('Kamerasysteme gepatcht: Regionstext + Links, areaServed (2 Knoten), Service-Beschreibung')
