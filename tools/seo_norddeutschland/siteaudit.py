#!/usr/bin/env python3
"""Detail-Audit einer Seite: python3 -I siteaudit.py <html>"""
import re, html, json, sys
s = open(sys.argv[1], encoding='utf-8').read()
head = s.split('</head>', 1)[0]; body = s.split('<body', 1)[1]
clean = re.sub(r'<(script|style|noscript|template)[^>]*>[\s\S]*?</\1>', '', body)
clean = re.sub(r'<div id="BorlabsCookieBox"[\s\S]*?</div>\s*</div>\s*</div>', '', clean)
def txt(x): return html.unescape(re.sub(r'\s+', ' ', re.sub('<[^>]+>', ' ', x))).strip()
text = txt(clean)
g = lambda r: html.unescape((re.search(r, head) or [None, ''])[1])
print('TITLE  :', g(r'<title>([^<]+)'), f"({len(g(r'<title>([^<]+)'))})")
print('DESC   :', g(r'<meta name="description" content="([^"]+)"'), f"({len(g(r'<meta name=\"description\" content=\"([^\"]+)\"'))})")
print('ROBOTS :', g(r"<meta name='robots' content='([^']+)'"), '| CANON:', g(r'rel="canonical" href="([^"]+)"'))
# Headings in DOM-Reihenfolge, Duplikate (Mobil/Desktop-Varianten) zusammenfassen
seen = []
for m in re.finditer(r'<(h[1-4])[^>]*>([\s\S]*?)</\1>', clean):
    t = txt(m.group(2))
    if t and (m.group(1), t) not in seen: seen.append((m.group(1), t))
print('HEADINGS:')
for h, t in seen: print(f'   {h}: {t[:110]}')
words = re.findall(r"[A-Za-zÄÖÜäöüß][A-Za-zÄÖÜäöüß\-]+", text)
print('WÖRTER :', len(words))
kws = ['Schließanlage', 'Schließsystem', 'elektronische Schließanlage', 'elektronisches Schließsystem', 'elektronischen Schließ', 'digitale Schließanlage', 'digitales Schließsystem', 'digitalen Schließ', 'Zutrittssystem', 'Zutrittskontrolle', 'Videoüberwachung', 'Kameraüberwachung', 'Kamerasystem', 'Überwachungskamera', 'Hamburg', 'Hannover', 'Norddeutschland', 'Niedersachsen', 'Lüneburg', 'Uelzen', 'Celle', 'Bad Bevensen']
print('KEYWORDS:', {k: len(re.findall(re.escape(k), text, re.I)) for k in kws})
links = re.findall(r'<a[^>]*href="([^"#]+)"', clean)
internal = sorted({l.replace('https://provision-infra.de', '') or '/' for l in links if l.startswith('/') or 'provision-infra.de' in l})
print('INTERNE LINKS:', internal)
imgs = re.findall(r'<img[^>]*>', clean)
noalt = []
for im in imgs:
    a = re.search(r'alt="([^"]*)"', im); src = re.search(r'(?:data-lazy-src|src)="([^"]+)"', im)
    if (not a or not a.group(1).strip()) and src and not src.group(1).startswith('data:'): noalt.append(src.group(1).split('/')[-1][:60])
print(f'BILDER : {len(imgs)} | ohne Alt: {len(noalt)} ->', sorted(set(noalt)))
types = []
for m in re.finditer(r'<script type="application/ld\+json"[^>]*>([\s\S]*?)</script>', s):
    try:
        j = json.loads(m.group(1)); types.append([(x.get('@type'), (x.get('areaServed') and [a.get('name') for a in x['areaServed']])) for x in j.get('@graph', [j])])
    except Exception as e: types.append('INVALID ' + str(e)[:50])
print('SCHEMA :', types)
