# SEO-Audit und Optimierungsbericht: provision-infra.de/lueneburg/

Stand: 26.10.2026 · Zielseite: https://provision-infra.de/lueneburg/ · Bearbeitung über WordPress/Elementor (Seite #4496)

Ziel: bestmögliche Google-Platzierung für lokale Suchanfragen rund um Schließanlagen, Zutrittskontrolle und Videoüberwachung in Lüneburg und im Landkreis Lüneburg.

## 1. Keyword-Strategie

| Priorität | Keyword (Suchintention) | Einsatz auf der Seite |
| --- | --- | --- |
| 1 | Schließanlagen Lüneburg (kommerziell, lokal) | Title, H1, Hero-Text, Yoast-Fokus-Keyphrase, URL `/lueneburg/`, FAQ |
| 1 | Videoüberwachung Lüneburg (kommerziell, lokal) | Title, H1, H2 „Videoüberwachung in Lüneburg“, Hero-Text, FAQ, Schema `Service` |
| 2 | Zutrittskontrolle Lüneburg | H2 „Schließanlagen & Zutrittskontrolle für Lüneburg“, Leistungsübersicht |
| 2 | elektronische / mechanische Schließanlage | H3-Karten, FAQ 2, Leistungsübersicht |
| 2 | Kamerasysteme Lüneburg, Kameraüberwachung | H2, Glass-Cards, Technik-Karussell (TP-Link VIGI) |
| 3 | Schließanlage umrüsten, Schließplan, Transponder, KeyCard, Sicherungskarte | Karten, Leistungsübersicht, FAQ 3 |
| 3 | Hersteller-Kombinationen (EVVA, SimonsVoss, NUKI, Keyota, Keyrent, TP-Link) | Karten 1–5, FAQ 7, Partner-Logos |
| Lokal | Lüneburg, Landkreis Lüneburg, Adendorf, Bardowick, Reppenstedt, Scharnebeck, Bleckede, Winsen (Luhe), Uelzen, Bad Bevensen | Standort-Abschnitt, FAQ 4, Schema `areaServed` |

Abgrenzung zu bestehenden Seiten: `/zutrittssystem/` und `/kamerasysteme/` zielen auf überregionale Produkt-Keywords (Hamburg, Hannover, Niedersachsen). `/lueneburg/` zielt ausschließlich auf die Stadt und den Landkreis, damit keine Kannibalisierung entsteht. Beide Produktseiten werden von der Lüneburg-Seite aus verlinkt.

## 2. Umgesetzte On-Page-Maßnahmen

### Meta-Daten (Yoast)
- Title (59 Zeichen): `Schließanlagen & Videoüberwachung Lüneburg | ProVision Infra`
- Description (158 Zeichen, mit Handlungsaufforderung): `Schließanlagen & Videoüberwachung in Lüneburg: ProVision Infra plant, installiert und betreut dein System vor Ort. Jetzt unverbindliches Erstgespräch sichern.`
- Fokus-Keyphrase `Schließanlagen Lüneburg`, Breadcrumb-Titel `Lüneburg`, Canonical auf sich selbst, `index, follow`, Open-Graph- und Twitter-Daten mit Hero-Bild.

### Inhalt und Struktur
- Eine H1 mit beiden Hauptthemen und Ortsbezug, darunter 11 H2 in logischer Reihenfolge, H3 nur für Karten, Ablauf und FAQ.
- Hero-Text nennt beide Keyphrasen in den ersten 60 Wörtern.
- Neue Abschnitte: Film der Startseite mit regionalem Text, Leistungsübersicht (8 Leistungen mit Neben-Keywords), Zielgruppen (Handwerk/Gewerbe, Praxen/Kanzleien, Hausverwaltungen/Einzelhandel).
- FAQ auf 10 Fragen erweitert (Kosten, mechanisch vs. elektronisch, Umrüstung, Anfahrt, Datenschutz Kamera, Kombination, Hersteller, Betreuung, Einbaudauer, Wartung). Die Fragen entsprechen typischen Long-Tail-Suchanfragen.
- NAP-Block (Name, Adresse, Telefon mit `tel:`-Link, E-Mail, Öffnungszeiten) im Standort-Abschnitt, identisch mit dem Schema und dem Impressum.
- Interne Verlinkung: Karte „Elektronische Schließanlagen“ → `/zutrittssystem/`, Karte „Zutritt und Videoüberwachung aus einer Hand“ → `/kamerasysteme/`, FAQ 7 → beide Seiten; alle CTAs → `/anfrage-auswahl/`.
- Eingehende Links: Hauptmenü (Aufklappmenü „Mehr“ → Lüneburg) auf allen Seiten in Header und Footer, Sitemap.

