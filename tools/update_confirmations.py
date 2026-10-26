#!/usr/bin/env python3
"""Setzt die HQ/LQ-Weiterleitungen (Bestätigungen) der Gravity Forms 2, 4 und 6.

Eingabe: aktuelle Formulare als JSON (GET /gf/v2/forms/{id}), Ausgabe: gleiche Objekte mit
geänderten 'confirmations' (alles andere bleibt unverändert, damit PUT /gf/v2/forms/{id} verlustfrei ist).

Regeln (Vorgabe vom 26.10.2026):
  Kamera (Formular 4):        HQ Geschäftlich            -> /termin-gebucht-kamerasysteme/ (4392)
                              LQ Privat                  -> /termin-kamerasysteme/ (4391)
  Schließsystem (Formular 2): HQ Geschäftlich ab 6 Türen oder Privat ab 16 Türen -> /termin-gebucht/ (823)
                              LQ alles andere            -> /termin/ (3617)
  Kombiniert (Formular 6):    HQ Geschäftlich            -> /termin-gebucht/ (823)
                              LQ Privat                  -> /termin/ (3617)
Aufruf: update_confirmations.py <in-dir> <out-dir>
"""
import copy, json, sys
IN, OUT = sys.argv[1], sys.argv[2]
PAGES = {'termin': 3617, 'termin-gebucht': 823, 'termin-kamerasysteme': 4391, 'termin-gebucht-kamerasysteme': 4392}

def choices(form, fid):
    f = next(x for x in form['fields'] if int(x['id']) == fid)
    return [c['value'] for c in f['choices']]

def rule(fid, op, value): return {'fieldId': str(fid), 'operator': op, 'value': value}

def conf(cid, name, page, qs, rules=None, default=False):
    c = {'id': cid, 'name': name, 'isDefault': default, 'type': 'page', 'message': '', 'url': '', 'pageId': page,
         'queryString': qs, 'disableAutoformat': False, 'event': 'form_submission', 'conditionalLogic': []}
    if rules: c['conditionalLogic'] = {'actionType': 'show', 'logicType': 'all', 'rules': rules}
    return c

def default_qs(form):
    d = next((c for c in form['confirmations'].values() if c.get('isDefault')), None)
    return d.get('queryString', '') if d else ''

def ids(form):
    """Bestehende IDs wiederverwenden (Default-ID bleibt Default)."""
    d = next(k for k, c in form['confirmations'].items() if c.get('isDefault'))
    others = [k for k in form['confirmations'] if k != d]
    return d, others

out = {}
# ---- Formular 2: Schließsystem
f2 = json.load(open(f'{IN}/gf_rest_form_2.json', encoding='utf-8'))
ch7, ch8 = choices(f2, 7), choices(f2, 8)
privat, gesch = [c for c in ch7 if c.lower().startswith('privat')][0], [c for c in ch7 if c.lower().startswith('gesch')][0]
small, mid, unsure = [c for c in ch8 if c.startswith('1')][0], [c for c in ch8 if c.startswith('6')][0], [c for c in ch8 if c.lower().startswith('noch')][0]
qs = default_qs(f2); d, others = ids(f2)
f2 = copy.deepcopy(f2)
f2['confirmations'] = {
    'hq-geschaeftlich': conf('hq-geschaeftlich', 'HQ Lead geschäftlich (ab 6 Türen) → Termin gebucht', PAGES['termin-gebucht'], qs,
                             [rule(7, 'is', gesch), rule(8, 'isnot', small), rule(8, 'isnot', unsure)]),
    'hq-privat': conf('hq-privat', 'HQ Lead privat (ab 16 Türen) → Termin gebucht', PAGES['termin-gebucht'], qs,
                      [rule(7, 'is', privat), rule(8, 'isnot', small), rule(8, 'isnot', mid), rule(8, 'isnot', unsure)]),
    d: conf(d, 'LQ Lead (Standard) → Termin', PAGES['termin'], qs, None, True),
}
out[2] = f2
# ---- Formular 4: Kamera
f4 = json.load(open(f'{IN}/gf_rest_form_4.json', encoding='utf-8'))
ch7 = choices(f4, 7); gesch = [c for c in ch7 if c.lower().startswith('gesch')][0]
qs = default_qs(f4); d, others = ids(f4)
f4 = copy.deepcopy(f4)
f4['confirmations'] = {
    'hq-geschaeftlich': conf('hq-geschaeftlich', 'HQ Lead geschäftlich → Termin gebucht Kamerasysteme', PAGES['termin-gebucht-kamerasysteme'], qs, [rule(7, 'is', gesch)]),
    d: conf(d, 'LQ Lead privat (Standard) → Termin Kamerasysteme', PAGES['termin-kamerasysteme'], qs, None, True),
}
out[4] = f4
# ---- Formular 6: Kombiniert
f6 = json.load(open(f'{IN}/gf_rest_form_6.json', encoding='utf-8'))
ch7 = choices(f6, 7); gesch = [c for c in ch7 if c.lower().startswith('gesch')][0]
qs = default_qs(f6); d, others = ids(f6)
f6 = copy.deepcopy(f6)
f6['confirmations'] = {
    'hq-geschaeftlich': conf('hq-geschaeftlich', 'HQ Lead geschäftlich → Termin gebucht', PAGES['termin-gebucht'], qs, [rule(7, 'is', gesch)]),
    d: conf(d, 'LQ Lead privat (Standard) → Termin', PAGES['termin'], qs, None, True),
}
out[6] = f6
for fid, form in out.items():
    json.dump(form, open(f'{OUT}/gf_form_{fid}.updated.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(fid, form['title'], '->', [(c['name'], c['pageId'], c.get('conditionalLogic') and [(r['fieldId'], r['operator'], r['value']) for r in c['conditionalLogic']['rules']]) for c in form['confirmations'].values()])
