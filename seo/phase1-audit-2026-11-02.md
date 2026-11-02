# SEO Phase 1 – Audit provision-infra.de (Stand 02.11.2026)

Nur-Lese-Audit der Live-Website. Es wurde **nichts an der Website verändert**. Alle Zahlen stammen aus eigenen Messungen (Crawl, HTTP-Header, Lighthouse 12.8.2) oder aus öffentlich abrufbaren Suchergebnissen. Suchvolumina und Google-Rankings liegen ohne Search-Console-Zugang nicht vor und werden nicht geschätzt.

## 1. Zusammenfassung

Die Seite ist technisch sauber indexierbar (robots, Sitemap, Canonicals, Meta-Daten, Schema), aber in drei Punkten deutlich unter ihren Möglichkeiten:

1. **Ladezeit / Core Web Vitals**: Die Startseite lädt 38 MB (zwei Hintergrundvideos mit 14,7 MB und 13,2 MB, beide auch auf Mobilgeräten, dazu 8 Lottie-Animationen à 0,9 MB). Lighthouse-Performance 25–50 von 100, LCP bis 13 s, Blockierzeit bis 14 s mobil.
2. **Tracking & Consent**: Facebook-Pixel, Google-Ads-Tag und das Entwickler-Tool BugHerd laden ohne Einwilligung (Cookies `fr`, `test_cookie`, `_bugherd_session5`), BugHerd wirft dabei Konsolenfehler. Das ist ein Datenschutz- und ein Performance-Thema.
3. **Sichtbarkeit in der Region**: Für keine der geprüften Suchanfragen (Lüneburg, Uelzen, Hamburg, Hannover, Niedersachsen) ist provision-infra.de in den Top 10 der DuckDuckGo-Ergebnisse (Region DE); nur für „Schließanlage Bad Bevensen“ (Platz 6). Die Stadtseiten Lüneburg und Uelzen sind intern nur untereinander verlinkt, Hamburg und Hannover haben keine eigene Seite.

## 2. Seiteninventar (23 veröffentlichte Seiten)

| URL | ID | Funktion | Index | Titel (Zeichen) | Wörter | CTA / Ziel |
| --- | --- | --- | --- | --- | --- | --- |
| / | 31 | Startseite: digitale Schließsysteme, Ablauf, Gründer, FAQ | index | 59 | 2407 | /kontakt |
| /zutrittssystem/ | 3316 | Leistungsseite elektronische Schließanlage, 3 Pakete, FAQ | index | 62 | 913 | /kontakt |
| /kamerasysteme/ | 4313 | Leistungsseite Kamera- & Videoüberwachung, FAQ | index | 60 | 1890 | /kontakt-kamerasysteme/ |
| /lueneburg/ | 4496 | Stadtseite Lüneburg (Schließanlagen + Video) | index | 60 | 1922 | /anfrage-auswahl/ |
| /uelzen/ | 4605 | Stadtseite Uelzen | index | 58 | 2194 | /anfrage-auswahl/ |
| /karriere/ | 4408 | Jobs (4 JobPosting-Schemas), von der Optimierung ausgenommen | index | 50 | 1623 | bewerbung@ |
| /anfrage-auswahl/ | 4497 | Funnel-Auswahl (Formular 5) | noindex | | | Formulare 2/4/6 |
| /kontakt/ | 42 | Anfrage Schließsystem (Formular 2, HQ/LQ-Routing) | noindex | | | /termin/ bzw. /danke/ |
| /kontakt-kamerasysteme/ | 4371 | Anfrage Kamera (Formular 4) | noindex | | | /termin-kamerasysteme/ |
| /kontakt-kombiniert/ | 4498 | Anfrage beides (Formular 6) | noindex | | | |
| /termin/, /termin-kamerasysteme/ | 3617, 4391 | Terminbuchung (Calendly-Widget) | noindex | | | |
| /termin-gebucht/, /termin-gebucht-kamerasysteme/ | 823, 4392 | Bestätigung nach Buchung | noindex | | | |
| /danke/, /danke-seite/ | 34, 2465 | Danke-Seiten (LQ-Leads) | noindex | | | |
| /kontakt-test/, /elementor-3524/, /opt-2/ | 2457, 3524, 1606 | Test-/Altseiten (noindex, erreichbar) | noindex | | | Löschkandidaten – nur mit Freigabe |
| /wartung/ | 54 | Wartungsseite | noindex | | | |
| /agb/, /impressum/, /datenschutz/ | 782, 52, 50 | Rechtliches | noindex | | | |

