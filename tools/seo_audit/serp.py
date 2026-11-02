import subprocess, re, html, urllib.parse, time, json, sys
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
Q = ["Schließanlagen Lüneburg", "Schließanlage Uelzen", "elektronische Schließanlage Hamburg", "digitale Schließanlage Hannover",
     "Videoüberwachung Unternehmen Lüneburg", "Schließanlagen für Unternehmen Niedersachsen", "ProVision Infra", "site:provision-infra.de"]
out = {}
def fetch(url, name):
    r = subprocess.run(["curl", "-sS", "-L", "--compressed", "--max-time", "40", "-A", UA, "-H", "Accept-Language: de-DE,de;q=0.9", url], capture_output=True)
    open(f"raw/serp/{name}.html", "wb").write(r.stdout); return r.stdout.decode("utf-8", "replace")
for i, q in enumerate(Q):
    qe = urllib.parse.quote_plus(q)
    res = {"ddg": [], "bing": []}
    s = fetch(f"https://html.duckduckgo.com/html/?q={qe}&kl=de-de", f"ddg_{i}")
    for m in re.finditer(r'<a rel="nofollow" class="result__a" href="([^"]+)"[^>]*>([\s\S]*?)</a>', s):
        href = html.unescape(m.group(1)); u = urllib.parse.parse_qs(urllib.parse.urlparse(href).query).get("uddg", [href])[0]
        res["ddg"].append((re.sub(r'^https?://(www\.)?', '', u).split('/')[0], html.unescape(re.sub('<[^>]+>', '', m.group(2))).strip()[:60]))
    time.sleep(2)
    s = fetch(f"https://www.bing.com/search?q={qe}&cc=DE&setlang=de-DE&mkt=de-DE", f"bing_{i}")
    for m in re.finditer(r'<li class="b_algo"[\s\S]*?<h2><a href="([^"]+)"[^>]*>([\s\S]*?)</a></h2>', s):
        u = html.unescape(m.group(1)); res["bing"].append((re.sub(r'^https?://(www\.)?', '', u).split('/')[0], html.unescape(re.sub('<[^>]+>', '', m.group(2))).strip()[:60]))
    out[q] = res
    print(f"\n### {q}")
    for eng in ("ddg", "bing"):
        lst = res[eng][:10]
        pv = [n+1 for n, (d, t) in enumerate(res[eng]) if "provision-infra" in d]
        print(f"  {eng.upper():4} ({len(res[eng])} Treffer, provision-infra Position: {pv or '-'}): " + " | ".join(f"{n+1}.{d}" for n, (d, t) in enumerate(lst)))
    time.sleep(2)
json.dump(out, open("serp_results.json", "w"), ensure_ascii=False, indent=1)
