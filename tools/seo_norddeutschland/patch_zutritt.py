#!/usr/bin/env python3
"""Zutrittssystem (3316): H1-Keyword, Regionsabschnitt + FAQ im Startseiten-Design, Schema.
Aufruf: python3 -I patch_zutritt.py live.json out.json"""
import copy, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from seo_common import *

d = load(sys.argv[1])
tpl = load(os.path.join(HERE, 'vorlage_startseite_region_faq.json'))
assert not any(e.get('settings', {}).get('_title') == 'Region (SEO)' for e in d['elements']), 'Region bereits eingefügt'

# 1 H1 mit Haupt-Keyword (gleiche Länge wie bisher)
set_exact(get(d, '678aadd9'), 'title',
          '<span style="font-weight: 700;">Wir betreuen dein komplettes Zutrittssystem</span> und das Thema ist für dich dauerhaft abgeschlossen!',
          '<span style="font-weight: 700;">Wir betreuen deine elektronische Schließanlage</span> und das Thema ist für dich dauerhaft abgeschlossen!')

# 2 Regionsabschnitt (Vorlage Startseite) mit eigenen Texten
region = copy.deepcopy(tpl['region'])
rix = {e['id']: e for e in walk(region)}
rix['51f3331']['settings']['title'] = 'Elektronische Schließanlagen zwischen <br><span style="font-weight: 700; ">Hamburg und Hannover</span>'
rix['51f3331']['settings']['header_size'] = 'h2'
rix['5c65e03']['settings']['editor'] = (
    f'<p>Wir betreuen elektronische Schließanlagen und digitale Schließsysteme für Unternehmen in ganz Norddeutschland, von unserem Sitz in Bad Bevensen bei Lüneburg aus, mitten zwischen Hamburg und Hannover. Unsere Techniker sind regelmäßig in {CITY_TEXT} im Einsatz, bei größeren Projekten auch bundesweit.</p>'
    '<p>Du hast noch keine Anlage? Dann planen und installieren wir deine <a href="/">digitale Schließanlage</a> von Grund auf. Auf Wunsch sichern wir dein Gelände zusätzlich mit <a href="/kamerasysteme/">Kamera- und Videoüberwachung</a> ab.</p>')
assert rix['10e8120']['settings']['link']['url'] == '/kontakt'
region['settings']['_title'] = 'Region (SEO)'
region = clone_new_ids(region, d)

# 3 FAQ-Abschnitt (Vorlage Startseite) mit eigenen Fragen
faq = copy.deepcopy(tpl['faq'])
fix = {e['id']: e for e in walk(faq)}
fix['7983242']['settings']['title'] = 'Häufige Fragen zur elektronischen \nSchließanlage mit <b>ProVision Infra</b>'
fix['45eaf1f']['settings']['title'] = 'Häufige Fragen zur elektronischen \nSchließanlage mit <br><b>ProVision Infra</b>'
acc = fix['ed852c3']['settings']
acc['eael_adv_accordion_faq_schema_show'] = 'yes'
acc['eael_adv_accordion_title_tag'] = 'h3'
t0 = acc['eael_adv_accordion_tab'][0]
QA = [
    ('Was gehört zur Betreuung einer elektronischen Schließanlage?',
     '<p>Wir übernehmen alles, was nach dem Einbau anfällt: neue Mitarbeiter anlegen, Berechtigungen ändern, verlorene Transponder oder KeyCards sperren, Zeitprofile pflegen sowie Software- und Sicherheitsupdates einspielen. Du meldest uns die Änderung, wir setzen sie um.</p>'),
    ('Was passiert, wenn ein Transponder oder eine KeyCard verloren geht?',
     '<p>Du gibst uns kurz Bescheid, und das Medium wird in der Software gesperrt. Anders als bei einer mechanischen Schließanlage müssen weder Zylinder noch die ganze Anlage getauscht werden.</p>'),
    ('Kann ich mein Zutrittssystem trotzdem selbst verwalten?',
     '<p>Ja. Berechtigungen kannst du jederzeit selbst in der Software oder App ändern. Mit unserem Service musst du es aber nicht: Wir übernehmen die Pflege, wenn dir im Tagesgeschäft die Zeit dafür fehlt.</p>'),
    ('Für welche Schließanlagen bietet ProVision Infra den Service an?',
     '<p>Für elektronische Schließanlagen und digitale Schließsysteme, die wir planen und installieren, unter anderem mit Komponenten von SimonsVoss, EVVA und NUKI. Ob sich eine bestehende Anlage übernehmen lässt, prüfen wir im Erstgespräch.</p>'),
    ('Lohnt sich eine elektronische Schließanlage auch für kleine Unternehmen?',
     '<p>Ja. Schon bei wenigen Türen sparst du dir Nachschlüssel, Zylinderwechsel nach einem Schlüsselverlust und den Aufwand für Übergaben. Welche Lösung wirtschaftlich passt, rechnen wir im Erstgespräch gemeinsam durch.</p>'),
    ('In welcher Region betreut ProVision Infra elektronische Schließanlagen?',
     f'<p>Unser Sitz ist Bad Bevensen bei Lüneburg. Wir betreuen elektronische Schließanlagen und digitale Schließsysteme vor allem in Norddeutschland zwischen Hamburg und Hannover, unter anderem in {CITY_TEXT}. Bei größeren Projekten sind wir bundesweit im Einsatz.</p>'),
]
acc['eael_adv_accordion_tab'] = [faq_item(t0, d, q, a) for q, a in QA]
faq['settings']['_title'] = 'FAQ (SEO)'
faq = clone_new_ids(faq, d)

# 4 Vor dem Footer einfügen
pos = [i for i, e in enumerate(d['elements']) if e['id'] == '5e012427']
assert pos, 'Footer-Abschnitt 5e012427 fehlt'
d['elements'][pos[0]:pos[0]] = [region, faq]

# 5 Strukturierte Daten
remove_existing_schema_container(d)
d['elements'].append(schema_container(d, [
    org_node(),
    {'@type': 'Service', '@id': f'{SITE}/zutrittssystem/#service', 'name': 'Elektronische Schließanlage mit Rundum-Service',
     'serviceType': 'Betreuung, Wartung und Verwaltung elektronischer Schließanlagen und Zutrittssysteme', 'url': f'{SITE}/zutrittssystem/',
     'description': 'ProVision Infra übernimmt Wartung, Updates und Berechtigungsänderungen deiner elektronischen Schließanlage, für Unternehmen zwischen Hamburg und Hannover.',
     'provider': {'@id': ORG_ID}, 'areaServed': AREA_SERVED,
     'audience': {'@type': 'BusinessAudience', 'name': 'Unternehmen, Betriebe und Praxen'}},
]))
save(d, sys.argv[2])
print('Zutrittssystem gepatcht: H1, Region (neu), FAQ (6 Fragen, neu), JSON-LD')
