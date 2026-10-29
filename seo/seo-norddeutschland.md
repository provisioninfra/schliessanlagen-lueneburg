# SEO-Optimierung Norddeutschland (Hamburg bis Hannover)

Stand: 29.10.2026 · Ziel: Gefunden werden von Unternehmen zwischen Hamburg und Hannover für Schließanlagen, Schließsysteme, elektronische und digitale Schließanlagen sowie Kamera- und Videoüberwachung. Die Karriere-Seite ist auf Wunsch ausgenommen.

## 1. Ausgangslage (Audit vom 29.10.2026)

| Seite | Befund vor der Optimierung |
| --- | --- |
| Startseite `/` | Beschreibung 191 Zeichen (wird abgeschnitten), ohne Region; „Schließanlage“ nur 3×, „elektronisch/digital + Schließanlage“ 0×; kein Unternehmens-Schema; FAQ ohne Schema-Ausgabe |
| `/zutrittssystem/` | Titel „Zutrittssystem - ProVision“, keine Beschreibung, 568 Wörter, keines der Ziel-Keywords, keine Region, keine Querverlinkung, kein Schema |
| `/kamerasysteme/` | gut ausgebaut (11 FAQ, Regions-H2), aber Titel ohne „Kamera“, Beschreibung ohne Hannover, keine Links zu den Schließanlagen-Seiten |
| `/lueneburg/`, `/uelzen/` | gut optimiert, aber nicht untereinander verlinkt |
| `/opt-2/`, `/elementor-3524/` | Test-Seiten mit 23–44 Wörtern, indexiert und in der Sitemap (Qualitätssignal der Domain) |

## 2. Keyword-Zuordnung (keine Kannibalisierung)

| Seite | Schwerpunkt | Fokus-Keyphrase |
| --- | --- | --- |
| `/` | Schließanlagen allgemein, digitale Schließanlagen, digitale/elektronische Schließsysteme, Norddeutschland | digitale Schließanlage |
| `/zutrittssystem/` | elektronische Schließanlage, Zutrittssystem, Betreuung/Wartung/Service | elektronische Schließanlage |
| `/kamerasysteme/` | Kamera- und Videoüberwachung für Unternehmen | Videoüberwachung für Unternehmen |
| `/lueneburg/`, `/uelzen/` | alle Themen + Stadt/Landkreis | Schließanlagen Lüneburg / Uelzen |

Einsatzgebiet in Texten und Schema: Hamburg, Lüneburg, Winsen (Luhe), Buchholz in der Nordheide, Uelzen, Bad Bevensen, Soltau, Celle, Hannover, Niedersachsen.

## 3. Umgesetzte Änderungen

### Startseite (Post 31)
- Titel bleibt wie am 28.10. festgelegt: „Schließanlagen & digitale Zutrittssysteme | ProVision Infra“.
- Beschreibung (157 Zeichen): „Digitale Schließanlagen & elektronische Schließsysteme für Unternehmen zwischen Hamburg und Hannover. ProVision Infra plant, installiert und betreut vor Ort.“
- Hero-Text: „… plant & installiert in Norddeutschland dein digitales Zutrittssystem …“.
- Leistungstext: „digitale Schließanlage“ und „elektronische Schließzylinder“ statt „Zutrittssystem“/„Schließzylinder“.
- „Mit digitalen Schließsystemen von ProVision Infra zusätzliche Kosten verhindern“ semantisch als H2 (Optik unverändert, feste Typografie).
- Regionsabschnitt: Überschrift „Digitale Schließanlagen zwischen Hamburg und Hannover“ (H2, vorher „Hier findest du ProVision Infra“ als div), Text mit Einsatzorten und Links zu `/kamerasysteme/` und `/zutrittssystem/`.
- FAQ: Überschrift „… zu digitalen Schließanlagen …“, Fragen als H3, FAQ-Schema eingeschaltet, zwei neue Fragen (Unterschied mechanisch/elektronisch/digital; Einsatzregion).
- JSON-LD: LocalBusiness/Locksmith (Adresse, Geo, Öffnungszeiten, Einsatzgebiet, Fachgebiete) und Service „Digitale und elektronische Schließanlagen für Unternehmen“.

