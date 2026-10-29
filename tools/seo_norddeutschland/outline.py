#!/usr/bin/env python3
"""Textbausteine einer Elementor-Seite auflisten: python3 -I outline.py cfg.json [max_text]"""
import json, re, html, sys
d = json.load(open(sys.argv[1], encoding='utf-8')); MAX = int(sys.argv[2]) if len(sys.argv) > 2 else 110
def t(v): return html.unescape(re.sub(r'\s+', ' ', re.sub('<[^>]+>', ' ', str(v)))).strip()
def walk(e, depth, top):
    s = e.get('settings', {}); w = e.get('widgetType')
    hide = ''.join(x[5] for x in ('hide_desktop', 'hide_tablet', 'hide_mobile') if s.get(x))  # d/t/m
    if w:
        txt = ''
        for k in ('title', 'editor', 'text', 'description_text', 'title_text', 'html'):
            if s.get(k): txt = t(s[k]) if k != 'html' else ('[HTML ' + str(len(s[k])) + ' Zeichen] ' + re.sub(r'\s+', ' ', s[k])[:80]); break
        if w == 'eael-adv-accordion': txt = 'FAQ: ' + ' | '.join(i.get('eael_adv_accordion_tab_title', '') for i in s.get('eael_adv_accordion_tab', []))
        if w == 'eael-content-timeline': txt = 'TIMELINE: ' + ' | '.join(i.get('eael_custom_title', '') for i in s.get('eael_coustom_content_posts', []))
        if w == 'button': txt = 'BTN: ' + t(s.get('text', '')) + ' -> ' + (s.get('link') or {}).get('url', '')
        if w in ('image',) and isinstance(s.get('image'), dict): txt = 'IMG: ' + s['image'].get('url', '').split('/')[-1] + f" id={s['image'].get('id')}"
        if txt or w in ('heading', 'text-editor'):
            hs = s.get('header_size', '') if w == 'heading' else ''
            print(f"{'  '*depth}{w}[{e['id']}] {hs} {('hide:'+hide) if hide else ''} :: {txt[:MAX]}")
    for c in e.get('elements', []): walk(c, depth + 1, top)
for e in d['elements']:
    s = e.get('settings', {})
    print(f"\n=== SECTION {e['id']} {s.get('_element_id','')} {s.get('_title','')} {s.get('css_classes','')}")
    for c in e.get('elements', []): walk(c, 1, e['id'])
