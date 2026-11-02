#!/usr/bin/env python3
import re, html, json, os, sys, glob
RAW = sys.argv[1]
def txt(x): return html.unescape(re.sub(r'\s+',' ', re.sub('<[^>]+>',' ',x))).strip()
def attr(tag, name):
    m = re.search(r'(?:^|\s)'+re.escape(name)+r'\s*=\s*("([^"]*)"|\'([^\']*)\')', tag)
    if not m: return ''
    return html.unescape(m.group(2) if m.group(2) is not None else m.group(3))
W = r"[A-Za-zÄÖÜäöüß][A-Za-zÄÖÜäöüß\-]+"
pages = {}
for f in sorted(glob.glob(RAW+'/pages/*.html')):
    slug = os.path.basename(f)[:-5]
    s = open(f, encoding='utf-8', errors='replace').read()
    hf = f[:-5]+'.hdr'
    hdr = open(hf, encoding='utf-8', errors='replace').read() if os.path.exists(hf) else ''
    status = (re.findall(r'^HTTP/\S+\s+(\d{3})', hdr, re.M) or ['?'])[-1]
    head = s.split('</head>',1)[0]
    body = s.split('<body',1)[1] if '<body' in s else s
    clean = re.sub(r'<(script|style|noscript|template|svg)\b[^>]*>[\s\S]*?</\1>', ' ', body)
    clean = re.sub(r'<div id="BorlabsCookieBox"[\s\S]*?</div>\s*</div>\s*</div>', ' ', clean)
    main = re.sub(r'<header\b[\s\S]*?</header>', ' ', clean, count=1)
    main = re.sub(r'<footer\b[\s\S]*?</footer>', ' ', main, count=1)
    metas = re.findall(r'<meta\b[^>]*>', head)
    def meta(name, key='name'):
        for m in metas:
            if attr(m, key).lower() == name: return attr(m, 'content')
        return ''
    links = re.findall(r'<link\b[^>]*>', head)
    def linkrel(rel): return [attr(l,'href') for l in links if rel in attr(l,'rel').lower().split()]
    title = txt((re.search(r'<title[^>]*>([\s\S]*?)</title>', head) or [None,''])[1])
    p = dict(slug=slug, status=status, title=title, title_len=len(title), desc=meta('description'),
             robots=meta('robots'), canonical=(linkrel('canonical') or [''])[0],
             og_title=meta('og:title','property'), og_desc=meta('og:description','property'), og_image=meta('og:image','property'),
             lang=attr((re.search(r'<html\b[^>]*>', s) or [''])[0], 'lang'), viewport=meta('viewport'),
             hreflang=[attr(l,'hreflang') for l in links if attr(l,'hreflang')],
             generator=[attr(m,'content') for m in metas if attr(m,'name')=='generator'],
             gsc_verify=meta('google-site-verification')[:6], html_kb=round(len(s)/1024),
             x_cache=(re.findall(r'^X-Varnish-Cache:\s*(\S+)', hdr, re.M|re.I) or ['-'])[-1],
             x_robots=(re.findall(r'^X-Robots-Tag:\s*(.+)$', hdr, re.M|re.I) or ['-'])[-1].strip())
    p['desc_len'] = len(p['desc'])
    hs = []
    for m in re.finditer(r'<(h[1-6])\b[^>]*>([\s\S]*?)</\1>', clean):
        t = txt(m.group(2))
        if t and (m.group(1), t) not in hs: hs.append((m.group(1), t))
    p['h1'] = [t for h,t in hs if h=='h1']; p['h2'] = [t for h,t in hs if h=='h2']; p['h3_n'] = len([1 for h,t in hs if h=='h3'])
    p['headings'] = hs
    tm = txt(main); words = re.findall(W, tm)
    p['words_main'] = len(words); p['words_all'] = len(re.findall(W, txt(clean))); p['text_main'] = tm
    kws = ['Schließanlage','Schließsystem','elektronisch','digital','Zutritt','Videoüberwachung','Kameraüberwachung','Kamera','Hamburg','Hannover','Lüneburg','Uelzen','Norddeutschland','Niedersachsen','Celle','Bad Bevensen','Winsen','Buchholz','Soltau']
    p['kw'] = {k: len(re.findall(re.escape(k), tm, re.I)) for k in kws}
    imgs = re.findall(r'<img\b[^>]*>', clean); noalt = []; fmts = {}
    for im in imgs:
        src = attr(im,'data-lazy-src') or attr(im,'src') or attr(im,'data-src')
        if not src or src.startswith('data:'): continue
        ext = src.split('?')[0].rsplit('.',1)[-1].lower(); fmts[ext] = fmts.get(ext,0)+1
        if not attr(im,'alt').strip(): noalt.append(src.split('/')[-1][:60])
    p['img_n'] = len(imgs); p['img_noalt'] = sorted(set(noalt)); p['img_fmts'] = fmts
    p['img_lazy'] = len([1 for im in imgs if 'loading="lazy"' in im or 'data-lazy-src' in im])
    p['iframes'] = sorted({re.sub(r'^(https?://[^/]+).*', r'\1', attr(i,'src') or attr(i,'data-src') or attr(i,'data-lazy-src')) for i in re.findall(r'<iframe\b[^>]*>', body)})
    p['videos'] = len(re.findall(r'<video\b', body)); p['forms'] = len(re.findall(r'<form\b', body))
    anchors = re.findall(r'<a\b[^>]*>', clean); hrefs = [attr(a,'href') for a in anchors]
    p['tel'] = sorted({h for h in hrefs if h.startswith('tel:')}); p['mailto'] = sorted({h for h in hrefs if h.startswith('mailto:')})
    internal, external, frag = set(), set(), set()
    for h in hrefs:
        if not h or h.startswith(('tel:','mailto:','javascript:')): continue
        if h.startswith('#'): frag.add(h[1:]); continue
        if h.startswith('/') or 'provision-infra.de' in h: internal.add(h if h.startswith('http') else 'https://provision-infra.de'+h)
        elif h.startswith('http'): external.add(re.sub(r'^(https?://[^/]+).*', r'\1', h))
    p['internal'] = sorted(internal); p['external'] = sorted(external); p['frag'] = sorted(frag)
    ids = set(re.findall(r'\bid="([^"]+)"', body)); p['frag_missing'] = sorted(x for x in frag if x and x not in ids)
    p['nofollow_n'] = len([a for a in anchors if 'nofollow' in attr(a,'rel')])
    p['scripts_ext'] = len(re.findall(r'<script\b[^>]*\bsrc=', s)); p['css_ext'] = len(re.findall(r'<link\b[^>]*rel=["\']stylesheet', s))
    p['inline_css_kb'] = round(sum(len(x) for x in re.findall(r'<style\b[^>]*>([\s\S]*?)</style>', s))/1024)
    sig = {'GTM':r'googletagmanager\.com/gtm\.js|GTM-[A-Z0-9]{5,}','gtag':r'googletagmanager\.com/gtag/js|gtag\(','GA4-ID':r'\bG-[A-Z0-9]{8,}\b','UA-ID':r'\bUA-\d{4,}-\d\b','Matomo':r'matomo|piwik','FB-Pixel':r'connect\.facebook\.net|fbq\(','Hotjar':r'hotjar','LinkedIn':r'snap\.licdn','Clarity':r'clarity\.ms','Borlabs':r'BorlabsCookie','ProvenExpert':r'provenexpert','Calendly':r'calendly','Lottie':r'lottie','YouTube':r'youtube\.com|youtu\.be|youtube-nocookie','GoogleFonts':r'fonts\.googleapis\.com|fonts\.gstatic','GoogleMaps':r'maps\.googleapis|google\.com/maps','WP-Rocket':r'rocket-loader|wp-rocket|data-rocket','Elementor':r'elementor'}
    p['tracking'] = [k for k,v in sig.items() if re.search(v, s)]
    sch = []
    for m in re.finditer(r'<script type="application/ld\+json"[^>]*>([\s\S]*?)</script>', s):
        try:
            j = json.loads(m.group(1)); nodes = j.get('@graph',[j]) if isinstance(j,dict) else j
            for n in nodes:
                sch.append({'type': n.get('@type'), 'name': n.get('name'), 'areaServed': ([a.get('name') if isinstance(a,dict) else a for a in n['areaServed']] if isinstance(n.get('areaServed'),list) else n.get('areaServed')), 'keys': sorted(k for k in n if not k.startswith('@'))})
        except Exception as e: sch.append({'type':'INVALID','err':str(e)[:80]})
    p['schema'] = sch
    pages[slug] = p
