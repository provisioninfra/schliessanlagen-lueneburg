#!/usr/bin/env python3
"""Baut die Elementor-Daten (elements + page settings) fuer die Seiten
/lueneburg/, /funnel-unterseite/ und /kontakt-kombiniert/ aus den Dumps der
bestehenden Seiten (Kamerasysteme #4313, Startseite #31, Kontakt Kamerasysteme #4371).

Aufruf: build_lueneburg.py <dump-dir> <out-dir> [--funnel-form-id N] [--combo-form-id N]
"""
import copy, json, os, random, re, sys

DUMP = sys.argv[1]; OUT = sys.argv[2]
args = sys.argv[3:]
FUNNEL_FORM_ID = args[args.index('--funnel-form-id')+1] if '--funnel-form-id' in args else '4'
COMBO_FORM_ID = args[args.index('--combo-form-id')+1] if '--combo-form-id' in args else '4'

K = json.load(open(f'{DUMP}/elementor_4313.json', encoding='utf-8'))   # Kamerasysteme
H = json.load(open(f'{DUMP}/elementor_31.json', encoding='utf-8'))     # Startseite
C = json.load(open(f'{DUMP}/elementor_4371.json', encoding='utf-8'))   # Kontakt Kamerasysteme

FUNNEL_URL = '/funnel-unterseite/'
SITE = 'https://provision-infra.de'

def _find(els, eid):
    for e in els:
        if e['id'] == eid: return e
        r = _find(e.get('elements', []), eid)
        if r: return r
    return None

def find(els, eid):
    r = _find(els, eid)
    if r is None: raise KeyError(eid)
    return r

def grab(doc, eid):
    """Tiefe Kopie eines Elements; htmlCache entfernen (wird von Elementor neu erzeugt)."""
    e = copy.deepcopy(find(doc['elements'], eid))
    def strip(x):
        x.pop('htmlCache', None)
        for c in x.get('elements', []): strip(c)
    strip(e)
    return e

def walk(e):
    yield e
    for c in e.get('elements', []): yield from walk(c)

def set_setting(root, eid, key, value):
    find([root], eid)['settings'][key] = value

def replace_text(root, mapping):
    """Ersetzt exakte Textvorkommen in allen String-Settings (auch in verschachtelten Listen)."""
    def rep(v):
        if isinstance(v, str):
            for a, b in mapping.items():
                if a in v: v = v.replace(a, b)
            return v
        if isinstance(v, list): return [rep(x) for x in v]
        if isinstance(v, dict): return {k: rep(x) for k, x in v.items()}
        return v
    for e in walk(root):
        e['settings'] = rep(e['settings'])

used_ids = set()
def new_id():
    while True:
        i = '%07x' % random.randrange(16**7)
        if i not in used_ids:
            used_ids.add(i); return i

def relink(root, old, new):
    for e in walk(root):
        l = e['settings'].get('link')
        if isinstance(l, dict) and l.get('url') == old: l['url'] = new

# ---------------------------------------------------------------- Inhalte
H1 = '<span style="font-weight: 700;">Mechanische &amp; elektronische Schließanlagen</span><br>sowie Videoüberwachung in Lüneburg'
HERO_SUB = ('Ein verlorener Schlüssel, ein unbeobachteter Hof, eine Tür, die nachts offen steht: '
            'Jede dieser Lücken kostet Lüneburger Betriebe schnell einen fünfstelligen Betrag. <br><br>'
            'ProVision Infra plant, installiert und betreut deine Schließanlage und dein Kamerasystem – mechanisch, '
            'elektronisch oder kombiniert. Von unserem Sitz in Bad Bevensen sind wir in rund einer halben Stunde bei dir in Lüneburg.')

