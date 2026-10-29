#!/usr/bin/env python3
"""Kundenstimmen-Karussell: weiteren Slide (Vincent Oswald) als exakte Kopie des 3. Slides anhängen.
Idempotent: ist das Zitat schon vorhanden, bleibt die Seite unverändert. Aufruf: python3 -I patch_testimonial.py live.json out.json"""
import copy, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seo_common import *

QUOTE = '"Super Service und sehr gutes Produkt! Obwohl wir ein vergleichsweise sehr kleiner Kunde sind, wurden wir behandelt wie ein großer. Absolute Empfehlung und gerne wieder!"'
NAME = 'Vincent Oswald​'          # ​ wie bei den bestehenden Namen
ROLE = 'Inhaber / Geschäftsführer Studio Lüüd​'

d = load(sys.argv[1])
sec = [s for s in d['elements'] if 'Kundenstimmen' in json.dumps(s, ensure_ascii=False)]
assert len(sec) == 1, f'Kundenstimmen-Abschnitt nicht eindeutig ({len(sec)})'
cars = [e for e in walk(sec[0]) if e.get('widgetType') == 'nested-carousel']
assert len(cars) == 1, 'Karussell nicht eindeutig'
car = cars[0]
items = car['settings']['carousel_items']
assert len(items) == len(car['elements']), 'carousel_items passt nicht zu den Slides'

def boxes(slide):
    ib = [w for w in walk(slide) if w.get('widgetType') == 'icon-box']
    im = [w for w in walk(slide) if w.get('widgetType') == 'image-box']
    assert len(ib) == 1 and len(im) == 1, f"Slide {slide['id']} hat unerwartete Struktur"
    return ib[0], im[0]

if any(boxes(s)[1]['settings'].get('title_text', '').startswith('Vincent Oswald') for s in car['elements']):
    save(d, sys.argv[2]); print('Slide Vincent Oswald bereits vorhanden, keine Änderung'); sys.exit(0)

# Vorlage: letzter Slide im Standard-Aufbau (Slides 2 und 3 sind bis auf Texte identisch)
tpl = car['elements'][-1]
assert boxes(tpl)[1]['settings'].get('title_text', '').startswith('Mia Manikati'), 'unerwartete Vorlage'
new = clone_new_ids(tpl, d)
ib, im = boxes(new)
ib['settings']['description_text'] = QUOTE
im['settings']['title_text'] = NAME
im['settings']['description_text'] = ROLE
car['elements'].append(new)
it = copy.deepcopy(items[-1]); it['_id'] = new_id(d); items.append(it)
save(d, sys.argv[2])
print(f"Slide ergänzt: Karussell {car['id']} hat jetzt {len(car['elements'])} Slides (neuer Slide {new['id']})")
