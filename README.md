# schliessanlagen-lueneburg

Unterseite **/lueneburg/** für provision-infra.de: mechanische & elektronische Schließanlagen sowie Video- und Kameraüberwachung in Lüneburg.

Die Seite ist direkt in WordPress/Elementor angelegt (Seite #4496). Dieses Repository enthält die Quelle der Elementor-Daten, die Gravity-Forms-Definitionen des Funnels und das SEO-Konzept, damit alles reproduzierbar bleibt.

## Inhalt

| Pfad | Zweck |
| --- | --- |
| `elementor/lueneburg.elementor.json` | Elementor-Elemente + Seiteneinstellungen + Yoast-Werte der Lüneburg-Seite |
| `elementor/anfrage-auswahl.elementor.json` | Funnel-Auswahlseite (`/anfrage-auswahl/`, Seitentitel „Funnel-Unterseite“) |
| `elementor/kontakt-kombiniert.elementor.json` | Kontaktseite mit kombiniertem Formular (`/kontakt-kombiniert/`) |
| `gravity-forms/funnel-auswahl.form.json` | Formular „Funnel Auswahl“ (Schließsystem / Kamerasysteme / Beides, bedingte Weiterleitungen) |
| `gravity-forms/anfrage-kombiniert.form.json` | Formular „Anfrageformular Schließ- & Kamerasysteme“ |
| `tools/build_lueneburg.py` | Baut die drei Elementor-JSONs aus Dumps der bestehenden Seiten (Kamerasysteme #4313, Startseite #31, Kontakt #4371) |
| `tools/build_forms.py` | Baut die beiden Formular-JSONs aus den bestehenden Formularen 2 und 4 |
| `seo/lueneburg-seo.md` | Keywords, Meta-Daten, Struktur, Schema, Funnel, Indexierungs-Checkliste |

## Design

Design, Farben (Kit: `#000D30`, `#263E96`, `#FBC91B`), Typografie (Poppins/Roboto) und Animationen (fadeInLeft/Right/Up, Glass-Container, Lottie-Timeline, Hero-Video) stammen 1:1 aus den bestehenden Elementor-Abschnitten der Live-Seite; es werden nur Texte, Anker, Links und Schema-Markup ersetzt.

## Nachbauen

```bash
python3 -I tools/build_lueneburg.py <dump-dir> elementor --funnel-form-id 5 --combo-form-id <ID>
python3 -I tools/build_forms.py <dump-dir> gravity-forms --kombi-page-id 4498
```

`<dump-dir>` enthält `elementor_<post-id>.json` (aus `elementor.config.initial_document` im Editor) und `gf_form_<id>.json` (aus `window.form` im Formular-Editor).