json.dump(pages, open(RAW+'/../pages_summary.json','w'), ensure_ascii=False, indent=1)
print(f"\n{'slug':26} {'st':>3} {'cache':5} {'rob':4} {'tit':>3} {'des':>3} {'wMain':>5} {'h1':>2} {'h2':>2} {'img':>3} {'noalt':>5} {'kb':>4}  title")
for k,p in pages.items():
    rob = 'NOI' if 'noindex' in p['robots'] else 'idx'
    print(f"{k:26} {p['status']:>3} {p['x_cache']:5} {rob:4} {p['title_len']:>3} {p['desc_len']:>3} {p['words_main']:>5} {len(p['h1']):>2} {len(p['h2']):>2} {p['img_n']:>3} {len(p['img_noalt']):>5} {p['html_kb']:>4}  {p['title'][:58]}")
idx = {k:p for k,p in pages.items() if 'noindex' not in p['robots'] and p['status']=='200'}
print("\n=== Indexierbare Seiten (Detail) ===")
for k,p in idx.items():
    print(f"\n--- {k} | canonical={p['canonical']} | lang={p['lang']} | x-robots={p['x_robots']} | gen={p['generator']}")
    print(f"TITLE({p['title_len']}): {p['title']}\nDESC({p['desc_len']}): {p['desc']}\nOG: {p['og_title'][:70]} | img={p['og_image'].split('/')[-1][:50]}")
    print("H1:", p['h1']); print("H2:", [h[:60] for h in p['h2']][:14], f"(+{max(0,len(p['h2'])-14)})", "| H3:", p['h3_n'])
    print("KW:", {a:b for a,b in p['kw'].items() if b})
    print(f"IMG: {p['img_n']} lazy={p['img_lazy']} fmts={p['img_fmts']} noalt={p['img_noalt']}")
    print("IFRAMES:", p['iframes'], "| VIDEO:", p['videos'], "| FORMS:", p['forms'], "| TEL:", p['tel'], "| MAIL:", p['mailto'])
    print("TRACKING/3rd:", p['tracking'])
    print("SCHEMA:", [(x['type'], x.get('name'), x.get('areaServed')) for x in p['schema']])
    print("INTERNE LINKS:", [u.replace('https://provision-infra.de','') for u in p['internal']])
    print("EXTERN:", p['external'], "| nofollow:", p['nofollow_n'], "| Anker fehlend:", p['frag_missing'])
    print(f"ASSETS: js={p['scripts_ext']} css={p['css_ext']} inlineCSS={p['inline_css_kb']}kB html={p['html_kb']}kB")
