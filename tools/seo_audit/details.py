import re, json, html, glob, os
RAW='raw/pages/'
def attr(tag, name):
    m = re.search(r'(?:^|\s)'+re.escape(name)+r'\s*=\s*("([^"]*)"|\'([^\']*)\')', tag)
    return html.unescape(m.group(2) if m and m.group(2) is not None else (m.group(3) if m else '')) if m else None
pages = {os.path.basename(f)[:-5]: open(f, encoding='utf-8', errors='replace').read() for f in glob.glob(RAW+'*.html')}
home = pages['home']
print("GTM-IDs:", sorted(set(re.findall(r'GTM-[A-Z0-9]{4,}', home))), "| GA4-IDs im HTML:", sorted(set(re.findall(r'\bG-[A-Z0-9]{8,}\b', home))))
print("google-site-verification:", re.findall(r'google-site-verification" content="([^"]{0,8})', home))
print("FB-Pixel auf karriere:", re.findall(r'.{60}(?:connect\.facebook\.net|fbq\().{40}', pages['karriere'])[:2])
print("Maps-/GBP-Links:", sorted({m for p in pages.values() for m in re.findall(r'https?://(?:www\.)?(?:google\.[a-z.]+/maps[^"\' ]{0,60}|g\.page/[^"\' ]+|maps\.app\.goo\.gl/[^"\' ]+)', p)})[:5])
print("Video-Dateien:", sorted({m for p in pages.values() for m in re.findall(r'https://provision-infra\.de/[^"\' ]+\.(?:mp4|webm)', p)}))
print("\n=== Bilder ohne alt-Attribut vs. alt=\"\" (indexierbare Seiten) ===")
for k in ('home','zutrittssystem','kamerasysteme','lueneburg','uelzen','karriere'):
    body = pages[k].split('<body',1)[1]
    body = re.sub(r'<(script|style|noscript|template|svg)\b[^>]*>[\s\S]*?</\1>', ' ', body)
    miss, empty = [], []
    for im in re.findall(r'<img\b[^>]*>', body):
        src = attr(im,'data-lazy-src') or attr(im,'src') or ''
        if not src or src.startswith('data:'): continue
        a = attr(im,'alt')
        name = src.split('/')[-1][:45]
        if a is None: miss.append(name)
        elif not a.strip(): empty.append(name)
    print(f"{k:15} fehlt={sorted(set(miss))} | leer(alt=\"\")={len(set(empty))}")
print("\n=== Schema-Details ===")
for k in ('home','karriere','lueneburg'):
    for m in re.finditer(r'<script type="application/ld\+json"[^>]*>([\s\S]*?)</script>', pages[k]):
        try: j = json.loads(m.group(1))
        except Exception as e: print(k, 'INVALID JSON', e); continue
        nodes = j.get('@graph',[j]) if isinstance(j,dict) else j
        for n in nodes:
            t = n.get('@type')
            if t in ('Product',) or (k=='karriere' and t in ('WebSite','WebPage','BreadcrumbList','JobPosting','Organization')):
                info = {kk: (str(v)[:70] if kk in ('@id','name','title','datePosted','validThrough') else type(v).__name__) for kk,v in n.items() if kk in ('@id','name','title','datePosted','validThrough','aggregateRating','review','offers','hiringOrganization','jobLocation','employmentType','description','baseSalary','url','sameAs','address','telephone','logo')}
                print(f"[{k}] {t}: {info}")
print("\n=== Footer-Links Startseite ===")
foot = re.search(r'<footer\b[\s\S]*?</footer>', home)
if foot: print(sorted({attr(a,'href') for a in re.findall(r'<a\b[^>]*>', foot.group(0)) if attr(a,'href')}))
hdr = re.search(r'<header\b[\s\S]*?</header>', home)
if hdr: print("Header-Links:", sorted({attr(a,'href') for a in re.findall(r'<a\b[^>]*>', hdr.group(0)) if attr(a,'href')}))
print("\n=== Bild-/Video-URLs Startseite (für Größenmessung) ===")
urls = set()
for im in re.findall(r'<img\b[^>]*>', home):
    for key in ('data-lazy-src','src'):
        v = attr(im,key)
        if v and v.startswith('http') and not v.startswith('data:'): urls.add(v)
urls |= set(re.findall(r'url\((?:&quot;|["\']?)(https://provision-infra\.de/wp-content/uploads/[^"\')&]+)', home))
urls |= set(re.findall(r'https://provision-infra\.de/[^"\' ]+\.(?:mp4|webm)', home))
open('home_media_urls.txt','w').write('\n'.join(sorted(urls))+'\n'); print(len(urls), 'Medien-URLs')
