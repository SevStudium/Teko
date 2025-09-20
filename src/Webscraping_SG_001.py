"""
Projektarbeit Webscraping
SRF-Headlines Scraper
Abruf -> Filter -> Ausgabe/Export (TXT/JSON/CSV/XML/PNG), Logs in logs/run.log.
Start: cd src && python Webscraping_SG_001.py
Ordner: data/ (Outputs), logs/ (run.log), src/ (Code)
Autor: Séverin Gschwind
Datum: 22.09.2025
"""

# Standardbibliothek: Datenformate, Pfade, Zeit, Regex, Logging
import csv
import json
import logging
import sys
import re
import random
from pathlib import Path
from datetime import datetime
import xml.etree.ElementTree as ET  # XML-Baum (Standardlib)

# Drittanbieter,HTTP, HTML-Parsing, Visualisierung
import requests
from bs4 import BeautifulSoup       # HTML-Parser
import matplotlib.pyplot as plt     # Diagramme


# Ordnerstruktur 
# BASE_DIR zeigt auf die Projektebene (Ebene über src/)
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Datenordner für alle Outputs
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# Logfile einrichtung (in Datei)
LOG_FILE = LOGS_DIR / "run.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(LOG_FILE, encoding="utf-8")]
)

# Zeitstempel
run_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
logging.info(f"=== Script gestartet um: {run_time} ===")

# Abruf (Zielseite und ein einfacher User-Agent, damit die Anfrage nicht wie ein Bot wirkt)
url = "https://www.srf.ch/news"
HEADERS = {"User-Agent": "Chrome/120.0.0.0"}

try:
    antwort = requests.get(url, headers=HEADERS, timeout=15)
    antwort.raise_for_status()
    logging.info("Abruf erfolgreich von URL: %s", url)
except requests.exceptions.RequestException as e:
    logging.error("Fehler beim Abruf: %s", e)
    print("Fehler beim Abruf:", e)
    exit()

# HTML in Soup überführen (Parser: html.parser reicht für SRF)
soup = BeautifulSoup(antwort.text, "html.parser")

# Headlines sammeln NEU spezifischer (Stopwoerter: Navigations-/ Rubriktitel, die keine echte Headline sind)
STOPWORTE = {
    "International", "Gesellschaft", "Schweiz", "Sport", "Kultur",
    "Wissen", "Panorama", "Wirtschaft", "Videos", "Podcasts",
    "News", "SRF News", "Mein Account"
}

def ist_echte_headline(t: str) -> bool:
    t = t.strip()
    if not t or t in STOPWORTE:
        return False
    
    if len(t) < 20 or len(re.findall(r"\w+", t)) < 4:
        return False
    
    if any(c.isalpha() for c in t) and t.upper() == t:
        return False
    return True

def erster_satz(text: str) -> str:
    if "." in text:
        return text.split(".")[0].strip() + "."
    return text.strip()

# Selector-Reihenfolge: zuerst typische Titel-Container (h2/h3), dann Fallback
kandidaten = soup.select(
    'h2 a[href*="/news/"], h3 a[href*="/news/"], '
    'a[href*="/news/"][aria-label], a[href*="/news/"][data-analytics], '
    'a[href*="/news/"]'
)
gesehen = set() # Duplikate vermeiden
headlines = [] 
for a in kandidaten:     
    text = a.get_text(strip=True)             
    if ist_echte_headline(text) and text not in gesehen:    
        gesehen.add(text)
        headlines.append(erster_satz(text)) # nur erster Satz der Headline

# Nur die ersten 10 Headlines für eine stabile, übersichtliche Ausgabe        
headlines = headlines[:10]

logging.info("Anzahl Headlines gefunden (nach Filter/Dedupe): %d", len(headlines))

if not headlines:
    logging.warning("Keine Headline gefunden – Script beendet.") # Ende, wenn nichts Qualifiziertes gefunden wurde
    print("Keine Headline gefunden")
    exit()

# Regel für Schweiz (aus keinem spezifischen Grund)- Case-insensitive Treffer inkl. Ableitungen (schweiz, Schweizer, schweizerisch, ...)
pattern = re.compile(r"schweiz\w*", re.IGNORECASE)

# Anzahl pro Headline (Liste mit Count je Headline)
schweiz_hits = [len(pattern.findall(h)) for h in headlines]
schweiz_count = sum(schweiz_hits)
logging.info("WordCount 'Schweiz': je Headline=%s | Gesamt=%d", schweiz_hits, schweiz_count)
print(f"WordCount 'Schweiz': {schweiz_count}")

# Plot (Liniendiagramm: X = Headline-Index (1..N), Y = Treffer pro Headline)
plt.figure(figsize=(8, 5))
plt.plot(range(1, len(headlines) + 1), schweiz_hits, marker="o", linestyle="-")
plt.xticks(range(1, len(headlines) + 1), [str(i) for i in range(1, len(headlines) + 1)])
plt.yticks(range(0, max(schweiz_hits) + 2))  
plt.title("WordCount 'Schweiz' in SRF-Headlines")
plt.xlabel("Headlines")
plt.ylabel("Anzahl Vorkommen")
plt.grid(True)

# PNG datei (Chart in data/ speichern)
plt.savefig(DATA_DIR / "WordCount.png")
plt.close()
logging.info("PNG gespeichert: %s", DATA_DIR / "WordCount.png")

# Ausgabe Console (Lesbare Zusammenfassung für den direkten Bestätigung der Funktion)
print("Projekt Webautomatisierung von Séverin")
print(f"Stand: {run_time}\n")
print("Headlines von SRF.ch:")



for t in headlines:
    print("-", t)

# txt datei (einfache Textliste für schnelle Kontrolle / Weitergabe, in data/ speichern)
with (DATA_DIR / "headlines.txt").open("w", encoding="utf-8") as f:
    f.write("Projekt Webautomatisierung von Séverin\n")
    f.write("Headlines von SRF.ch:\n")
    f.write(f"Stand: {run_time}\n\n")
    for t in headlines:
        f.write(f"- {t}\n")
logging.info("TXT gespeichert: %s", DATA_DIR / 'headlines.txt')

# JSON datei (strukturierte, leicht weiterverarbeitbare Repräsentation, in data/ speichern)
data = {
    "titel": "Projekt Webautomatisierung von Séverin",
    "untertitel": "Headlines von SRF.ch",
    "stand": run_time,
    "headlines": [f"- {t}" for t in headlines],
}
with (DATA_DIR / "headlines.json").open("w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
logging.info("JSON gespeichert: %s", DATA_DIR / 'headlines.json')

# CSV datei (tabellenform für Excel/BI-Tools, in data/ speichern)
with (DATA_DIR / "headlines.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["time", "index", "headline"])
    for i, t in enumerate(headlines, start=1):
        w.writerow([run_time, i, t])
logging.info("CSV gespeichert: %s", DATA_DIR / 'headlines.csv')

# XML datei (hierarchische Struktur, gut für Systeme, die XML erwarten , in data/ speichern)
root = ET.Element("headlines", attrib={"stand": run_time, "quelle": "srf.ch/news"})
for i, t in enumerate(headlines, start=1):
    item = ET.SubElement(root, "item", attrib={"index": str(i)})
    item.text = t
tree = ET.ElementTree(root)
ET.indent(tree, space="  ", level=0)        # Einrückung  
tree.write(DATA_DIR / "headlines.xml", encoding="utf-8", xml_declaration=True)
logging.info("XML gespeichert: %s", DATA_DIR / 'headlines.xml')

logging.info("=== Script erfolgreich beendet ===") # Ende

