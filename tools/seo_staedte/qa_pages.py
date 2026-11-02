#!/usr/bin/env python3
"""Live-HTML-Prüfung der Stadtseiten: python3 -I qa_pages.py <raw-dir> key [key...]  (lädt HTML per curl, prüft Meta/H1/Schema/FAQ/Links/Bilder)"""
import subprocess, re, json, html, sys, os, time
sys.path.insert(0, '/home/user/schliessanlagen-lueneburg/tools/seo_staedte'); from cities import CITIES, ALL_CITY_LINKS
RAW = sys.argv[1]; os.makedirs(RAW, exist_ok=True); keys = sys.argv[2:] or [c['key'] for c in CITIES]
UA = 'Mozilla/5.0 (compatible; ProVisionSEOAudit/1.0)'; SITE = 'https://provision-infra.de'
prof = {c['key']: c for c in CITIES}
def attr(tag, name):
    m = re.search(r'(?:^|\s)' + re.escape(name) + r'\s*=\s*("([^"]*)"|\'([^\']*)\')', tag)
    return html.unescape(m.group(2) if m and m.group(2) is not None else (m.group(3) if m else '')) if m else None
def txt(x): return html.unescape(re.sub(r'\s+', ' ', re.sub('<[^>]+>', ' ', x))).strip()
seen_img = {}; report = {}
for key in keys:
    c = prof[key]; url = f'{SITE}/{key}/'
    r = subprocess.run(['curl', '-sS', '--http1.1', '-A', UA, '--max-time', '90', '-D', f'{RAW}/{key}.hdr', '-o', f'{RAW}/{key}.html', '-w', '%{http_code} %{time_total}', url], capture_output=True, text=True)
    code = r.stdout.split()[0] if r.stdout else '000'
    s = open(f'{RAW}/{key}.html', encoding='utf-8', errors='replace').read() if os.path.exists(f'{RAW}/{key}.html') else ''
    head = s.split('</head>', 1)[0]; body = s.split('<body', 1)[1] if '<body' in s else ''
    clean = re.sub(r'<(script|style|noscript|template|svg)\b[^>]*>[\s\S]*?</\1>', ' ', body)
    metas = re.findall(r'<meta\b[^>]*>', head)
    def meta(n, k='name'):
        for m in metas:
            if (attr(m, k) or '').lower() == n: return attr(m, 'content') or ''
        return ''
    title = txt((re.search(r'<title[^>]*>([\s\S]*?)</title>', head) or [None, ''])[1])
    canon = (re.search(r'rel="canonical" href="([^"]+)"', head) or [None, ''])[1]
    h1 = [txt(m) for m in re.findall(r'<h1\b[^>]*>([\s\S]*?)</h1>', clean)]
    hs = []
    for m in re.finditer(r'<(h[1-6])\b[^>]*>([\s\S]*?)</\1>', clean):
        t = txt(m.group(2))
        if t and (m.group(1), t) not in hs: hs.append((m.group(1), t))
    main = re.sub(r'<div class="[^"]*elementor-location-footer[\s\S]*$', '', clean)
    text = txt(main); words = len(re.findall(r'[A-Za-zÄÖÜäöüß][A-Za-zÄÖÜäöüß\-]+', text))
    sch = []; invalid = 0
    for m in re.finditer(r'<script type="application/ld\+json"[^>]*>([\s\S]*?)</script>', s):
        try:
            j = json.loads(m.group(1)); nodes = j.get('@graph', [j]) if isinstance(j, dict) else j
            sch += [str(n.get('@type')) for n in nodes]
        except Exception: invalid += 1
    faq_n = len(re.findall(r'class="[^"]*eael-accordion-header', body))
    imgs = []
    for im in re.findall(r'<img\b[^>]*>', clean):
        src = attr(im, 'data-lazy-src') or attr(im, 'src') or ''
        if src.startswith('http') and src not in seen_img: seen_img[src] = None
        imgs.append(src)
    hrefs = {attr(a, 'href') for a in re.findall(r'<a\b[^>]*>', clean)} - {None}
    internal = sorted({h.replace(SITE, '') for h in hrefs if h.startswith('/') or h.startswith(SITE)})
    city_links = [u for u, _ in ALL_CITY_LINKS if u != f'/{key}/']
    missing_city_links = [u for u in city_links if u not in internal]
    vids = sorted(set(re.findall(r'background_video_link&quot;:&quot;([^&]+)&quot;', s)))
    name = c['name']; kurz = c['kurz']
    checks = {
        'status200': code == '200', 'title_ok': title == c['title'], 'desc_ok': meta('description') == c['desc'],
        'index': 'noindex' not in meta('robots'), 'canonical_ok': canon == url, 'h1_once': len(h1) == 1, 'h1_city': bool(h1) and name in h1[0],
        'og_title_ok': meta('og:title', 'property') == c['title'], 'schema_valid': invalid == 0,
        'schema_types': all(t in ' '.join(sch) for t in ['LocalBusiness', 'Service', 'FAQPage', 'WebPage', 'BreadcrumbList']),
        'faq10': faq_n == 10, 'city_links_all': not missing_city_links, 'cta_funnel': '/anfrage-auswahl/' in internal,
        'service_links': '/zutrittssystem/' in internal and '/kamerasysteme/' in internal, 'videos2': len(vids) == 2,
        'no_lueneburg_leftover': body.count('Lüneburger Betriebe') + body.count('Adendorf') + body.count('Lüneburger Altstadt') == 0,
        'tel_link': 'tel:+4958214049040' in s, 'city_mentions_ok': text.count(kurz) >= 15,
    }
    report[key] = {'code': code, 'title': title, 'desc_len': len(meta('description')), 'h1': h1, 'h2_n': len([1 for h, t in hs if h == 'h2']), 'words': words, 'kurz_count': text.count(kurz), 'lueneburg_count': text.count('Lüneburg'), 'schema': sch, 'faq_n': faq_n, 'img_n': len(imgs), 'missing_city_links': missing_city_links, 'videos': [v.split('/')[-1] for v in vids], 'checks': checks, 'size_kb': round(len(s) / 1024)}
    bad = [k for k, v in checks.items() if not v]
    print(f"{key:15} {code} {round(len(s)/1024):>4}kB W={words:>5} {kurz}×{text.count(kurz):>3} Lüneburg×{text.count('Lüneburg'):>2} FAQ={faq_n:>2} schema={len(sch):>2} | {'OK' if not bad else 'FEHLER: ' + ', '.join(bad)}")
    time.sleep(0.5)
print('\n=== Bilder (HEAD, einmal je URL) ===')
bad_img = []
for u in list(seen_img)[:80]:
    rr = subprocess.run(['curl', '-sS', '-I', '--http1.1', '-A', UA, '--max-time', '30', '-o', '/dev/null', '-w', '%{http_code}', u], capture_output=True, text=True)
    seen_img[u] = rr.stdout.strip()
    if seen_img[u] != '200': bad_img.append((seen_img[u], u))
print(f'{len(seen_img)} Bild-URLs geprüft, nicht 200:', bad_img or 'keine')
json.dump(report, open(f'{RAW}/../qa_pages.json', 'w'), ensure_ascii=False, indent=1)
