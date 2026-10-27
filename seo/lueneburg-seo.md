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
| Landeseiten-Formularvorlagen (Plugin „Landeseiten Form for Gravity Forms“) | 4598 (Formular 5), 4599 (Formular 6) | Kopien der Vorlage „Kontakt test“ (Formular 2): Reveal-Modus, Poppins, Akzent #fbc91b, 800 px; Button der Auswahlseite „Weiter →“ |
| Hauptmenü „Main“ (ID 6), umgebaut am 27.10.2026 | Einträge 413, 414, 4568, 415, 416, 4558 | sichtbar: „Mit digitalen Schlüsseln Kosten sparen“, „So arbeiten wir zusammen“; Aufklappmenü „Mehr“: „Über uns“, „FAQ“, zuletzt „Komm in unser Team“. Der Punkt „Lüneburg“ wurde auf Wunsch am 27.10.2026 wieder entfernt. |
| Menü „Menü Lüneburg“ (Slug `menue-lueneburg`) | 18 | fünf Anker-Links, in Header und Footer der Lüneburg-Seite eingebunden. Der Name beginnt bewusst mit „Me…“: WordPress nutzt bei Nav-Widgets ohne gültiges Menü (Footer-Widgets „karriere-menu“ auf allen Seiten) das alphabetisch erste Menü als Fallback, das muss „Main“ bleiben. |

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
| Meta-Description (158 Zeichen) | `Schließanlagen & Videoüberwachung in Lüneburg: ProVision Infra plant, installiert und betreut dein System vor Ort. Jetzt unverbindliches Erstgespräch sichern.` |
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
| 3 | Region mit Film (`#region`) | Startseite „Video + drei Punkte“ (fadeInLeft/Right, Vimeo-Film mit Vorschaubild, Zeile vertikal zentriert) | H2 Sicherheitstechnik für Lüneburg, Sitz Bad Bevensen, Einsatzgebiet |
| 4 | Schließanlagen (`#schliessanlagen`) | Kamera-Seite „5 Karten“ (sticky Text, fadeInRight) | H2 + 5 Karten (H3): mechanisch, elektronisch, smart, Umrüstung, kombiniert; CTA |
| 5 | Videoüberwachung (`#kamera`) | „So arbeiten wir“ Glass-Cards (fadeInUp, floating) | H2 + 3 Nutzen-Karten |
| 5b | Leistungen (`#leistungen`) | „Stell dir mal vor“ Zwei-Spalten-Liste mit Lottie-Kamera (Desktop + Mobil) | H2 + 8 Leistungen mit Neben-Keywords |
| 5c | Zielgruppen (`#zielgruppen`) | Glass-Cards (Klon) | H2 + 3 Zielgruppen-Karten |
| 6 | Technik (`#technik`) | Produkt-Karussell | TP-Link VIGI Kameras |
| 7 | Kundenstimmen | Testimonial-Karussell | 3 Bewertungen (u. a. „direkt aus Bad Bevensen“) |
| 8 | Ablauf (`#arbeiten`) | Lottie-Timeline (Desktop) / EA-Timeline (Mobil) | 5 Schritte mit Lüneburg-Bezug |
| 9 | Gründer (`#ueber`) | Glass-Container | unverändert |
| 10 | Standort (`#standort`) | Deutschlandkarte + Glass-Card | H2 Lüneburg und Umgebung, Ortsliste, CTA |
| 11 | FAQ (`#FAQ`) | EA Advanced Accordion | 10 Fragen (siehe 5.) |
| 12 | Partner, Footer, ProvenExpert-Badge | unverändert | – |
| 13 | Strukturierte Daten | HTML-Widget | JSON-LD (siehe 4.) |

Überschriften-Hierarchie: 1× H1, 11× H2, H3 nur innerhalb der Karten/Ablauf/FAQ.

## 4. Strukturierte Daten (JSON-LD im letzten Abschnitt)

Eigenes JSON-LD (HTML-Widget am Seitenende):

- `LocalBusiness` + `Locksmith` (Organisation, Adresse Bad Bevensen, Öffnungszeiten, `areaServed` Lüneburg / Landkreis Lüneburg / Uelzen / Hamburg / Niedersachsen)
- 2× `Service` (Schließanlagen, Videoüberwachung) mit `areaServed` Lüneburg

Automatisch von Plugins erzeugt (deshalb **nicht** im eigenen JSON-LD):

- Yoast: `WebSite`, `WebPage`, `ImageObject`, `BreadcrumbList` (Startseite → Lüneburg)
- Essential Addons Advanced Accordion: `FAQPage` mit allen 8 Fragen
- ProvenExpert-Widget: `Product` mit `AggregateRating` (wie auf allen Seiten)

Lerneffekt vom 26.10.2026: Die erste Fassung enthielt zusätzlich eigene `WebPage`-, `BreadcrumbList`- und `FAQPage`-Knoten. Die eigene `BreadcrumbList` hatte dieselbe `@id` wie die von Yoast (`/lueneburg/#breadcrumb`); Google hat beide Listen zu einer verschmolzen und für das Yoast-Element ohne `item` den kritischen Fehler „Feld item fehlt“ gemeldet. Die Kopien wurden entfernt.