Sitemap (`page-sitemap.xml`): genau die 6 indexierbaren URLs. robots.txt erlaubt alles, verweist auf die Sitemap. Suchergebnisseite (`?s=`) und 404 sind noindex bzw. liefern 404. http→https und www→non-www sind 301. Groß-/Kleinschreibung in URLs (`/Lueneburg/`) liefert 200 mit korrektem Canonical (unkritisch).

## 3. Werkzeuge und Verbindungen

**Verfügbar in dieser Umgebung**: eigener Crawler (curl/Python), Lighthouse 12.8.2 mit Chromium (Labordaten mobil/desktop), Playwright (Rendering, Screenshots), Websuche (US-zentriert) und DuckDuckGo-Abfragen mit Region DE, ffmpeg/ImageMagick/Pillow (Video- und Bildkompression), Connectoren Gmail, Pipedrive (Lead-Kennzahlen für das Reporting), Metricool (Social-Analytics).

**Nicht verfügbar**: Google Search Console, Google Analytics 4, Google Business Profile, Google Tag Manager, Bing Webmaster Tools, Backlink-/Keyword-Datenbanken (Ahrefs, Semrush, Sistrix o. ä.), PageSpeed-Insights-API (Tageskontingent erschöpft, Felddaten/CrUX daher offen). Der gespeicherte WordPress-Login ist abgelaufen; Plugin-Versionen, Updates und WP-Rocket-Einstellungen konnten deshalb nicht geprüft werden.

**Sichere Verbindungswege (keine Zugangsdaten im Chat)**:

| System | Empfohlener Weg | Variable / Ablage |
| --- | --- | --- |
| WordPress | Eigener Benutzer `seo-agent` (Rolle Administrator, jederzeit löschbar); Zugangsdaten als Secrets der Cloud-Umgebung (Sitzungs-Titelzeile → Umgebung → Bearbeiten → Netzwerk-Secrets/Umgebungsvariablen); zusätzlich optional ein Anwendungspasswort für die REST-API | `WP_SEO_USER`, `WP_SEO_PASSWORD`, optional `WP_SEO_APP_PASSWORD` |
| Search Console | Google-Cloud-Dienstkonto anlegen, dessen E-Mail-Adresse in der Search Console als Nutzer (eingeschränkt genügt) hinzufügen, Schlüssel-JSON als Secret | `GOOGLE_SA_JSON` – alternativ CSV-Exporte (Leistung 16 Monate: Suchanfragen + Seiten, Indexierung → Seiten, Core Web Vitals, Verbesserungen) in `seo/gsc-exports/` |
| Google Analytics 4 | Dasselbe Dienstkonto als „Betrachter“ in der Property-Zugriffsverwaltung | `GA4_PROPERTY_ID` |
| Google Tag Manager | Container `GTM-KV75JXFB` als JSON exportieren (Verwaltung → Container exportieren) und in `seo/gtm/` ablegen | – |
| Google Business Profile | Zugriff kann ich nicht übernehmen (kein Google-Konto). Änderungen setze ich als Checkliste auf, Kennzahlen bitte als Export/Screenshot | – |

Eine neue Sitzung liest die Secrets automatisch ein.

## 4. Technisches Audit

### 4.1 Performance (Lighthouse 12.8.2, simuliertes Mobilgerät, Laborwerte)

| Seite | Perf. | LCP | TBT | CLS | Übertragung | Requests |
| --- | --- | --- | --- | --- | --- | --- |
| Startseite mobil | 41 | 4,2 s | 14,3 s | 0,005 | 38,1 MB | 220 |
| Startseite desktop | 31 | 11,4 s | 0,9 s | 0,008 | 38,1 MB | 221 |
| /zutrittssystem/ mobil | 25 | 13,3 s | 4,6 s | 0,228 | 17,1 MB | 146 |
| /kamerasysteme/ mobil | 44 | 5,8 s | 2,2 s | 0,046 | 3,1 MB | 159 |
| /lueneburg/ mobil | 50 | 3,6 s | 4,6 s | 0,033 | 31,0 MB | 162 |

SEO-Kategorie: 100/100 auf allen Seiten. Barrierefreiheit 92–99 (Überschriften-Reihenfolge, ARIA-Rollen, Skip-Link). Best Practices 74–75 (Drittanbieter-Cookies, Konsolenfehler).

Ursachen:

- **Hintergrundvideos**: Startseite und Lüneburg laden `Main-Banner-Video-6.mp4` (14,7 MB) **und** `Main-Banner-Video-new-2.mp4` (13,2 MB), weil Desktop- und Mobil-Abschnitt jeweils ein eigenes Video haben und ausgeblendete Abschnitte trotzdem laden; „Auf Mobilgeräten abspielen“ ist aktiv. Zutrittssystem: 6,1 MB + 3,6 MB. Kamerasysteme ist mit 3,5 MB + 0,5 MB bereits das Vorbild.
- **Lottie-Animationen**: Startseite 8 JSON-Dateien à 0,88 MB (7 MB), Zutrittssystem 6 à 0,83 MB. Lottie-Bibliothek ist mit 3,5 s der größte Einzelposten der Skript-Ausführung (mobil).
- **Bilder**: PNG statt WebP/AVIF, z. B. `Untitled-design-1.png` 697 kB, `Untitled-design-12.png` 521 kB, `Ellipse-3.png` 449 kB (zweimal), `Ellipse-4.png` 238 kB. Lighthouse-Ersparnis ~1,3 MB je Seite. OG-Bild `provision_header_02-1.png` 546 kB.
- **Drittanbieter-Skripte**: Google Tag Manager 323 kB / 1,7 s Blockierzeit, Facebook 210 kB / 1,4 s, BugHerd 76 kB. Render-blockierend: `post-31.css`, `jquery.min.js`, Font-Awesome-Shims.
- **Server**: TTFB aus dem Varnish-Cache 0,7 s, ohne Cache 1,3–3,6 s (gemessen aus dieser Umgebung). Statische Dateien 30 Tage cachebar (Brotli aktiv, HTTP/2 aktiv). HTML 430–600 kB unkomprimiert (Elementor-Inline-CSS ~64 kB, 22 inline eingebettete Base64-Bilder).
- **CLS 0,228 auf /zutrittssystem/**: Hero-Container ohne reservierte Höhe (Lighthouse-Knoten `div.elementor-element > div.e-con…`).

### 4.2 Tracking und Consent

- GTM `GTM-KV75JXFB` ist auf allen Seiten eingebunden; darüber laden Google-Tag `GT-NC8XZMMS` (vermutlich GA4), Facebook-Pixel `1882223199102262` und ein Google-Ads-Conversion-Tag.
- Ohne jede Einwilligung (Lighthouse klickt nichts) werden die Cookies `fr` (Facebook), `test_cookie` (DoubleClick) und `_bugherd_session5` gesetzt. Borlabs Cookie blockiert nur YouTube/Vimeo/reCAPTCHA-Inhalte, nicht die GTM-Tags. Ob Consent Mode v2 konfiguriert ist, lässt sich nur im GTM-Container prüfen.
- **BugHerd** (`bugherd.com/sidebarv2.js`, Feedback-Tool aus der Entwicklung) ist im Quelltext aller Seiten eingebunden, meldet „Unauthenticated Error“ in der Konsole und setzt ein Cookie. Gehört nicht in die Produktion.
- Kein Search-Console-Verifizierungs-Tag im HTML (Verifizierung läuft vermutlich über GTM/GA oder DNS).

### 4.3 Strukturierte Daten

- Yoast: WebPage, BreadcrumbList, WebSite auf allen Seiten; Organization/LocalBusiness (Locksmith) mit Einsatzgebieten, Service und FAQPage auf den 5 Leistungs-/Stadtseiten (aus der Optimierung vom 29.10.).
- ProvenExpert-Widget liefert auf jeder Seite ein `Product`-Schema „ProVision Infra“ mit `aggregateRating` (ohne `offers`). Google wertet Bewertungen zum eigenen Unternehmen nicht als Rich Result; ein Hinweis „Product“ in der Search Console wäre die Folge. Beobachten, ggf. Schema-Ausgabe des Widgets abschalten.
- /karriere/: WebSite, WebPage und BreadcrumbList sind **doppelt** vorhanden (Yoast + eigener Block mit denselben `@id`s). Das ist dieselbe Konstellation, die zuvor den GSC-Fehler „Feld item fehlt“ ausgelöst hat. 4 JobPostings sind vollständig (datePosted, validThrough 31.01.2027, jobLocation, hiringOrganization).

### 4.4 Links und Navigation

- Header und Footer sind **Teil jeder Seite** (kein Theme-Builder-Template); Änderungen an der Navigation müssen je Seite erfolgen.
- Interne Links auf /lueneburg/ und /uelzen/: nur gegenseitig. Startseite, Zutrittssystem, Kamerasysteme und Karriere verlinken keine Stadtseite (Menüpunkt wurde auf Wunsch entfernt).
- Footer-Links `/agb` und `/kontakt` ohne Schrägstrich → je ein 301-Umweg auf allen Seiten.
- Anker `#mehr` (Startseite, Kamerasysteme) und `#content` (Zutrittssystem, Skip-Link) haben kein Ziel.
- Facebook-Link `facebook.com/share/1CWs2rohMt/?mibextid=wwXIfr` antwortet mit HTTP 400; die kanonische Seite ist `facebook.com/p/ProVision-Infra-GmbH-61584524562665/`.
- Telefonnummer als `tel:`-Link nur auf Stadtseiten und Karriere; Startseite, Zutrittssystem und Kamerasysteme haben keinen klickbaren Anruf-Link.
- Keine Weiterleitungsketten, keine 404 in internen Links, keine hreflang nötig (nur Deutsch, `lang="de"`).

### 4.5 Sicherheit und Hygiene (gering für SEO)

HSTS mit Preload, `X-Content-Type-Options`, XML-RPC gesperrt, REST-Nutzerliste geschützt, Autor-Enumeration blockiert, Verzeichnislisting aus. Fehlend: `X-Frame-Options`/CSP, `Referrer-Policy`, `Permissions-Policy`; `readme.html` erreichbar. WordPress 7.0.8, Elementor 4.3.5, WP Rocket 3.23.5.1, Borlabs 3.4.6 laut Generator-Tags.

## 5. Inhaltliches Audit

### 5.1 Keyword-Zuordnung (Ist)

| Seite | Primärbegriff | Belege im Haupttext |
| --- | --- | --- |
| / | digitales Schließsystem / digitale Schließanlage (Hamburg–Hannover) | „digital“ 24×, Schließanlage 14×, Schließsystem 7×, Hamburg 6×, Hannover 5× |
| /zutrittssystem/ | elektronische Schließanlage, Zutrittssystem | Schließanlage 13×, elektronisch 10×, Zutritt 10× – aber nur 913 Wörter |
| /kamerasysteme/ | Kamera-/Videoüberwachung für Unternehmen | Kamera 35×, Videoüberwachung 21× |
| /lueneburg/ | Schließanlagen + Videoüberwachung Lüneburg | Lüneburg 31×, Schließanlage 27× |
| /uelzen/ | Schließanlagen + Videoüberwachung Uelzen | Uelzen 40×, Schließanlage 30× |

Titles 50–62 Zeichen, Descriptions 152–158 Zeichen, je genau eine H1, keine Duplikate. Textähnlichkeit Lüneburg/Uelzen 19 % (6-Wort-Shingles) – unkritisch, aber bei weiteren Stadtseiten muss jede Seite eigene, echte Inhalte bekommen (keine Doorway-Pages).

### 5.2 Lücken

- Kein „Über uns“ als eigene Seite (Menüpunkt zeigt auf einen Anker der Startseite): schwache E-E-A-T-Signale, kein Ziel für Marken- und Knowledge-Panel-Signale.
- Keine Seiten für Hamburg, Hannover, Celle, Winsen, Buchholz, Soltau – die im Text und im Schema genannten Einsatzgebiete.
- Zutrittssystem (Kernseite für „elektronische Schließanlage“) ist die dünnste Leistungsseite und hat 4 Inhaltsbilder ohne Alt-Text (`Frame-2147225609…png`, `Frame-8…png`, `Frame-9-9.png`, `Untitled-design-3.png`); Startseite 1 (`4e8bba65…webp`). Die übrigen leeren Alt-Attribute sind dekorative SVG-Linien (korrekt).
- Kein Blog/Ratgeber: Fragen wie „Was kostet eine elektronische Schließanlage“, „Schlüssel verloren Schließanlage“, „Videoüberwachung am Arbeitsplatz DSGVO“ werden nur in FAQ-Akkordeons angerissen. Das ist das Feld für KI-Suche (AI Overviews, ChatGPT) und für Backlinks.

### 5.3 Suchumfeld (DuckDuckGo, Region DE, 02.11.2026; Bing-Index, nicht Google)

| Anfrage | Top-Domains | provision-infra.de |
| --- | --- | --- |
| Schließanlagen Lüneburg | andreas-schliessanlagen.de, hfs-lueneburg.de, ms-schliesstechnik.de, bofferding.de, lueneburger-schluesseldienst24.de | nicht in Top 10 |
| Schließanlage Uelzen | andreas-schliessanlagen.de, kopp-uelzen.de, afl-schluesseldienst.de, sicherheitstechnik-kortus.de | nicht in Top 10 |
| elektronische Schließanlage Hamburg | siego-sicherheitstechnik-hamburg.de, meinalarm24.de, schulz-sicherheitstechnik.de, sicherheitstechnik-kloeppner.de | nicht in Top 10 |
| digitale Schließanlage Hannover | deterding-sicherheitstechnik.de, hfs-hannover.de, sauerwein-dilcher.de, dp-elektronik.de | nicht in Top 10 |
| Videoüberwachung Unternehmen Lüneburg | ct-netze.de, lueneprotect.de, kl-lueneburg.de, ks-service-gmbh.de | nicht in Top 10 |
| Zutrittskontrolle Unternehmen Lüneburg | gruppe-fsp.de, gsg-sicherheitsdienst.de, ass-sicherheitstechnik.de | nicht in Top 10 |
| Schließanlage Bad Bevensen | Schlüsseldienste | **Platz 6** |
| ProVision Infra | provision-infra.de 1–2, Creditreform, LinkedIn, 11880, provision-isr.com (Namensnähe), ProvenExpert, werkenntdenbesten, Facebook, unternehmerjournal.de | Platz 1–2 |

`site:provision-infra.de` zeigt im Bing-Index nur 6 URLs mit veralteten Titeln („Digitales Zutrittssystem – ProVision Infra“, „Zutrittssystem – ProVision“) sowie die noindex-Seiten Danke, Danke-seite und Elementor #3524: Bing hat die Seite seit Wochen nicht neu gecrawlt. Bing Webmaster Tools + IndexNow fehlen. Google-Daten folgen mit der Search Console.

## 6. Die zehn Maßnahmen mit dem höchsten Geschäftsnutzen

| # | Maßnahme | Nutzen | Aufwand | Risiko | Freigabe |
| --- | --- | --- | --- | --- | --- |
| 1 | **Hero-Videos verschlanken**: je Seite ein Video (H.264, 1080p/720p, Ziel ≤ 3 MB), Mobil-Autoplay aus bzw. Standbild, Poster-Bild; Lottie-JSONs komprimieren und erst im Viewport laden | sehr hoch (CWV, Absprünge, Crawl-Budget) | mittel | gering – Design bleibt identisch, nur Dateien/Einstellungen | ja (Medien, Elementor-Einstellungen) |
| 2 | **BugHerd entfernen** | hoch (Konsolenfehler, Cookie ohne Consent, 76 kB) | gering | gering | ja (Code/Plugin) |
| 3 | **Consent reparieren**: Facebook-Pixel und Ads-Tag im GTM an die Borlabs-Einwilligung koppeln (Consent Mode v2), GA4 verifizieren, Conversions (Formular, Anruf, Calendly) als Ereignisse definieren | hoch (Rechtssicherheit, Messbarkeit aller weiteren Maßnahmen) | mittel | gering | ja (GTM = externes System) |
| 4 | **Stadtseiten intern verlinken**: Footer-Block „Einsatzgebiete“ (Lüneburg, Uelzen) auf allen Seiten; auf der Startseite ein Satz mit Links im Abschnitt „Digitale Schließanlagen zwischen Hamburg und Hannover“ | hoch (ohne Links kein Ranking der Stadtseiten) | gering | gering – Startseitentext: 1 Satz | ja (Design/Navigation) |
| 5 | **Bilder in WebP/AVIF** wandeln (PNG-Großbilder, OG-Bild), 4 Alt-Texte auf Zutrittssystem, 1 auf der Startseite | hoch (~1,3 MB je Seite) | gering | gering | ja (Medien) |
| 6 | **Search Console, GA4, Bing Webmaster Tools, IndexNow anbinden** (Verbindungen laut Abschnitt 3; IndexNow per Plugin oder Yoast Premium) | hoch (reale Daten statt Annahmen; Bing/ChatGPT-Index aktuell) | gering | gering | ja (Plugin) + deine Konten |
| 7 | **/zutrittssystem/ ausbauen**: CLS-Fix am Hero, Abschnitte mechanisch vs. elektronisch, Ablauf, Hersteller/Technik (nur reale Angaben), Kosten-FAQ; Ziel ≥ 1.500 Wörter | hoch (Kernseite der Kernleistung) | mittel | gering | ja (Inhalt) |
| 8 | **Google Business Profile & NAP**: Kategorien, Leistungen, Einsatzgebiete, Fotos, Beiträge, Bewertungslink; Adresse/Telefon identisch auf Website, 11880, Creditreform, werkenntdenbesten; Facebook-Link korrigieren | hoch für „Schließanlage + Stadt“-Suchen (Local Pack) | gering–mittel | gering | ja (externe Systeme, Footer-Link) |
| 9 | **Regionalseiten Hamburg und Hannover** (später Celle, Winsen, Buchholz, Soltau) nach dem Lüneburg-Muster, aber mit eigenen Inhalten: Anfahrt/Servicezeit, reale Referenzen aus der Region (von dir), lokale FAQ; plus eigene „Über uns“-Seite | sehr hoch (Zielregion ohne Präsenz) | hoch | mittel (nur mit echten Inhalten, sonst Doorway-Risiko) | ja (neue Seiten/URLs) |
| 10 | **Conversion-Elemente**: klickbare Telefonnummer im Header/Sticky-Leiste aller Seiten, Calendly-Buchung auch auf Leistungsseiten verlinken, Testseiten /kontakt-test/, /elementor-3524/, /opt-2/ entfernen (nach Prüfung) | mittel–hoch (mehr Anfragen aus bestehendem Traffic) | gering | gering | ja (Design, Löschen) |