INTRO = {
    'Solange nichts passiert, denkt kaum jemand an Kameras.':
        'Sicherheitstechnik für Lüneburg – geplant und montiert aus der Region.',
    '<p>Erst nach dem Einbruch wird klar, was fehlt. Ohne verwertbare Aufnahmen hat die Polizei nichts in der Hand, und die Versicherung verlangt Belege, die du nicht liefern kannst. Der Schaden bleibt an dir hängen.</p>':
        '<p>Unser Sitz liegt in Bad Bevensen im Landkreis Uelzen, rund 30 Kilometer südlich von Lüneburg. Beratung, Aufmaß, Montage und Service übernehmen wir selbst – ohne Subunternehmer, ohne lange Anfahrt und mit einem festen Ansprechpartner.</p>',
    '<p>Mit einer Videoüberwachung von ProVision Infra siehst du jederzeit per App, was auf deinem Gelände passiert. Dein Handy meldet sich bei Bewegung, und im Ernstfall hast du Aufnahmen, mit denen Polizei und Versicherung arbeiten können.</p>':
        '<p>Ob Handwerksbetrieb in der Lüneburger Altstadt, Lager im Gewerbegebiet am Stadtrand oder Praxis in Adendorf: Wir sehen uns dein Objekt vor Ort an und planen Schließanlage und Kameras so, dass beides zusammenpasst – ein Konzept, ein Angebot, ein Ansprechpartner.</p>',
}

CARDS_HEAD = {
    'Was ohne Kameras <span style="font-weight: 700; ">auf deinem Gelände passiert?</span>':
        'Schließanlagen für Lüneburg: <span style="font-weight: 700; ">mechanisch, elektronisch oder kombiniert</span>',
    '<p>Fünf Situationen, die jeden Betrieb treffen können. Ohne Kameras passiert Folgendes, wenn …</p>':
        '<p>Vom klassischen Schließzylinder bis zur App-gesteuerten Zutrittskontrolle: fünf Lösungen, die wir in Lüneburg und Umgebung planen, einbauen und betreuen.</p>',
}
CARDS = [
    # (titel, text, folge)
    ('Mechanische Schließanlagen',
     '<p>Gleichschließende und zentral geschlossene Anlagen mit Sicherungskarte, zum Beispiel von EVVA. Ein Schlüssel pro Person, ein Schließplan für das ganze Gebäude – vom Haupteingang bis zum Serverraum.</p>',
     '<p>Kopierschutz und Schließplan sorgen dafür, dass du jederzeit weißt, welcher Schlüssel welche Tür in deinem Betrieb öffnet.</p>'),
    ('Elektronische Schließanlagen',
     '<p>Digitale Zylinder und Beschläge, zum Beispiel von SimonsVoss: Zutritt per Transponder, KeyCard oder App. Berechtigungen vergibst und entziehst du in Sekunden – für Mitarbeitende, Reinigung, Handwerker oder Lieferanten.</p>',
     '<p>Geht ein Transponder verloren, sperrst du ihn mit einem Klick – statt Zylinder zu tauschen und neue Schlüssel zu verteilen.</p>'),
    ('Smarte Türschlösser für Büro, Praxis und kleine Betriebe',
     '<p>Nachrüstbare Lösungen wie NUKI für einzelne Türen: ohne Verkabelung, in wenigen Stunden montiert, bedienbar per App, Code oder Transponder.</p>',
     '<p>Zeitfenster für Reinigungskräfte, Handwerker oder Gäste richtest du selbst am Handy ein – ohne Schlüsselübergabe.</p>'),
    ('Umrüstung bestehender Schließanlagen',
     '<p>Du hast bereits eine mechanische Anlage? Wir ersetzen einzelne Zylinder durch digitale Komponenten und bauen schrittweise um, während der Betrieb weiterläuft. Herstellerneutral mit EVVA, SimonsVoss, Keyota, Keyrent und NUKI.</p>',
     '<p>Kein Stillstand und keine neue Anlage auf einen Schlag – am Ende stimmt der Schließplan wieder und jede Tür ist dokumentiert.</p>'),
    ('Zutritt und Videoüberwachung aus einer Hand',
     '<p>Schließanlage und Kamerasystem planen wir gemeinsam: Wer wann welche Tür geöffnet hat, siehst du im Protokoll – und auf der Aufnahme, was dabei passiert ist.</p>',
     '<p>Eine Begehung in Lüneburg, ein Konzept, ein Ansprechpartner – für Türen, Tore und Gelände.</p>'),
]
CARD5_HINT = {
    '<p>Selbst mit Versicherung musst du beweisen, dass es ein Einbruch war. Ohne Aufnahmen steht nur dein Wort.</p>':
        '<p>Kameras von TP-Link VIGI, Zutritt von EVVA, SimonsVoss, Keyota, Keyrent oder NUKI – wir wählen die Technik nach deinem Objekt aus, nicht nach Katalog.</p>',
}

