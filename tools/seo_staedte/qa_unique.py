#!/usr/bin/env python3
"""Eindeutigkeit über alle Stadtseiten: Titles/Descriptions/H1, Textähnlichkeit (6-Wort-Shingles, Haupttext ohne Header/Footer-Navigation)"""
import re, html, json, glob, os, sys, itertools
RAW = sys.argv[1]
def txt(x): return html.unescape(re.sub(r'\s+', ' ', re.sub('<[^>]+>', ' ', x))).strip()
pages = {}
for f in sorted(glob.glob(RAW + '/*.html')):
    k = os.path.basename(f)[:-5]; s = open(f, encoding='utf-8', errors='replace').read()
    head = s.split('</head>', 1)[0]; body = s.split('<body', 1)[1] if '<body' in s else ''
    clean = re.sub(r'<(script|style|noscript|template|svg)\b[^>]*>[\s\S]*?</\1>', ' ', body)
    title = txt((re.search(r'<title[^>]*>([\s\S]*?)</title>', head) or [None, ''])[1])
    desc = (re.search(r'<meta name="description" content="([^"]*)"', head) or [None, ''])[1]
    h1 = [txt(m) for m in re.findall(r'<h1\b[^>]*>([\s\S]*?)</h1>', clean)]
    words = re.findall(r'[A-Za-zÄÖÜäöüß][A-Za-zÄÖÜäöüß\-]+', txt(clean).lower())
    pages[k] = {'title': title, 'desc': html.unescape(desc), 'h1': h1[0] if h1 else '', 'words': words}
for fld in ('title', 'desc', 'h1'):
    seen = {}
    for k, p in pages.items(): seen.setdefault(p[fld], []).append(k)
    dups = {v: ks for v, ks in seen.items() if len(ks) > 1}
    print(f'{fld}: {len(seen)} eindeutig von {len(pages)}', ('DUPLIKATE: ' + str(dups)) if dups else '')
def sh(w, n=6): return {' '.join(w[i:i+n]) for i in range(max(0, len(w) - n + 1))}
S = {k: sh(p['words']) for k, p in pages.items()}
ks = sorted(pages); rows = []
for a, b in itertools.combinations(ks, 2):
    j = len(S[a] & S[b]) / max(1, len(S[a] | S[b])); rows.append((j, a, b))
rows.sort(reverse=True)
print('\nHöchste Textähnlichkeiten (Jaccard, 6-Wort-Shingles, ganze Seite inkl. gemeinsamer Bausteine):')
for j, a, b in rows[:12]: print(f'  {j:.0%}  {a} ~ {b}')
import statistics; print(f'Median über alle Paare: {statistics.median([r[0] for r in rows]):.0%} | Max: {rows[0][0]:.0%} | Min: {rows[-1][0]:.0%}')
print('\nWörter je Seite:', {k: len(p['words']) for k, p in pages.items()})