print("\n=== Duplikate ===")
for fld in ('title','desc'):
    seen = {}
    for k,p in idx.items(): seen.setdefault(p[fld], []).append(k)
    for v,ks in seen.items():
        if len(ks) > 1: print(f"DUP {fld}: {ks} -> {v[:70]}")
h1s = {}
for k,p in idx.items():
    for h in p['h1']: h1s.setdefault(h, []).append(k)
for v,ks in h1s.items():
    if len(ks) > 1: print(f"DUP H1: {ks} -> {v[:70]}")
def shingles(t, n=6):
    w = re.findall(W, t.lower()); return {' '.join(w[i:i+n]) for i in range(max(0, len(w)-n+1))}
ks = list(idx)
print("\n=== Textähnlichkeit (Jaccard, 6-Wort-Shingles, ohne Header/Footer) ===")
for i in range(len(ks)):
    for j in range(i+1, len(ks)):
        a, b = shingles(idx[ks[i]]['text_main']), shingles(idx[ks[j]]['text_main'])
        if a and b:
            jac = len(a & b)/len(a | b)
            if jac >= 0.08: print(f"{ks[i]} ~ {ks[j]}: {jac:.0%}")
print("\n=== Sonderfälle ===")
for k in ('Lueneburg','_s_test','gibtesnicht-404-test'):
    if k in pages: print(k, '| status', pages[k]['status'], '| robots', pages[k]['robots'], '| canonical', pages[k]['canonical'], '| title', pages[k]['title'][:50])
allint = set()
for p in idx.values(): allint |= set(p['internal'])
open(RAW+'/../internal_links.txt','w').write('\n'.join(sorted({u.split('#')[0] for u in allint}))+'\n')
print("\nInterne Ziel-URLs (ohne Fragment):", len({u.split('#')[0] for u in allint}))
