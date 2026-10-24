# SEO-Konzept: /lueneburg/ – Schließanlagen & Videoüberwachung Lüneburg

Stand: 24.10.2026 · Seite: https://provision-infra.de/lueneburg/ (WordPress-Seite #4496, Elementor)

Angelegte Objekte in WordPress (alle drei Seiten **veröffentlicht** am 24.10.2026):

| Objekt | ID | Hinweis |
| --- | --- | --- |
| Seite „Schließanlagen & Videoüberwachung Lüneburg“ | 4496 | `/lueneburg/`, index |
| Seite „Funnel-Unterseite“ | 4497 | `/anfrage-auswahl/` (Slug auf Wunsch geändert), noindex, enthält Formular 5 |
| Seite „Kontakt Schließ- & Kamerasysteme“ | 4498 | `/kontakt-kombiniert/`, noindex, enthält Formular 6 |
| Gravity Form „Funnel Auswahl (Lüneburg / alle Unterseiten)“ | 5 | Weiterleitungen: Schließsystem → Seite 42, Kamerasysteme → Seite 4371, Beides → Seite 4498 |
| Gravity Form „Anfrageformular Schließ- & Kamerasysteme“ | 6 | Standard → Seite 3617 (Termin), LQ-Regel → Seite 823, Admin-Benachrichtigung an anfragen@provision-infra.de |
| Menü „Lüneburg“ | 18 | fünf Anker-Links, im Header der Lüneburg-Seite eingebunden |

Zusätzlich wurde in Gravity Forms → Einstellungen → REST API der Zugriff aktiviert (nötig zum Anlegen der Formulare; kann wieder deaktiviert werden).

## 1. Ziel und Keyword-Set

Lokale Landingpage für Lüneburg und den Landkreis Lüneburg mit zwei Leistungsfeldern:

| Cluster | Haupt-Keyword | Neben-Keywords (im Text verwendet) |
| --- | --- | --- |
| Schließanlagen | **Schließanlagen Lüneburg** (Fokus-Keyphrase in Yoast) | mechanische Schließanlage, elektronische Schließanlage, Zutrittskontrolle Lüneburg, Schließzylinder, Schließplan, Transponder, KeyCard, Umrüstung Schließanlage, EVVA, SimonsVoss, NUKI, Keyota, Keyrent |
| Videoüberwachung | **Videoüberwachung Lüneburg** | Kameraüberwachung Lüneburg, Kamerasysteme Lüneburg, Kamera Firmengelände, TP-Link VIGI, Aufzeichnung Rekorder, App |
| Region | Lüneburg, Landkreis Lüneburg | Adendorf, Bardowick, Reppenstedt, Scharnebeck, Bleckede, Winsen (Luhe), Uelzen, Bad Bevensen |

Suchintention: gewerbliche Entscheider (Betriebe, Praxen, Handwerk, Lager) in Lüneburg, die ein Angebot für Schließanlage und/oder Kameras suchen. Ansprache wie auf der restlichen Website in der Du-Form.

## 2. Meta-Daten (Yoast SEO)

| Feld | Wert |
| --- | --- |
| SEO-Titel (59 Zeichen) | `Schließanlagen & Videoüberwachung Lüneburg \| ProVision Infra` |
| Meta-Description (144 Zeichen) | `Mechanische & elektronische Schließanlagen und Videoüberwachung in Lüneburg: ProVision Infra plant, installiert und betreut dein System vor Ort.` |
| Fokus-Keyphrase | `Schließanlagen Lüneburg` |
| Slug / Canonical | `/lueneburg/` → `https://provision-infra.de/lueneburg/` |
| Robots | index, follow (Yoast-Standard, max-image-preview:large) |
| OG/Twitter | Titel + Description wie oben, Bild `provision_header_02-1.png` (1305×980) |

Funnel-Seiten (`/anfrage-auswahl/`, `/kontakt-kombiniert/`) sind wie die bestehenden Kontaktseiten auf **noindex** gesetzt und erscheinen nicht in der Sitemap.

## 3. Seitenstruktur (gekürzt gegenüber der Kamera-Seite: 13 statt 22 Abschnitte)

| # | Abschnitt (Anker) | Herkunft des Designs | Inhalt |
| --- | --- | --- | --- |
| 1 | Header (sticky Glass-Navigation) | Kamera-Seite | Logo, Menü „Lüneburg“ mit Ankern |
| 2 | Hero mit Tür-Video, Google-Bewertung, Counter | Startseite | H1 + Einleitung + CTA |
| 3 | Region (`#region`) | Kamera-Seite „Logo + drei Punkte“ (fadeInLeft/Right) | H2 Sicherheitstechnik für Lüneburg, Sitz Bad Bevensen, Einsatzgebiet |
| 4 | Schließanlagen (`#schliessanlagen`) | Kamera-Seite „5 Karten“ (sticky Text, fadeInRight) | H2 + 5 Karten (H3): mechanisch, elektronisch, smart, Umrüstung, kombiniert; CTA |
| 5 | Videoüberwachung (`#kamera`) | „So arbeiten wir“ Glass-Cards (fadeInUp, floating) | H2 + 3 Nutzen-Karten |
| 6 | Technik (`#technik`) | Produkt-Karussell | TP-Link VIGI Kameras |
| 7 | Kundenstimmen | Testimonial-Karussell | 3 Bewertungen (u. a. „direkt aus Bad Bevensen“) |
| 8 | Ablauf (`#arbeiten`) | Lottie-Timeline (Desktop) / EA-Timeline (Mobil) | 5 Schritte mit Lüneburg-Bezug |
| 9 | Gründer (`#ueber`) | Glass-Container | unverändert |
| 10 | Standort (`#standort`) | Deutschlandkarte + Glass-Card | H2 Lüneburg und Umgebung, Ortsliste, CTA |
| 11 | FAQ (`#FAQ`) | EA Advanced Accordion | 8 Fragen (siehe 5.) |
| 12 | Partner, Footer, ProvenExpert-Badge | unverändert | – |
| 13 | Strukturierte Daten | HTML-Widget | JSON-LD (siehe 4.) |