GLASS = {
    'So arbeiten wir': 'Video- &amp; Kameraüberwachung in Lüneburg',
    'Jede Kamera planen wir nach einer Begehung vor Ort. Im Ernstfall zeigt sie den Täter, nicht den Parkplatz.':
        'Jede Kamera planen wir nach einer Begehung vor Ort in Lüneburg. Im Ernstfall zeigt sie den Täter, nicht den Parkplatz.',
    'Aufzeichnung und App sind eingerichtet, bevor wir vom Hof fahren. Dein Handy schlägt ab dem ersten Tag Alarm.':
        'Live-Bild und Aufzeichnung siehst du per App. Dein Handy meldet sich, sobald sich nachts jemand am Tor, am Lager oder auf dem Hof bewegt.',
    '<p>Übergeben wird erst, wenn du nachts Gesichter erkennst. Das Ergebnis bekommst du schriftlich.</p>':
        '<p>Die Aufnahmen bleiben auf deinem Rekorder im Gebäude, datenschutzkonform mit Hinweisschildern. Polizei und Versicherung bekommen Bilder, die etwas beweisen.</p>',
}

TIMELINE = {
    '<p>Wir gehen mit dir über das Gelände und suchen die Stellen, an denen jemand ungesehen reinkommt. Den Kostenrahmen nennen wir dir noch vor Ort.</p>':
        '<p>Wir kommen zu dir nach Lüneburg, gehen durch das Gebäude und über das Gelände und zeigen dir, wo Schlüssel, Türen und Kameras heute Lücken lassen. Den Kostenrahmen nennen wir dir noch vor Ort.</p>',
    '<p>Die Kameras montieren wir, Aufzeichnung und App richten wir komplett ein. Du musst nichts selbst konfigurieren.</p>':
        '<p>Zylinder, Beschläge und Kameras montieren wir, Schließplan, Software und App richten wir komplett ein. Du musst nichts selbst konfigurieren.</p>',
    '<p>Ein kurzes Telefonat: Was ist passiert, oder was soll nie passieren? Du bekommst eine erste ehrliche Einschätzung.</p>':
        '<p>Ein kurzes Telefonat: Geht es um Schlüssel, um Kameras oder um beides? Du bekommst eine erste ehrliche Einschätzung.</p>',
    'Planung deines Kamerasystems': 'Planung deines Systems',
    '<p>Du bekommst ein Konzept mit Kamerastandorten und ein Angebot, das zu deinem Budget passt. Dann entscheidest du.</p>':
        '<p>Du bekommst ein Konzept mit Schließplan und Kamerastandorten sowie ein Angebot, das zu deinem Budget passt. Dann entscheidest du.</p>',
}

MAP = {
    'Hier findest du <br><span style="font-weight: 700; ">ProVision Infra</span>':
        'ProVision Infra <br><span style="font-weight: 700; ">in Lüneburg und Umgebung</span>',
    '<p>Wir sitzen in Norddeutschland und sind vor allem im Raum Hamburg, Hannover und Niedersachsen unterwegs. Darüber hinaus sind wir bundesweit im Einsatz.</p><p>Für Beratung, Planung und Umsetzung kommen wir direkt zu dir vor Ort, schauen uns deine Situation an und setzen das System dort um, wo es gebraucht wird.</p>':
        '<p>Unser Sitz ist Bad Bevensen, rund 30 Kilometer von Lüneburg entfernt. Regelmäßig sind wir in Lüneburg, Adendorf, Bardowick, Reppenstedt, Scharnebeck, Bleckede, Winsen (Luhe), Uelzen und im gesamten Landkreis Lüneburg unterwegs.</p><p>Für Beratung, Aufmaß und Montage kommen wir direkt zu dir, sehen uns Türen, Zugänge und Gelände an und setzen Schließanlage und Kameras dort um, wo sie gebraucht werden.</p>',
}