## 5. FAQ (Keyword-Abdeckung)

1. Was kostet eine Schließanlage in Lüneburg?
2. Mechanische oder elektronische Schließanlage – was passt zu meinem Betrieb?
3. Kann ich meine bestehende Schließanlage auf elektronisch umrüsten?
4. Wie schnell seid ihr in Lüneburg vor Ort?
5. Darf ich mein Firmengelände in Lüneburg per Kamera überwachen?
6. Kann ich Zutritt und Kameras in einem System verbinden?
7. Welche Hersteller verbaut ProVision Infra?
8. Was passiert nach der Installation?
9. Wie lange dauert der Einbau einer Schließanlage in Lüneburg?
10. Übernehmt ihr auch Wartung und Service für Schließanlagen und Kameras im Raum Lüneburg?

## 6. Funnel

```
/lueneburg/  ──CTA──▶  /anfrage-auswahl/  (Formular 5 „Funnel Auswahl“: Schließsystem | Kamerasysteme | Beides)
                             │ Schließsystem  ──▶ /kontakt/                (Formular 2)
                             │                       ├ HQ: Geschäftlich mit 6–15 / 16–50 / 51+ Türen  ──▶ /termin-gebucht/
                             │                       ├ HQ: Privat mit 16–50 / 51+ Türen               ──▶ /termin-gebucht/
                             │                       └ LQ (alles andere, inkl. „Noch unsicher“)        ──▶ /termin/
                             │ Kamerasysteme  ──▶ /kontakt-kamerasysteme/  (Formular 4)
                             │                       ├ HQ: Geschäftlich ──▶ /termin-gebucht-kamerasysteme/
                             │                       └ LQ: Privat       ──▶ /termin-kamerasysteme/
                             └ Beides         ──▶ /kontakt-kombiniert/    (Formular 6)
                                                     ├ HQ: Geschäftlich ──▶ /termin-gebucht/
                                                     └ LQ: Privat       ──▶ /termin/

HQ/LQ-Regeln gesetzt am 27.10.2026 (Vorgabe: Schließsystem HQ ab 6 Türen geschäftlich bzw. ab 15 Türen privat; da das Feld in Stufen 1–5 / 6–15 / 16–50 / 51+ fragt, gilt privat ab der Stufe 16–50). Vorname/Nachname/E-Mail werden per Query-String an Calendly übergeben.
```

UTM-Parameter (utm_source … fbclid) werden im Funnel-Formular als versteckte Felder übernommen und per Query-String an das Folgeformular weitergereicht; zusätzlich wird `bereich=` mitgegeben.

## 7. Indexierung – Checkliste nach Veröffentlichung

- [x] Seite in WordPress veröffentlichen (Status „Entwurf“ → „Veröffentlicht“), Funnel- und Kombi-Seite ebenfalls
- [x] `https://provision-infra.de/page-sitemap.xml` enthält `/lueneburg/` (geprüft 24.10.2026)
- [x] `https://provision-infra.de/lueneburg/` liefert 200, Canonical auf sich selbst, `robots` = index,follow (geprüft 24.10.2026)
- [ ] Google Search Console → URL-Prüfung → „Indexierung beantragen“ (nur mit Google-Login möglich; nach dem Schema-Fix vom 26.10.2026 zuerst „Live-URL testen“, dann beantragen)
- [ ] Bing: IndexNow wurde am 26.10.2026 versucht, scheitert aber ohne Schlüsseldatei im Webroot (eine Datei in `/wp-content/uploads/` deckt nur diesen Pfad ab, Antwort 422). Optionen: Bing Webmaster Tools → URL einreichen (Login nötig) oder das offizielle Plugin „IndexNow“ von Microsoft Bing installieren, das die Schlüsseldatei im Root bereitstellt und neue Seiten automatisch meldet. Google nimmt an IndexNow nicht teil.
- [x] Rich-Results-Test: Fehler „Feld item fehlt“ (Breadcrumb-Kollision) behoben, siehe Abschnitt 4
- [ ] Interne Verlinkung: Der Menüpunkt „Lüneburg“ wurde auf Wunsch wieder entfernt; die Seite ist aktuell nur über die Sitemap erreichbar. Empfehlung: ein unauffälliger Textlink, z. B. im Footer („Standort Lüneburg“) oder im Standort-Abschnitt der Startseite, damit Google die Seite über die interne Verlinkung findet. Von der Lüneburg-Seite aus bestehen Links zu `/zutrittssystem/` und `/kamerasysteme/`.
- [ ] Google Unternehmensprofil: Leistungsgebiet „Lüneburg“ ergänzen und auf `/lueneburg/` verlinken
- [ ] PageSpeed prüfen (Hero-Video wird auf Mobil durch den separaten Mobil-Block ersetzt, wie auf der Startseite)

## 8. Später erweiterbar

- Weitere Stadt-Seiten nach demselben Muster (`tools/build_lueneburg.py` kopieren, Texte/Orte austauschen); der Funnel ist für alle Unterseiten gedacht.
- Lokale Referenz (Projekt in Lüneburg) als zusätzlicher Abschnitt mit Foto.