### Zutrittssystem (Post 3316)
- Titel (62): „Elektronische Schließanlage & Zutrittssystem | ProVision Infra“; Beschreibung (156): „Elektronische Schließanlage mit Rundum-Service: ProVision Infra plant, installiert und betreut dein Zutrittssystem für Unternehmen von Hamburg bis Hannover.“; Breadcrumb „Elektronische Schließanlage“.
- H1: „Wir betreuen deine elektronische Schließanlage und das Thema ist für dich dauerhaft abgeschlossen!“ (gleiche Länge wie vorher).
- Neu vor dem Footer, im Design der Startseite: Regionsabschnitt „Elektronische Schließanlagen zwischen Hamburg und Hannover“ (Karte, Text mit Einsatzorten, Links zur Startseite und zu `/kamerasysteme/`) und FAQ mit 6 Fragen (Betreuung, Transponder verloren, Selbstverwaltung, Hersteller, kleine Unternehmen, Region), FAQ-Schema aktiv.
- JSON-LD: LocalBusiness/Locksmith und Service „Elektronische Schließanlage mit Rundum-Service“.

### Kamerasysteme (Post 4313)
- Titel (60): „Kamera- & Videoüberwachung für Unternehmen | ProVision Infra“; Beschreibung (155): „Kamera- & Videoüberwachung für Unternehmen zwischen Hamburg und Hannover: DSGVO-konform geplant, mit Alarm aufs Handy. ProVision Infra installiert vor Ort.“ (auch Open Graph/Twitter).
- Regionstext mit Einsatzorten und Links zu `/` (digitale Schließanlagen) und `/zutrittssystem/`.
- Schema: Einsatzgebiet auf die Achse Hamburg–Hannover erweitert, Service-Beschreibung angepasst.

### Lüneburg (4496) und Uelzen (4605)
- Regionstext: gegenseitige Verlinkung der Städteseiten und Link zur Startseite („digitale Schließanlagen“).

### Technik / seitenübergreifend
- `/opt-2/` und `/elementor-3524/` auf noindex (Seiten bleiben erreichbar, fallen aus der Sitemap).
- WordPress-Website-Titel „ProVision“ → „ProVision Infra“ (Marke in Open Graph, Schema „WebSite“ und Standardtiteln), Untertitel mit Keywords und Region.
- Alt-Texte (Mediathek, wirken auf allen Seiten): SimonsVoss-Beschlag mit Digitalzylinder (1220), elektronischer Türbeschlag (3364), Support-Ansprechpartner (3649), Logos (309, 3317, 3351), Google-Bewertung (3319). Rein dekorative Linien, Verläufe und Icons bleiben bewusst ohne Alt-Text.
- Nebenbei behoben: Der bisherige WordPress-Untertitel war doppelt kodiert („&amp;amp;“) und erschien so im Schema „WebSite“.

Werkzeuge: `tools/seo_norddeutschland/` (Patches arbeiten immer auf dem frisch geladenen Live-Stand und brechen ab, wenn ein Text zwischenzeitlich geändert wurde).

## 4. Messwerte nach der Umsetzung (29.10.2026, Live-HTML ohne Cache)

| Seite | Titel | Beschreibung | Robots | H1 | Strukturierte Daten |
| --- | --- | --- | --- | --- | --- |
| `/` | 59 | 157 | index | 1 | LocalBusiness+Locksmith, Service, FAQPage (10 Fragen), Yoast, ProvenExpert |
| `/zutrittssystem/` | 62 | 156 | index | 1 | LocalBusiness+Locksmith, Service, FAQPage (6 Fragen), Yoast, ProvenExpert |
| `/kamerasysteme/` | 60 | 155 | index | 1 | LocalBusiness, Service, FAQPage (11 Fragen), Yoast, ProvenExpert |
| `/lueneburg/` | 60 | 158 | index | 1 | LocalBusiness+Locksmith, 2× Service, FAQPage, Yoast, ProvenExpert |
| `/uelzen/` | 58 | 153 | index | 1 | LocalBusiness+Locksmith, 2× Service, FAQPage, Yoast, ProvenExpert |
| `/opt-2/`, `/elementor-3524/` | – | – | noindex | – | nicht mehr in der Sitemap |

Sitemap danach: `/`, `/karriere/`, `/zutrittssystem/`, `/kamerasysteme/`, `/lueneburg/`, `/uelzen/`. Markenname in Open Graph und Schema „WebSite“: „ProVision Infra“.

Keyword-Vorkommen vorher → nachher (sichtbarer Text):