FAQ = [
    ('Was kostet eine Schließanlage in Lüneburg?',
     '<p>Das hängt von der Zahl der Türen, der Art der Zylinder und davon ab, ob die Anlage mechanisch, elektronisch oder kombiniert sein soll. Eine mechanische Anlage für ein kleines Büro liegt deutlich unter einer digitalen Lösung mit App-Steuerung. Einen ersten Rahmen bekommst du im Erstgespräch, einen verbindlichen Preis nach dem Termin vor Ort.</p>'),
    ('Mechanische oder elektronische Schließanlage – was passt zu meinem Betrieb?',
     '<p>Wenige Türen und wenig Wechsel beim Personal: Dann reicht oft eine mechanische Anlage mit Sicherungskarte. Viele Mitarbeitende, Dienstleister oder mehrere Standorte: Dann lohnt sich eine elektronische Anlage, weil du Berechtigungen in Sekunden änderst. Häufig ist eine Mischung sinnvoll – wir beraten dich herstellerneutral.</p>'),
    ('Kann ich meine bestehende Schließanlage auf elektronisch umrüsten?',
     '<p>Ja. Digitale Zylinder von SimonsVoss oder smarte Schlösser wie NUKI lassen sich in vorhandene Türen einsetzen, meist ohne Verkabelung. Wir rüsten schrittweise um, der Betrieb läuft weiter.</p>'),
    ('Wie schnell seid ihr in Lüneburg vor Ort?',
     '<p>Von Bad Bevensen sind wir in rund einer halben Stunde in Lüneburg. Termine für Begehung und Montage stimmen wir so ab, dass dein Betrieb nicht stillsteht – auch in Adendorf, Bardowick, Reppenstedt oder Winsen (Luhe).</p>'),
    ('Darf ich mein Firmengelände in Lüneburg per Kamera überwachen?',
     '<p>Ja, innerhalb klarer Regeln. Erlaubt ist dein eigenes Gelände samt Zugängen, nicht der Gehweg oder das Nachbargrundstück. Mitarbeitende müssen informiert sein, ein Hinweisschild ist Pflicht. Wir planen die Kamerawinkel entsprechend und geben dir Schilder und Unterlagen mit.</p>'),
    ('Kann ich Zutritt und Kameras in einem System verbinden?',
     '<p>Ja. Öffnet jemand eine Tür per Transponder oder App, siehst du im Protokoll, wer es war, und auf der Aufnahme, was passiert ist. Wir planen beides zusammen, damit Kamerastandorte und Zugänge zueinander passen.</p>'),
    ('Welche Hersteller verbaut ProVision Infra?',
     '<p>Bei Schließanlagen arbeiten wir unter anderem mit EVVA, SimonsVoss, Keyota, Keyrent und NUKI, bei Kamerasystemen mit TP-Link VIGI. Welche Komponenten zu dir passen, entscheiden wir nach der Begehung – nicht nach Katalog.</p>'),
    ('Was passiert nach der Installation?',
     '<p>Wir übergeben die Anlage erst, wenn alles so funktioniert wie vereinbart, und halten das schriftlich fest. Danach bleiben wir Ansprechpartner für Erweiterungen, Nachschlüssel, neue Transponder und Wartung.</p>'),
]

def strip_tags(s): return re.sub(r'\s+', ' ', re.sub('<[^>]+>', '', s)).replace('&amp;', '&').strip()

SEO_TITLE = 'Schließanlagen & Videoüberwachung Lüneburg | ProVision Infra'
SEO_DESC = ('Mechanische & elektronische Schließanlagen und Videoüberwachung in Lüneburg: ProVision Infra plant, '
            'installiert und betreut dein System vor Ort.')
assert len(SEO_TITLE) <= 60, len(SEO_TITLE)
assert len(SEO_DESC) <= 160, len(SEO_DESC)