Überschriften-Hierarchie: 1× H1, 9× H2, H3 nur innerhalb der Karten/Ablauf/FAQ.

## 4. Strukturierte Daten (JSON-LD im letzten Abschnitt)

- `LocalBusiness` + `Locksmith` (Organisation, Adresse Bad Bevensen, Öffnungszeiten, `areaServed` Lüneburg / Landkreis Lüneburg / Uelzen / Hamburg / Niedersachsen)
- `WebPage` + `BreadcrumbList` (Startseite → Lüneburg)
- 2× `Service` (Schließanlagen, Videoüberwachung) mit `areaServed` Lüneburg
- `FAQPage` mit allen 8 Fragen (Textfassung ohne HTML)

Yoast ergänzt automatisch `WebSite`, `WebPage` und `BreadcrumbList`; doppelte Breadcrumbs sind unkritisch, können aber in Yoast → Schema deaktiviert werden.

## 5. FAQ (Keyword-Abdeckung)

1. Was kostet eine Schließanlage in Lüneburg?
2. Mechanische oder elektronische Schließanlage – was passt zu meinem Betrieb?
3. Kann ich meine bestehende Schließanlage auf elektronisch umrüsten?
4. Wie schnell seid ihr in Lüneburg vor Ort?
5. Darf ich mein Firmengelände in Lüneburg per Kamera überwachen?
6. Kann ich Zutritt und Kameras in einem System verbinden?
7. Welche Hersteller verbaut ProVision Infra?
8. Was passiert nach der Installation?

## 6. Funnel

```
/lueneburg/  ──CTA──▶  /anfrage-auswahl/  (Formular „Funnel Auswahl“: Schließsystem | Kamerasysteme | Beides)
                             │ Schließsystem  ──▶ /kontakt/            (Formular 2, bestehend) ──▶ /termin/
                             │ Kamerasysteme  ──▶ /kontakt-kamerasysteme/ (Formular 4, bestehend) ──▶ /termin-kamerasysteme/
                             └ Beides         ──▶ /kontakt-kombiniert/ (neues Formular „Anfrageformular Schließ- & Kamerasysteme“)
                                                     ├ Standard ──▶ /termin/ (Calendly, Vorname/Nachname/E-Mail vorausgefüllt)
                                                     └ LQ-Regel ──▶ /termin-gebucht/ (wie Formular 2)
```

UTM-Parameter (utm_source … fbclid) werden im Funnel-Formular als versteckte Felder übernommen und per Query-String an das Folgeformular weitergereicht; zusätzlich wird `bereich=` mitgegeben.

## 7. Indexierung – Checkliste nach Veröffentlichung

- [x] Seite in WordPress veröffentlichen (Status „Entwurf“ → „Veröffentlicht“), Funnel- und Kombi-Seite ebenfalls
- [ ] `https://provision-infra.de/page-sitemap.xml` enthält `/lueneburg/` (Yoast automatisch, Cache von WP Rocket ggf. leeren)
- [ ] `https://provision-infra.de/lueneburg/` liefert 200, Canonical auf sich selbst, `robots` = index,follow
- [ ] Google Search Console → URL-Prüfung → „Indexierung beantragen“
- [ ] Bing Webmaster Tools → URL einreichen (optional)
- [ ] Rich-Results-Test (https://search.google.com/test/rich-results) für FAQ/LocalBusiness
- [ ] Interne Verlinkung: Link auf `/lueneburg/` aus Footer-Menü oder Startseite („Standorte: Lüneburg“) ergänzen – stärkster Hebel für die Indexierung
- [ ] Google Unternehmensprofil: Leistungsgebiet „Lüneburg“ ergänzen und auf `/lueneburg/` verlinken
- [ ] PageSpeed prüfen (Hero-Video wird auf Mobil durch den separaten Mobil-Block ersetzt, wie auf der Startseite)

## 8. Später erweiterbar

- Weitere Stadt-Seiten nach demselben Muster (`tools/build_lueneburg.py` kopieren, Texte/Orte austauschen); der Funnel ist für alle Unterseiten gedacht.
- Lokale Referenz (Projekt in Lüneburg) als zusätzlicher Abschnitt mit Foto.
