#!/usr/bin/env python3
"""Erzeugt die Gravity-Forms-Definitionen fuer den Luenburg-Funnel.
Aufruf: build_forms.py <dump-dir> <out-dir> --kombi-page-id N [--kontakt-page-id 42] [--kamera-page-id 4371]
"""
import copy, json, sys
DUMP, OUT = sys.argv[1], sys.argv[2]; a = sys.argv[3:]
def opt(k, d): return a[a.index(k)+1] if k in a else d
KOMBI_PAGE = int(opt('--kombi-page-id', 0)); KONTAKT_PAGE = int(opt('--kontakt-page-id', 42)); KAMERA_PAGE = int(opt('--kamera-page-id', 4371))
assert KOMBI_PAGE, 'kombi page id fehlt'

F2 = json.load(open(f'{DUMP}/gf_form_2.json', encoding='utf-8'))
F4 = json.load(open(f'{DUMP}/gf_form_4.json', encoding='utf-8'))

def field(form, fid):
    f = copy.deepcopy(next(x for x in form['fields'] if x['id'] == fid))
    f.pop('formId', None)
    return f

def base(title):
    b = {k: copy.deepcopy(v) for k, v in F4.items() if k not in ('id', 'fields', 'title', 'nextFieldId', 'confirmations', 'notifications', 'is_active', 'date_created', 'is_trash')}
    b['title'] = title
    b['button'] = copy.deepcopy(F4['button'])
    return b

UTM = [field(F4, i) for i in (13, 14, 15, 16, 17, 18, 19)]
UTM_QS = '&'.join(f'{f["inputName"]}={{{f["label"]}:{f["id"]}}}' for f in UTM)

def notification():
    return {'id': 'luen-admin', 'isActive': True, 'to': 'anfragen@provision-infra.de', 'toType': 'email', 'name': 'Admin Notification',
            'event': 'form_submission', 'from': 'anfragen@provision-infra.de', 'subject': 'New submission from {form_title}',
            'message': '{all_fields}', 'disableAutoformat': False}

# ---------------- Formular A: Funnel-Auswahl
CH = ['Schließsystem', 'Kamerasysteme', 'Beides – Schließ- & Kamerasysteme']
sel = field(F4, 7)
sel.update({'id': 20, 'label': 'Wofür suchst du eine Lösung?', 'description': 'Wähle aus, worum es bei dir geht. Danach stellen wir dir passende Fragen.',
            'choices': [{'text': c, 'value': c, 'isSelected': False, 'price': ''} for c in CH],
            'inputs': [{'id': f'20.{i+1}', 'label': c, 'name': ''} for i, c in enumerate(CH)]})
funnel = base('Funnel Auswahl (Lüneburg / alle Unterseiten)')
funnel['description'] = ''
funnel['button']['text'] = 'Weiter'
funnel['fields'] = UTM + [sel]
funnel['nextFieldId'] = 21
qs = UTM_QS + '&bereich={Wofür suchst du eine Lösung?:20}'
def conf(cid, name, page, value=None, default=False):
    c = {'id': cid, 'name': name, 'isDefault': default, 'type': 'page', 'message': '', 'url': '', 'pageId': page,
         'queryString': qs, 'disableAutoformat': False, 'conditionalLogic': []}
    if value:
        c['conditionalLogic'] = {'actionType': 'show', 'logicType': 'all', 'rules': [{'fieldId': '20', 'operator': 'is', 'value': value}]}
    return c
funnel['confirmations'] = {
    'luen-kamera': conf('luen-kamera', 'Weiter zu Kamerasysteme', KAMERA_PAGE, CH[1]),
    'luen-beides': conf('luen-beides', 'Weiter zu Schließ- & Kamerasysteme', KOMBI_PAGE, CH[2]),
    'luen-schliess': conf('luen-schliess', 'Weiter zu Schließsystem (Standard)', KONTAKT_PAGE, None, True),
}
funnel['notifications'] = {}

# ---------------- Formular B: kombiniertes Anfrageformular
kombi = base('Anfrageformular Schließ- & Kamerasysteme')
geb = field(F4, 8); geb['id'] = 21
geb['inputs'] = [dict(i, id=f'21.{n+1}') for n, i in enumerate(geb.get('inputs', []))]
kombi['fields'] = UTM + [field(F2, 1), field(F2, 20), field(F2, 7), field(F2, 11), field(F2, 8), field(F2, 10), geb, field(F2, 6), field(F2, 5)]
kombi['nextFieldId'] = 22
kombi['confirmations'] = {
    'luen-termin': {'id': 'luen-termin', 'name': 'Default Confirmation', 'isDefault': True, 'type': 'page', 'message': '', 'url': '', 'pageId': 3617,
                    'queryString': 'first_name={Wie lautet dein Vorname?:1}&last_name={Wie lautet dein Nachname?:20}&email={Wie lautet deine E-Mail-Adresse?:6}',
                    'disableAutoformat': False, 'conditionalLogic': []},
    'luen-lq': {'id': 'luen-lq', 'name': 'LQ form', 'isDefault': False, 'type': 'page', 'message': '', 'url': '', 'pageId': 823,
                'queryString': 'first_name={Wie lautet dein Vorname?:1}&last_name={Wie lautet dein Nachname?:20}&email={Wie lautet deine E-Mail-Adresse?:6}',
                'disableAutoformat': False,
                'conditionalLogic': {'actionType': 'show', 'logicType': 'any', 'rules': [
                    {'fieldId': '7', 'operator': 'is', 'value': 'Privat'},
                    {'fieldId': '11', 'operator': 'is', 'value': '1–10'}, {'fieldId': '11', 'operator': 'is', 'value': '11–50'},
                    {'fieldId': '8', 'operator': 'is', 'value': '1–5'}, {'fieldId': '8', 'operator': 'is', 'value': '6–15'},
                    {'fieldId': '8', 'operator': 'is', 'value': 'Noch unsicher'}]}},
}
kombi['notifications'] = {'luen-admin': notification()}

json.dump(funnel, open(f'{OUT}/funnel-auswahl.form.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump(kombi, open(f'{OUT}/anfrage-kombiniert.form.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('OK funnel fields', len(funnel['fields']), '| kombi fields', len(kombi['fields']))