SCHEMA = {
  "@context": "https://schema.org",
  "@graph": [
    {"@type": ["LocalBusiness", "Locksmith"], "@id": f"{SITE}/#organisation", "name": "ProVision Infra GmbH",
     "url": f"{SITE}/", "logo": f"{SITE}/wp-content/uploads/2026/10/kamera-logo-provision-infra-1032.png",
     "image": f"{SITE}/wp-content/uploads/2026/05/provision_header_02-1.png",
     "telephone": "+49 5821 4049040", "email": "info@provision-infra.de",
     "address": {"@type": "PostalAddress", "streetAddress": "Klein Hesebecker Straße 11", "postalCode": "29549",
                 "addressLocality": "Bad Bevensen", "addressRegion": "Niedersachsen", "addressCountry": "DE"},
     "openingHoursSpecification": [
        {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday"], "opens": "09:00", "closes": "18:00"},
        {"@type": "OpeningHoursSpecification", "dayOfWeek": "Friday", "opens": "09:00", "closes": "14:00"}],
     "areaServed": [{"@type": "City", "name": "Lüneburg"}, {"@type": "AdministrativeArea", "name": "Landkreis Lüneburg"},
                    {"@type": "City", "name": "Bad Bevensen"}, {"@type": "City", "name": "Uelzen"},
                    {"@type": "City", "name": "Hamburg"}, {"@type": "State", "name": "Niedersachsen"}],
     "sameAs": ["https://www.instagram.com/provision_infra_gmbh/", "https://www.facebook.com/share/1CWs2rohMt/",
                "https://www.linkedin.com/company/provision-infra-gmbh-i-g/"]},
    {"@type": "WebPage", "@id": f"{SITE}/lueneburg/#webpage", "url": f"{SITE}/lueneburg/", "name": SEO_TITLE,
     "description": SEO_DESC, "inLanguage": "de", "isPartOf": {"@id": f"{SITE}/#website"},
     "about": {"@id": f"{SITE}/#organisation"}, "breadcrumb": {"@id": f"{SITE}/lueneburg/#breadcrumb"}},
    {"@type": "BreadcrumbList", "@id": f"{SITE}/lueneburg/#breadcrumb", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Startseite", "item": f"{SITE}/"},
        {"@type": "ListItem", "position": 2, "name": "Schließanlagen & Videoüberwachung Lüneburg", "item": f"{SITE}/lueneburg/"}]},
    {"@type": "Service", "@id": f"{SITE}/lueneburg/#schliessanlagen", "name": "Mechanische und elektronische Schließanlagen in Lüneburg",
     "serviceType": "Schließanlagen und Zutrittskontrolle", "url": f"{SITE}/lueneburg/#schliessanlagen",
     "description": "Planung, Montage und Betreuung mechanischer und elektronischer Schließanlagen (EVVA, SimonsVoss, Keyota, Keyrent, NUKI) für Unternehmen in Lüneburg und im Landkreis Lüneburg.",
     "provider": {"@id": f"{SITE}/#organisation"},
     "areaServed": [{"@type": "City", "name": "Lüneburg"}, {"@type": "AdministrativeArea", "name": "Landkreis Lüneburg"}],
     "audience": {"@type": "BusinessAudience", "name": "Unternehmen, Betriebe und Praxen"}},
    {"@type": "Service", "@id": f"{SITE}/lueneburg/#kamera", "name": "Video- und Kameraüberwachung in Lüneburg",
     "serviceType": "Videoüberwachung", "url": f"{SITE}/lueneburg/#kamera",
     "description": "Planung und Installation von Kamerasystemen (TP-Link VIGI) mit App-Zugriff und lokaler Aufzeichnung für Betriebe in Lüneburg und Umgebung.",
     "provider": {"@id": f"{SITE}/#organisation"},
     "areaServed": [{"@type": "City", "name": "Lüneburg"}, {"@type": "AdministrativeArea", "name": "Landkreis Lüneburg"}],
     "audience": {"@type": "BusinessAudience", "name": "Unternehmen, Betriebe und Gewerbe"}},
    {"@type": "FAQPage", "@id": f"{SITE}/lueneburg/#faq", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}} for q, a in FAQ]},
  ]
}

# ---------------------------------------------------------------- Seite /lueneburg/
els = []

