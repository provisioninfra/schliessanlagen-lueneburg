#!/usr/bin/env python3
"""Städteseiten: Querverlinkung im Regionstext. Aufruf: STADT=lueneburg|uelzen python3 -I patch_stadt.py live.json out.json
(-I ignoriert nur PYTHON*-Variablen, STADT wird normal gelesen)"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seo_common import *

stadt = os.environ['STADT']
d = load(sys.argv[1])
el = get(d, '5c65e03')
marker = '<p><strong>ProVision Infra GmbH</strong>'
if stadt == 'lueneburg':
    extra = ('<p>Auch in <a href="/uelzen/">Uelzen</a> und im gesamten Raum zwischen Hamburg und Hannover sind wir für dich im Einsatz. '
             'Mehr zu <a href="/">digitalen Schließanlagen</a> findest du auf unserer Startseite.</p>')
else:
    extra = ('<p>Auch in <a href="/lueneburg/">Lüneburg</a> und im gesamten Raum zwischen Hamburg und Hannover sind wir für dich im Einsatz. '
             'Mehr zu <a href="/">digitalen Schließanlagen</a> findest du auf unserer Startseite.</p>')
assert 'Mehr zu <a href="/">digitalen Schließanlagen</a>' not in el['settings']['editor'], 'bereits ergänzt'
replace_exact(el, 'editor', marker, extra + marker)
save(d, sys.argv[2])
print(f'{stadt}: Querverlinkung ergänzt')
