Praxisarbeit Webautomatisierung von Séverin Gschwind

Kurzbeschreibung:
Dieses Projekt liest Schlagzeilen von srf.ch/news aus, filtert sie (nur „echte“ Headlines, optional auf ersten Satz gekürzt) und speichert die Ergebnisse in TXT, JSON, CSV, XML.
Zusätzlich wird die Häufigkeit des Begriffs „Schweiz“ in den aktuellen Headlines gezählt und als Diagramm (PNG) ausgegeben.
Ein Logfile dokumentiert jeden Lauf.

Voraussetzungen:
- Python 3.10+ installiert (Windows)
- Pakete:
- - requests
- - beautifulsoup4
- - matplotlib
 
Schritt für Schritt (Windows / PowerShell):
- Projektordner öffnen (z.B. in VS Code).
- Terminal öffnen und ins src wechseln:
- cd Laufwerk:\Pfad\src
- Skript starten:
- - python Webscraping_SG_001.py

Ergebnisse ansehen:
Die Ergebnisse werden in der Konsole angezeigt. Zusätzlich werden sie noch hier gespeichert:
- data/headlines.txt|json|csv|xml
- data/WordCountSchweizChart.png
- logs/run.log (Ablauf/Fehler/Anzahl Headlines)

Was das Skript macht:
- Das Skript ruft die Webseite srf.ch/news automatisiert ab.
- Die Schlagzeilen werden dabei wie folgt verarbeitet:
- Abruf & Parsing: Die HTML-Seite wird mit requests geladen und mit BeautifulSoup ausgewertet.
- Filter: Es werden nur Headlines berücksichtigt, die mindestens 20 Zeichen und 4 Wörter enthalten. Standard-Kategorien wie International, Gesellschaft oder Sport werden ignoriert.
- Kürzung: Jede Headline wird auf den ersten vollständigen Satz (bis zum Punkt) reduziert.
- Anzahl: Es werden maximal die ersten 10 Headlines gespeichert.
- Speicherung: Ergebnisse werden in vier Formaten abgelegt.
- Analyse: Zusätzlich wird gezählt, wie oft das Wort „Schweiz“ (inkl. Ableitungen wie „Schweizer“) vorkommt.
- Visualisierung: Ein Liniendiagramm zeigt die Häufigkeit pro Headline. Ausgabe: data/WordCountSchweizChart.png.
- Logging: Jeder Programmlauf erzeugt Einträge im Logfile logs/run.log (Start, Abruf, Anzahl Headlines, gespeicherte Dateien, Ende).

Troubleshooting:
Das Skript gibt an mehreren Stellen klare Meldungen aus, die dir helfen, Probleme sofort zu erkennen:
- „Fehler beim Abruf“: Die Webseite konnte nicht geladen werden (z. B. kein Internet, SRF nicht erreichbar).
- „Keine Headline gefunden“ / „Script beendet“: Auf der Seite wurden keine gültigen Schlagzeilen erkannt. Das Programm bricht ab, ohne Dateien zu schreiben.
- „Datei gespeichert: …“ (im Logfile): Dateien wurden korrekt geschrieben.
- „Anzahl Headlines gefunden: 0“: Es wurde zwar eine Verbindung aufgebaut, aber keine Headline erfüllte die Filterkriterien.
- „WordCount … = 0“: Das gesuchte Wort (z. B. „Schweiz“) kam in den Headlines nicht vor.