# 1 Header
header = grab(K, '192a273')
set_setting(header, '2a487ab', 'menu', 'lueneburg')
els.append(header)

# 2 Hero (Startseite: Tuer-Video) + mobiler Videoblock + Kennzahlen (mobil)
hero = grab(H, '0f0c707')
set_setting(hero, '9dcea29', 'title', H1)
set_setting(hero, 'e429076', 'title', HERO_SUB)
relink(hero, '/kontakt', FUNNEL_URL)
els.append(hero)
els.append(grab(H, 'd135e80'))
els.append(grab(K, '67b8213'))

# 3 Intro / Region (Logo + drei Punkte)
intro = grab(K, '371b95f')
replace_text(intro, INTRO)
set_setting(intro, '371b95f', '_element_id', 'region')
set_setting(intro, '371b95f', '_title', 'Region Lüneburg')
els.append(intro)

# 4 Schliessanlagen-Karten
cards = grab(K, 'd7f768f')
replace_text(cards, CARDS_HEAD)
replace_text(cards, CARD5_HINT)
set_setting(cards, 'd7f768f', '_element_id', 'schliessanlagen')
set_setting(cards, 'd7f768f', '_title', 'Schließanlagen Lüneburg')
set_setting(cards, '74b6d54', '_title', 'Schließanlagen Lüneburg')
card_ids = ['94cb6e5', '32b0c9f', 'f0e4802', '0d4babd', 'a98086e']
for cid, (t, txt, folge) in zip(card_ids, CARDS):
    card = find([cards], cid)
    card['settings']['_title'] = t
    ws = [w for w in walk(card) if w.get('elType') == 'widget']
    headings = [w for w in ws if w['widgetType'] == 'heading']
    texts = [w for w in ws if w['widgetType'] == 'text-editor']
    headings[0]['settings']['title'] = t
    headings[0]['settings']['_title'] = t
    texts[0]['settings']['editor'] = txt
    texts[-1]['settings']['editor'] = folge  # Folge-Box ist immer der letzte Text-Editor
relink(cards, '/kontakt-kamerasysteme/', FUNNEL_URL)
els.append(cards)

# 5 Kamera: Glass-Cards
glass = grab(K, 'd70fb3d')
replace_text(glass, GLASS)
set_setting(glass, 'd70fb3d', '_element_id', 'kamera')
set_setting(glass, 'd70fb3d', '_title', 'Videoüberwachung Lüneburg')
els.append(glass)

# 6 Technik-Karussell (TP-Link VIGI)
tech = grab(K, 'f9348eb')
set_setting(tech, 'f9348eb', '_element_id', 'technik')
els.append(tech)

# 7 Testimonials
els.append(grab(K, '7cfc047c'))

# 8 Ablauf
ablauf = grab(K, 'a3437e1')
replace_text(ablauf, TIMELINE)
els.append(ablauf)

# 9 Gruender
gruender = grab(K, 'a4e4757')
set_setting(gruender, 'a4e4757', '_element_id', 'ueber')
els.append(gruender)
els.append(grab(K, 'bec6cfd'))

# 10 Standort / Karte
karte = grab(K, '55b8573')
replace_text(karte, MAP)
set_setting(karte, '55b8573', '_element_id', 'standort')
relink(karte, '/kontakt-kamerasysteme/', FUNNEL_URL)
els.append(karte)

# 11 FAQ
faq = grab(K, 'b0720cd')
set_setting(faq, '7983242', 'title', 'Häufige Fragen zu Schließanlagen &amp; Videoüberwachung in <b>Lüneburg</b>')
set_setting(faq, '45eaf1f', 'title', 'Häufige Fragen zu Schließanlagen &amp; <br>Videoüberwachung in <b>Lüneburg</b>')
acc = find([faq], 'ed852c3')['settings']
tmpl = acc['eael_adv_accordion_tab'][0]
acc['eael_adv_accordion_tab'] = []
for q, a in FAQ:
    item = copy.deepcopy(tmpl)
    item['eael_adv_accordion_tab_title'] = q
    item['eael_adv_accordion_tab_content'] = a
    item['_id'] = new_id()
    acc['eael_adv_accordion_tab'].append(item)
