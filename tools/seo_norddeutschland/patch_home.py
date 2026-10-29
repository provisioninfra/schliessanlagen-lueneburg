#!/usr/bin/env python3
"""Startseite (31): Region, Keywords, FAQ, Schema. Aufruf: python3 -I patch_home.py live.json out.json"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seo_common import *

d = load(sys.argv[1])

# 1 Hero: Region im Einleitungstext
replace_exact(get(d, 'e429076'), 'title',
              'ProVision Infra plant &amp; installiert dein digitales Zutrittssystem,',
              'ProVision Infra plant &amp; installiert in Norddeutschland dein digitales Zutrittssystem,')

# 2 Leistungstext: digitale Schließanlage + elektronische Schließzylinder
el = get(d, 'f085e1b')
replace_exact(el, 'editor', 'planen und installieren wir ein Zutrittssystem,<br />bei dem du',
              'planen und installieren wir eine digitale Schließanlage,<br />bei der du')
replace_exact(el, 'editor', 'mit neuen Schließzylindern', 'mit neuen elektronischen Schließzylindern')

# 3 Keyword-Überschrift semantisch als H2 (Typografie ist fest gesetzt, Optik unverändert)
h = get(d, 'ecdc807')
assert h['settings'].get('typography_font_size', {}).get('size'), 'ecdc807 ohne feste Schriftgröße'
h['settings']['header_size'] = 'h2'

# 4 Regionsabschnitt
set_exact(get(d, '51f3331'), 'title', 'Hier findest du <br><span style="font-weight: 700; ">ProVision Infra</span>',
          'Digitale Schließanlagen zwischen <br><span style="font-weight: 700; ">Hamburg und Hannover</span>')
get(d, '51f3331')['settings']['header_size'] = 'h2'
set_exact(get(d, '5c65e03'), 'editor',
          '<p>Wir sitzen in Norddeutschland und sind vor allem im Raum Hamburg, Hannover und Niedersachsen unterwegs. Darüber hinaus sind wir bundesweit im Einsatz.</p><p>Für Beratung, Planung und Umsetzung kommen wir direkt zu dir vor Ort, schauen uns deine Situation an und setzen das System dort um, wo es gebraucht wird.</p>',
          f'<p>Unser Sitz ist Bad Bevensen bei Lüneburg, mitten zwischen Hamburg und Hannover. Von hier aus planen und installieren wir digitale Schließanlagen, elektronische Schließsysteme und <a href="/kamerasysteme/">Videoüberwachung für Unternehmen</a> in ganz Norddeutschland: in {CITY_TEXT}. Darüber hinaus sind wir bundesweit im Einsatz.</p>'
          '<p>Für Beratung, Planung und Umsetzung kommen wir direkt zu dir vor Ort, schauen uns deine Situation an und setzen das System dort um, wo es gebraucht wird. Wenn du die Anlage danach nicht selbst verwalten willst, übernehmen wir das mit unserem <a href="/zutrittssystem/">Rundum-Service für elektronische Schließanlagen</a>.</p>')

# 5 FAQ: Überschrift, Schema-Ausgabe, Fragen als H3, zwei neue Fragen vor „Wie starte ich am besten?“
replace_exact(get(d, '7983242'), 'title', 'Schlüsseln mit', 'Schließanlagen mit')
replace_exact(get(d, '45eaf1f'), 'title', 'Schlüsseln mit', 'Schließanlagen mit')
acc = get(d, 'ed852c3')['settings']
acc['eael_adv_accordion_faq_schema_show'] = 'yes'
acc['eael_adv_accordion_title_tag'] = 'h3'
items = acc['eael_adv_accordion_tab']
assert not any('mechanischer, elektronischer' in i['eael_adv_accordion_tab_title'] for i in items), 'FAQ bereits ergänzt'
new = [
    faq_item(items[0], d, 'Was ist der Unterschied zwischen mechanischer, elektronischer und digitaler Schließanlage?',
             '<p>Bei einer mechanischen Schließanlage öffnet ein Schlüssel die Türen nach einem festen Schließplan. Geht er verloren, müssen oft Zylinder getauscht werden. Eine elektronische Schließanlage arbeitet mit Transpondern, KeyCards oder Codes: Verlorene Medien sperrst du einfach, ohne Schlosswechsel. Ein digitales Schließsystem verwaltest du zusätzlich per Software oder App, mit Zeitprofilen, Zutrittsprotokoll und Berechtigungen nach Abteilung. Wir beraten dich herstellerneutral, welche Lösung zu deinem Betrieb passt.</p>'),
    faq_item(items[0], d, 'In welcher Region installiert ProVision Infra Schließanlagen und Videoüberwachung?',
             f'<p>Unser Sitz ist Bad Bevensen bei Lüneburg. Wir installieren digitale Schließanlagen, elektronische Schließsysteme und Videoüberwachung vor allem in Norddeutschland zwischen Hamburg und Hannover, unter anderem in {CITY_TEXT}. Bei größeren Projekten sind wir bundesweit im Einsatz.</p>'),
]
last = items[-1]
assert last['eael_adv_accordion_tab_title'].startswith('Wie starte ich'), 'unerwartete FAQ-Reihenfolge'
acc['eael_adv_accordion_tab'] = items[:-1] + new + [last]

# 6 Strukturierte Daten
remove_existing_schema_container(d)
d['elements'].append(schema_container(d, [
    org_node(),
    {'@type': 'Service', '@id': f'{SITE}/#schliessanlagen', 'name': 'Digitale und elektronische Schließanlagen für Unternehmen',
     'serviceType': 'Schließanlagen und Zutrittskontrolle', 'url': f'{SITE}/',
     'description': 'Planung, Installation und Betreuung digitaler Schließanlagen und elektronischer Schließsysteme für Unternehmen in Norddeutschland zwischen Hamburg und Hannover.',
     'provider': {'@id': ORG_ID}, 'areaServed': AREA_SERVED,
     'audience': {'@type': 'BusinessAudience', 'name': 'Unternehmen, Betriebe und Praxen'}},
]))
save(d, sys.argv[2])
print('Startseite gepatcht: Hero, Leistungstext, H2, Region, FAQ (+2, Schema an), JSON-LD')