Kleinere Punkte für denselben Durchgang: Footer-Links auf `/agb/` und `/kontakt/` mit Schrägstrich, tote Anker `#mehr`/`#content`, doppelte Schema-Knoten auf /karriere/ (nur technisch, Text bleibt), Cache-Laufzeit statischer Dateien auf 1 Jahr (Raidboxes-Einstellung), WP-Rocket-Optionen „JavaScript verzögern“ für GTM/Lottie/ProvenExpert und „Ungenutztes CSS entfernen“ (erst nach Einsicht in die aktuelle Konfiguration).

Ausdrücklich **nicht** vorgesehen: Änderungen am Startseitentext über den einen Verlinkungssatz hinaus, Änderungen an /karriere/ (außer Schema-Doppelung), URL-Änderungen, Design-Umbauten.

## 7. Priorisierte Umsetzungsübersicht

| Sprint | Zeitraum | Inhalt | Voraussetzung |
| --- | --- | --- | --- |
| 1 „Technik“ | Woche 1–2 | Maßnahmen 1, 2, 5 + Kleinpunkte (Links, Anker, Alt-Texte, Karriere-Schema); Lighthouse vorher/nachher je Seite | WordPress-Zugang (Secrets) |
| 2 „Messen & Consent“ | Woche 1–3 parallel | Maßnahmen 3 und 6; Baseline aus GSC (16 Monate), GA4, Pipedrive-Leads; Bing Webmaster Tools, IndexNow | GSC/GA4-Dienstkonto, GTM-Export, Plugin-Freigabe |
| 3 „Inhalt & Verlinkung“ | Woche 3–6 | Maßnahmen 4, 7, 10; Keyword-Architektur auf Basis echter GSC-Daten (Phase 4) | Freigabe der Texte vor Veröffentlichung |
| 4 „Region & Local“ | Woche 6–12 | Maßnahmen 8 und 9: Hamburg, Hannover, Über uns; GBP-Ausbau; erste Ratgeber-Inhalte für KI-Suche | Reale Referenzen/Fotos je Region von dir |

Vor jeder Änderung: Sicherung des Ist-Zustands (Elementor-JSON und Yoast-Werte je Seite im Repository), Vorschau-Prüfung, dann Veröffentlichung; Wochenbericht mit Vorher/Nachher-Messwerten.

## 8. Rohdaten

- `seo/data/phase1/pages_summary.json` – alle Seiten: Meta-Daten, Überschriften, Keyword-Zählung, Bilder, Links, Schema.
- `seo/data/phase1/lighthouse_summary.json` – Lighthouse-Kennzahlen und Opportunities (5 Läufe).
- `seo/data/phase1/serp_ddg_2026-11-02.json` – Suchergebnis-Stichproben.
- `seo/data/phase1/timing.csv`, `internal_links.txt` – Statuscodes, Antwortzeiten, Linkziele.
- `tools/seo_audit/` – Crawler (`analyze.py`, `details.py`), SERP-Abfrage (`serp.py`), Lighthouse-Läufe (`run_lh.sh`, `lh_parse.py`), Backend-Audit (`backend_audit.js`, benötigt gültige WordPress-Sitzung).