els.append(faq)

# 12 Partner, Footer, ProvenExpert-Badge
els.append(grab(K, '88956c0'))
footer = grab(K, '9fafb57')
els.append(footer)
els.append(grab(K, 'af73376'))

# 13 Strukturierte Daten (nur Schema, ohne Video-Steuerung der Kamera-Seite)
sd = grab(K, '730dd41')
sd['elements'] = [w for w in sd['elements'] if w['id'] == 'f058554']
sd['settings']['_title'] = 'Strukturierte Daten (SEO)'
find([sd], 'f058554')['settings']['html'] = '<script type="application/ld+json">' + json.dumps(SCHEMA, ensure_ascii=False) + '</script>'
els.append(sd)

# Pruefung: keine Rest-Links auf die Kamera-/Zutrittsfunnel, keine doppelten IDs
ids = [e['id'] for root in els for e in walk(root)]
dups = {i for i in ids if ids.count(i) > 1}
assert not dups, dups
for root in els:
    for e in walk(root):
        l = e['settings'].get('link')
        if isinstance(l, dict) and l.get('url') in ('/kontakt', '/kontakt-kamerasysteme/'):
            raise SystemExit(f"Alter CTA-Link in {e['id']}")

page_settings = copy.deepcopy(H['settings'])
page_settings.update({'post_title': 'Schließanlagen & Videoüberwachung Lüneburg', 'post_status': 'draft',
                      'custom_css': H['settings']['custom_css']})

json.dump({'elements': els, 'settings': page_settings,
           'seo': {'title': SEO_TITLE, 'description': SEO_DESC, 'focuskw': 'Schließanlagen Lüneburg',
                   'slug': 'lueneburg', 'robots_noindex': '2',
                   'og_image': f'{SITE}/wp-content/uploads/2026/05/provision_header_02-1.png'}},
          open(f'{OUT}/lueneburg.elementor.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# ---------------------------------------------------------------- Funnel- und Kombi-Seite (Vorlage: Kontakt Kamerasysteme)
def contact_page(title, heading, text, form_id, slug, seo_title):
    root = grab(C, '3d963d8')
    for e in walk(root): e['id'] = new_id()
    ws = [w for w in walk(root) if w.get('elType') == 'widget']
    ws[0]['settings']['title'] = heading
    ws[1]['settings']['editor'] = text
    ws[2]['settings']['contact_form_list'] = str(form_id)
    settings = copy.deepcopy(C['settings']); settings.update({'post_title': title, 'post_status': 'draft'})
    return {'elements': [root], 'settings': settings,
            'seo': {'title': seo_title, 'description': '', 'focuskw': '', 'slug': slug, 'robots_noindex': '1'}}

json.dump(contact_page('Funnel-Unterseite',
    'Wofür suchst du eine Lösung?',
    '<p>Wähle aus, worum es bei dir geht: Schließsystem, Kamerasystem oder beides. Danach stellen wir dir ein paar kurze Fragen, damit sich unser Team optimal auf dein Erstgespräch vorbereiten kann.</p>',
    FUNNEL_FORM_ID, 'funnel-unterseite', 'Anfrage – ProVision Infra'),
    open(f'{OUT}/funnel-unterseite.elementor.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

json.dump(contact_page('Kontakt Schließ- & Kamerasysteme',
    'Bitte fülle den Fragebogen aus, damit sich unser Team bestmöglich auf deinen Termin vorbereiten kann. Im nächsten Schritt kannst du ein Datum und eine Uhrzeit für dein Gespräch auswählen.',
    '<p>Im Gespräch klären wir, welche Türen und Zugänge du regeln willst, welche Bereiche du im Blick haben willst und wie beides zusammenspielt. Dazu bekommst du eine erste Einschätzung zu Aufwand und Kosten.</p>',
    COMBO_FORM_ID, 'kontakt-kombiniert', 'Kontakt Schließ- & Kamerasysteme – ProVision Infra'),
    open(f'{OUT}/kontakt-kombiniert.elementor.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

print('OK', len(els), 'Abschnitte;', len(ids), 'Elemente; FAQ', len(FAQ))