| Seite | „Schließanlage“ | „elektronische Schließanlage“ | „digitale Schließanlage“ | „Hamburg“ | „Hannover“ | Wörter |
| --- | --- | --- | --- | --- | --- | --- |
| `/` | 3 → 14 | 0 → 2 | 0 → 4 | 2 → 6 | 1 → 5 | 2.202 → 2.376 |
| `/zutrittssystem/` | 0 → 13 | 0 → 7 | 0 → 1 | 0 → 5 | 0 → 5 | 568 → 913 |

Hinweis zur Prüfung: In dieser Arbeitsumgebung brechen einzelne Abrufe sporadisch ab (leere Antwort, HTTP/2-Fehler). Screenshots und Funktionsprüfungen werden deshalb nur gewertet, wenn alle CSS- und JS-Dateien der Website vollständig geladen wurden.

## 5. Empfehlungen (nicht automatisch umsetzbar)

1. **Weitere Städteseiten** nach dem Muster Lüneburg/Uelzen für Hamburg, Hannover, Celle, Winsen/Buchholz und Soltau. Ohne lokale Landingpage rankt eine Firma aus Bad Bevensen für „Schließanlage Hamburg“ kaum organisch. Jede Seite braucht eigene Texte (keine Kopien mit ausgetauschtem Ortsnamen).
2. **Google-Unternehmensprofil**: Einzugsgebiet auf die Achse Hamburg–Hannover setzen (bis zu 20 Orte), Dienste „Schließanlagen“, „Elektronische Schließanlage“, „Zutrittskontrolle“, „Videoüberwachung“ anlegen, regelmäßig Beiträge und Fotos von Projekten, Kunden um Bewertungen mit Ortsnennung bitten.
3. **Search Console**: Für `/`, `/zutrittssystem/` und `/kamerasysteme/` „Live-URL testen“ und „Indexierung beantragen“; nach 4–6 Wochen Leistungsbericht nach Suchanfragen mit Ortsnamen filtern.
4. **Verzeichnisse und Backlinks**: einheitliche Firmendaten (Name, Adresse, Telefon) bei IHK, Gelbe Seiten, Das Örtliche, 11880, Bing Places, Apple Business Connect; Partnerverzeichnisse von EVVA und SimonsVoss; Referenzen bei Kunden.
5. **Interne Links zu Städteseiten**: Der Menüpunkt Lüneburg wurde auf Wunsch entfernt. Ein dezenter Textlink (z. B. im Footer „Standorte: Lüneburg, Uelzen“) würde beiden Seiten helfen; das ist eine Geschmacksentscheidung und wurde deshalb nicht umgesetzt.

## 6. Kundenstimme Vincent Oswald (29.10.2026)

Auf allen Seiten mit Kundenstimmen-Karussell (Startseite, Kamerasysteme, Lüneburg, Uelzen; die Zutrittssystem- und Karriere-Seite haben keins) ist ein vierter Slide ergänzt:

> "Super Service und sehr gutes Produkt! Obwohl wir ein vergleichsweise sehr kleiner Kunde sind, wurden wir behandelt wie ein großer. Absolute Empfehlung und gerne wieder!"
> **Vincent Oswald**, Inhaber / Geschäftsführer Studio Lüüd

Umsetzung: exakte Kopie des dritten Slides (identisch zum zweiten), nur Zitat, Name und Funktion ausgetauscht; alle Design-, Abstands- und Animationswerte unverändert (`tools/seo_norddeutschland/patch_testimonial.py`).

Ablauf je Seite (`testimonial_run.js`): Vorschau als Autosave speichern, Funktionsprüfung in der Vorschau, erst danach veröffentlichen; anschließend Cache geleert und Live-Prüfung (`carousel_check.js`). Geprüft jeweils auf Desktop (1440 px) und Handy (390 px):

- 4 Slides und 4 Navigationspunkte,
- Formatierung des neuen Slides identisch mit dem bestehenden (Schriftart, -größe, -farbe, Zeilenhöhe, Karte, Sternegrafik, Anführungszeichen-Grafik),
- Weiter-Pfeil durchläuft alle vier Kundenstimmen,
- Hervorhebung (gelber Rahmen, volle Deckkraft) greift auch beim neuen Slide.

Ergebnis: Vorschau und Live-Prüfung auf allen vier Seiten bestanden. Screenshots: `seo/screenshots/kundenstimmen-vincent-*.png`.
