#!/usr/bin/env python3
"""On-Page-Audit der Live-Seite: python3 -I audit.py <html-datei> [--json out.json]"""
import re, html, json, sys
path = sys.argv[1]; s = open(path, encoding='utf-8').read()
head = s.split('</head>', 1)[0]; body = s.split('<body', 1)[1]
clean = re.sub(r'<(script|style|noscript|template)[^>]*>[\s\S]*?</\1>', '', body)
# Cookie-Dialog und Admin-Bar herausrechnen
clean = re.sub(r'<div id="BorlabsCookieBox"[\s\S]*?</div>\s*</div>\s*</div>', '', clean)
text = html.unescape(re.sub(r'\s+', ' ', re.sub('<[^>]+>', ' ', clean)))
words = re.findall(r"[A-Za-zÄÖÜäöüß][A-Za-zÄÖÜäöüß\-]+", text)
g = lambda re_: (re.search(re_, head) or [None, ''])[1]
title = html.unescape(g(r'<title>([^<]+)')); desc = html.unescape(g(r'<meta name="description" content="([^"]+)"'))
res = {
  'title': title, 'title_len': len(title), 'description': desc, 'description_len': len(desc),
  'canonical': g(r'rel="canonical" href="([^"]+)"'), 'robots': g(r"<meta name='robots' content='([^']+)'"),
  'og_title': g(r'property="og:title" content="([^"]+)"'), 'og_image': g(r'property="og:image" content="([^"]+)"'),
  'h1': [html.unescape(re.sub('<[^>]+>', ' ', h)).strip() for h in re.findall(r'<h1[^>]*>([\s\S]*?)</h1>', clean)],
  'h2_count': len(re.findall(r'<h2[^>]*>', clean)), 'h3_count': len(re.findall(r'<h3[^>]*>', clean)),
  'words': len(words),
  'images': len(re.findall(r'<img ', clean)), 'images_alt_empty': len(re.findall(r'<img[^>]*alt=""', clean)),
  'internal_links': sorted(set(re.findall(r'href="(?:https://provision-infra\.de)?(/[a-z0-9\-/]+/?)"', clean))),
  'tel_links': len(re.findall(r'href="tel:', clean)), 'mailto_links': len(re.findall(r'href="mailto:', clean)),
  'schema_types': [],
  'keywords': {},
}
for m in re.finditer(r'<script type="application/ld\+json"[^>]*>([\s\S]*?)</script>', s):
    try:
        j = json.loads(m.group(1)); gph = j.get('@graph', [j])
        res['schema_types'].append([x.get('@type') for x in gph])
    except Exception as e: res['schema_types'].append('INVALID: ' + str(e)[:60])
for kw in ['Schließanlagen Lüneburg', 'Schließanlage', 'Videoüberwachung', 'Videoüberwachung in Lüneburg', 'Zutrittskontrolle', 'Kamerasystem', 'Lüneburg', 'Bad Bevensen', 'Zutrittssystem', 'EVVA', 'SimonsVoss', 'TP-Link']:
    res['keywords'][kw] = len(re.findall(re.escape(kw), text, re.I))
res['faq_questions'] = len(re.findall(r'eael-accordion-tab-title|eael-accordion-header', clean)) // 1
if '--json' in sys.argv: json.dump(res, open(sys.argv[sys.argv.index('--json') + 1], 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for k, v in res.items(): print(f'{k}: {v}')
