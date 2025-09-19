import json, csv
import xml.etree.ElementTree as ET

import requests
from bs4 import BeautifulSoup

from pathlib import Path
from datetime import datetime

# Ordnerstruktur 
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Zeitstempel
run_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Abruf
url = "https://www.srf.ch/news"
HEADERS = {"User-Agent": "Chrome/120.0.0.0"}

try:
    antwort = requests.get(url, headers=HEADERS, timeout=15)
    antwort.raise_for_status()
except requests.exceptions.RequestException as e:
    print("Fehler beim Abruf:", e)
    exit()

soup = BeautifulSoup(antwort.text, "html.parser")

# Headlines sammeln
headlines = []
for a in soup.select('a[href*="/news/"]'):
    text = a.get_text(strip=True)
    if text and len(text) >= 12:
        headlines.append(text)
    if len(headlines) == 5:
        break

if not headlines:
    print("Keine Headline gefunden")
    exit()

# Ausgabe Console
print("Projekt Webautomatisierung von Séverin")
print(f"Stand: {run_time}\n")
print("Headlines von SRF.ch:")

for t in headlines:
    print("-", t)

# txt datei
with (DATA_DIR / "headlines.txt").open("w", encoding="utf-8") as f:
    f.write("Projekt Webautomatisierung von Séverin\n")
    f.write("Headlines von SRF.ch:\n")
    f.write(f"Stand: {run_time}\n\n")
    for t in headlines:
        f.write(f"- {t}\n")

# JSON datei
data = {
    "titel": "Projekt Webautomatisierung von Séverin",
    "untertitel": "Headlines von SRF.ch",
    "stand": run_time,
    "headlines": [f"- {t}" for t in headlines],
}
with (DATA_DIR / "headlines.json").open("w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# CSV datei
with (DATA_DIR / "headlines.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["time", "index", "headline"])
    for i, t in enumerate(headlines, start=1):
        w.writerow([run_time, i, t])

# XML datei
root = ET.Element("headlines", attrib={"stand": run_time, "quelle": "srf.ch/news"})
for i, t in enumerate(headlines, start=1):
    item = ET.SubElement(root, "item", attrib={"index": str(i)})
    item.text = t
tree = ET.ElementTree(root)
ET.indent(tree, space="  ", level=0)
tree.write(DATA_DIR / "headlines.xml", encoding="utf-8", xml_declaration=True)


