import json, glob, os
summary = {}
for f in sorted(glob.glob('lh/lh_*.json')):
    name = os.path.basename(f)[3:-5]; j = json.load(open(f)); a = j['audits']; c = j['categories']
    def v(k, key='numericValue'): return a.get(k, {}).get(key)
    s = {'scores': {k: round((c[k]['score'] or 0)*100) for k in c},
         'metrics': {'FCP_s': round((v('first-contentful-paint') or 0)/1000, 2), 'LCP_s': round((v('largest-contentful-paint') or 0)/1000, 2), 'TBT_ms': round(v('total-blocking-time') or 0), 'CLS': round(v('cumulative-layout-shift') or 0, 3), 'SI_s': round((v('speed-index') or 0)/1000, 2), 'TTI_s': round((v('interactive') or 0)/1000, 2), 'TTFB_ms': round(v('server-response-time') or 0), 'bytes_MB': round((v('total-byte-weight') or 0)/1048576, 2), 'requests': len(a.get('network-requests', {}).get('details', {}).get('items', [])), 'DOM_nodes': v('dom-size')},
         'opportunities': [], 'seo_fail': [], 'a11y_fail': [], 'bp_fail': [], 'third_party': []}
    for k, au in a.items():
        d = au.get('details') or {}
        if d.get('type') == 'opportunity' and (d.get('overallSavingsMs') or 0) >= 100:
            s['opportunities'].append((k, round(d.get('overallSavingsMs', 0)), round((d.get('overallSavingsBytes') or 0)/1024)))
    s['opportunities'].sort(key=lambda x: -x[1])
    for cat, key in (('seo', 'seo_fail'), ('accessibility', 'a11y_fail'), ('best-practices', 'bp_fail')):
        for ref in c[cat]['auditRefs']:
            au = a[ref['id']]
            if au.get('score') is not None and au['score'] < 1 and au.get('scoreDisplayMode') in ('binary', 'numeric'):
                s[key].append((ref['id'], au.get('title', '')[:70], len((au.get('details') or {}).get('items', []))))
    for it in (a.get('third-party-summary', {}).get('details') or {}).get('items', [])[:8]:
        e = it.get('entity'); s['third_party'].append((e if isinstance(e, str) else (e or {}).get('text'), round(it.get('transferSize', 0)/1024), round(it.get('blockingTime', 0))))
    lcp = a.get('largest-contentful-paint-element', {}).get('details', {}).get('items', [])
    try: s['lcp_element'] = lcp[0]['items'][0]['node']['snippet'][:160]
    except Exception: s['lcp_element'] = None
    try: s['lcp_phases'] = {x['phase']: round(x['timing']) for x in lcp[1]['items']}
    except Exception: pass
    s['css_count'] = len((a.get('unused-css-rules', {}).get('details') or {}).get('items', [])); s['js_count'] = len((a.get('unused-javascript', {}).get('details') or {}).get('items', []))
    s['render_blocking'] = [(i.get('url', '').split('/')[-1][:50], round(i.get('wastedMs', 0))) for i in (a.get('render-blocking-resources', {}).get('details') or {}).get('items', [])[:6]]
    s['modern_images'] = [(i.get('url', '').split('/')[-1][:45], round(i.get('wastedBytes', 0)/1024)) for i in (a.get('modern-image-formats', {}).get('details') or {}).get('items', [])[:6]]
    summary[name] = s
    print(f"\n##### {name}: scores={s['scores']} | {s['metrics']}")
    print("  LCP-Element:", s['lcp_element'], "| Phasen:", s.get('lcp_phases'))
    print("  Opportunities (ms, kB):", s['opportunities'][:8])
    print("  Render-blocking:", s['render_blocking'])
    print("  Moderne Bildformate (kB Ersparnis):", s['modern_images'])
    print("  3rd-Party (kB, blocking ms):", s['third_party'])
    print("  SEO-Audits fehlgeschlagen:", s['seo_fail']); print("  A11y fehlgeschlagen:", s['a11y_fail'][:10]); print("  Best-Practices fehlgeschlagen:", s['bp_fail'][:8])
json.dump(summary, open('lighthouse_summary.json', 'w'), ensure_ascii=False, indent=1)
