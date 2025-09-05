import json

import requests
from bs4 import BeautifulSoup

url = "https://www.srf.ch/news"
HEADERS = {"User-Agent": "Chrome/120.0.0.0"}

try:
    antwort = requests.get(url, headers=HEADERS, timeout=15)
    antwort.raise_for_status()
except requests.exceptions.RequestException as e:
    print("Fehler beim Abruf:", e)
    exit()

soup = BeautifulSoup(antwort.text, "html.parser")

headlines = []
for a in soup.select('a[href*="/news/"]'):
    text = a.get_text(strip=True)
    if text and len(text) >= 12:
        headlines.append(text)
    if len(headlines) == 5:
        break

if headlines:
    print("SRF Schlagzeilen:")
    for t in headlines:
        print("-", t)

    # txt datei
    with open("resources/headlines.txt", "w", encoding="utf-8") as f:
        f.write("Projekt Webautomatisierung von Severin\n")
        f.write("Headlines von SRF.ch\n")
        f.write("\n")
        for t in headlines:
            f.write(f"- {t}\n")

    # JSON datei
    data = {
        "titel": "Projekt Webautomatisierung von Severin",
        "untertitel": "Headlines von SRF.ch",
        "headlines": [f"- {t}" for t in headlines],
    }
    with open("resources/headlines.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

else:
    print("Keine Headline gefunden")