### Bilder
- Alt-Texte in der Mediathek gesetzt (Logo, Google-Bewertung, Film-Vorschaubild, Deutschlandkarte, Sterne, Partner-Logos). Kamera-Produktbilder hatten bereits beschreibende Alt-Texte. Rein dekorative Linien und Icons bleiben ohne Alt-Text (korrekt für Screenreader).

### Strukturierte Daten
- Eigenes JSON-LD: `LocalBusiness` + `Locksmith` (Adresse, Telefon, Öffnungszeiten, `areaServed` Lüneburg/Landkreis/Uelzen/Hamburg/Niedersachsen, `sameAs` Social-Profile) und zwei `Service`-Knoten (Schließanlagen, Videoüberwachung) mit `areaServed` Lüneburg.
- Von Plugins erzeugt: Yoast `WebPage`/`BreadcrumbList`/`WebSite`, Essential Addons `FAQPage` (alle 10 Fragen), ProvenExpert `Product`/`AggregateRating`.
- Fehler „Feld item fehlt“ (Breadcrumb-Kollision) ist behoben.

## 3. Technik

| Prüfpunkt | Status |
| --- | --- |
| HTTP 200, HTTPS, Canonical | ok |
| robots `index, follow`, in Yoast-Sitemap | ok |
| Mobile: eigener Mobil-Hero-Block, keine horizontale Scrollbar | ok (Screenshots in `seo/screenshots/`) |
| Lazy Loading | Vimeo-Film lazy (Vorschaubild + Play), Bilder über WordPress-Lazy-Loading |
| Cookie-Consent | Vimeo wird erst nach Einwilligung geladen (Borlabs), kein Einfluss auf Crawling |
| Seitengewicht | wie Startseite und Kamera-Seite (Elementor, Lottie, Hintergrundvideo); Verbesserungen wären site-weit (WP Rocket: Delay JS, Bildformate WebP/AVIF über Imagify) |

## 4. Noch offen (nur mit Zugängen des Betreibers möglich)

1. **Google Search Console**: URL-Prüfung → „Live-URL testen“ → „Indexierung beantragen“. Danach Leistungsbericht nach „Lüneburg“ filtern.
2. **Google Unternehmensprofil**: Leistungsgebiet „Lüneburg“ und Landkreis ergänzen, Leistungen „Schließanlagen“, „Zutrittskontrolle“, „Videoüberwachung“ anlegen, Website-Link auf `/lueneburg/` setzen, regelmäßig Beiträge mit Lüneburg-Bezug, Kundenbewertungen aktiv um Ortsnennung bitten.
3. **Lokale Zitationen (NAP-Konsistenz)**: identische Firmendaten bei IHK Lüneburg-Wolfsburg, Gelbe Seiten, 11880, Das Örtliche, Cylex, Yelp, Bing Places, Apple Business Connect. Jeweils mit Link auf die Website.
4. **Backlinks mit Lüneburg-Bezug**: Handwerkerverzeichnisse, Partner (EVVA Certified Partner-Verzeichnis, SimonsVoss-Partnersuche), Kunden-Referenzen mit Verlinkung, lokale Presse (LZ Online), Sponsoring lokaler Vereine.
5. **Bing**: IndexNow-Plugin installieren oder URL in Bing Webmaster Tools einreichen.
6. **Content-Ausbau (quartalsweise)**: Referenzprojekt in Lüneburg mit Fotos, Ratgeber „Schließanlage planen: Schließplan erklärt“, Preis-Orientierung, Blog-Artikel zu DSGVO-konformer Videoüberwachung in Niedersachsen; jeweils intern auf `/lueneburg/` verlinken.
7. **Weitere Stadtseiten** (Uelzen, Winsen, Buchholz, Celle) nach demselben Muster, ohne Textduplikate.

## 5. Erfolgsmessung

- Search Console: Impressionen/Klicks für Suchanfragen mit „Lüneburg“, Position der Seite für die Haupt-Keywords (Ziel: Top 10 innerhalb von 3 Monaten, Top 3 innerhalb von 6–9 Monaten, abhängig vom Wettbewerb).
- Google Unternehmensprofil: Aufrufe, Anrufe, Routenanfragen.
- Website: Formular-Starts auf `/anfrage-auswahl/` und Abschlussquote je Formular (Gravity-Forms-Einträge, GTM-Ereignisse auf den Termin-Seiten).

Die gemessenen Ist-Werte nach Veröffentlichung stehen in Abschnitt 6.

## 6. Messwerte nach Veröffentlichung

Wird nach dem Speichern der finalen Fassung ergänzt (Audit-Skript: Titel-/Description-Länge, H1, Wortzahl, Keyword-Vorkommen, Alt-Abdeckung, interne Links, Schema-Typen).
