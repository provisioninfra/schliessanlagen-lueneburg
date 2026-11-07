#!/usr/bin/env python3
"""Startseite: Hero-H1 (9dcea29) leicht vergrößern, Zeilenhöhen proportional. Aufruf: patch_h1.py live.json out.json"""
import json, sys
d = json.load(open(sys.argv[1], encoding='utf-8'))
def walk(e):
    yield e
    for c in e.get('elements', []): yield from walk(c)
ix = {e['id']: e for r in d['elements'] for e in walk(r)}
s = ix['9dcea29']['settings']
assert s.get('header_size') == 'h1' and 'Wir installieren' in s.get('title', ''), 'H1-Widget nicht erkannt'
plan = {  # key: (erwartet, neu)
    'typography_font_size': (52, 55),            # Desktop (> 1440 px), Zeilenhöhe bleibt 124 %
    'typography_font_size_laptop': (40, 42),     # 1281–1440 px
    'typography_font_size_tablet_extra': (35, 37),  # 1025–1280 px
    'typography_line_height_tablet_extra': (40, 42),
    'typography_font_size_tablet': (25, 27),     # 768–1024 px (auch Smartphone quer)
    'typography_line_height_tablet': (35, 37),
    'typography_font_size_mobile': (22, 24),     # bis 767 px
    'typography_line_height_mobile': (25, 27),
}
for k, (old, new) in plan.items():
    v = s[k]; assert v.get('unit') == 'px' and v.get('size') == old, f'{k}: Live-Wert {v} statt {old}px – Abbruch'
    s[k] = {**v, 'size': new}
assert s['typography_line_height'] == {'unit': 'custom', 'size': '124%', 'sizes': []}, s['typography_line_height']
json.dump(d, open(sys.argv[2], 'w', encoding='utf-8'), ensure_ascii=False)
print('H1 angepasst:', ', '.join(f'{k.replace("typography_", "")} {o}->{n}' for k, (o, n) in plan.items()))
