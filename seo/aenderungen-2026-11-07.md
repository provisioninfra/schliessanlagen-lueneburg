# Startseite: Hero-Headline leicht vergrößert (07.11.2026)

Auftrag: Die H1 „Wir installieren in deinem Unternehmen ein digitales Schließsystem“ auf der Startseite (#31, Elementor-Widget `9dcea29`) ganz leicht vergrößern, Formatierung auf allen Bildschirmklassen prüfen, veröffentlichen. Text, Farben, Breiten, Abstände, Animationen und alle anderen Elemente blieben unverändert.

## Werte je Breakpoint (Elementor-Kit: Mobil ≤ 767, Tablet 768–1024, Tablet extra 1025–1280, Laptop 1281–1440, Desktop > 1440)

| Breakpoint | Schriftgröße vorher → nachher | Zeilenhöhe vorher → nachher |
| --- | --- | --- |
| Desktop (> 1440 px, auch Widescreen) | 52 → 55 px | 124 % (unverändert, 64,5 → 68,2 px) |
| Laptop (1281–1440 px) | 40 → 42 px | 124 % (49,6 → 52,1 px) |
| Tablet extra (1025–1280 px) | 35 → 37 px | 40 → 42 px |
| Tablet (768–1024 px, auch Smartphone quer) | 25 → 27 px | 35 → 37 px |
| Mobil (≤ 767 px) | 22 → 24 px | 25 → 27 px |

Umsetzung: `tools/startseite_h1/patch_h1.py` über `pagepatch.js` (Live-Stand laden, Werte mit Soll-Prüfung ersetzen, `save_builder` mit Status „publish“). Elementor hat `post-31.css` neu erzeugt, WP Rocket und Varnish wurden beim Speichern für die URL geleert; die Messung erfolgte am Live-HTML mit Cache-Umgehung.

## Prüfung (Playwright/Chromium, Live-Seite)

| Viewport | Schrift | Zeilen vorher → nachher | H1-Höhe | Abstand zur Subline | Überlauf |
| --- | --- | --- | --- | --- | --- |
| PC 1920×1080 | 55 px | 2 → 3 | 129 → 205 px | 55 px (gleich) | nein |
| PC 1440×900 | 42 px | 3 → 3 | 149 → 156 px | 15 px (gleich) | nein |
| Laptop 1366×768 | 42 px | 3 → 3 | 149 → 156 px | 15 px | nein |
| Laptop 1280×720 | 37 px | 3 → 3 | 120 → 126 px | 20 px | nein |
| Tablet quer 1024×768 | 27 px | 2 → 2 | 70 → 74 px | 20 px | nein |
| Tablet hochkant 820×1180 | 27 px | 2 → 2 | 70 → 74 px | 20 px | nein |
| Tablet hochkant 768×1024 (echter iPad-Browser) | 27 px | 2 → 3 | 70 → 111 px | 20 px | nein |
| Smartphone hochkant 430 / 390 / 360 px | 24 px | 3 → 3 | 75 → 81 px | 18 px | nein |
| Smartphone quer 932×430 / 844×390 | 27 px | 2 → 2 | 70 → 74 px | 20 px | nein |

Zeilenumbrüche: Auf 1920 px passt die fette erste Zeile „Wir installieren in deinem Unternehmen“ ab 54 px nicht mehr in die 1092 px breite Textspalte (gemessene Textbreite 1066 px bei 52 px, 1128 px bei 55 px); ein Verbreitern der Spalte würde die Zeile in die Tür-Grafik laufen lassen. Die Headline bricht daher auf großen Bildschirmen wie auf Tablet und Smartphone nach „deinem“ um, drei ausgewogene Zeilen, Subline, Absatz, Button und Bewertungszeile rücken um 76 px nach unten und bleiben auf 1080p im ersten Bildschirm. Auf 768 px breiten Tablets (iPad hochkant) entsteht ebenfalls der dreizeilige Umbruch; ab 790 px Breite bleiben es zwei Zeilen. Alle anderen Breiten behalten ihre Zeilenstruktur.

Funktion: Hero-Videos (Desktop und Handy) `readyState 4`, Einblend-Animationen und Lottie unverändert, kein horizontaler Überlauf, Hero-Container auf 1920 px 1042 px hoch mit nahtlosem Übergang zur Folgesektion. Screenshots vorher/nachher (1920 px, 1440 px, 390 px) liegen im Sitzungs-Scratchpad; die Messwerte in `seo/data/startseite_h1/`.
