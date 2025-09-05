
#Praxisarbeit Webautomatisierung


# Falls noch nicht vorhanden:
# pip install requests beautifulsoup4


print("Hello")

import requests
from bs4 import BeautifulSoup
import json

url = "https://www.srf.ch/news"
HEADERS = {"User-Agent": "Chrome/120.0.0.0"} 

antwort = requests.get(url, headers=HEADERS, timeout=15)

soup = BeautifulSoup(antwort.text, "html.parser")

headlines = []
for a in soup.select('a[href*="/news/"]'):
    text = a.get_text(strip=True)
    if text and len(text) >= 12:
        headlines.append(text)
    if len(headlines) == 5:
        break

if headlines:
    for t in headlines:
        print("-", t)
else:
    print("Keine Headline gefunden!")

#Headlines in txt datei speichern

with open("headlines.txt", "w", encoding="utf-8") as f:
    for t in headlines:
        f.write(t + "\n")

#JSON Datei erstellen
with open("headlines.json", "w", encoding="utf-8") as f:
    json.dump(headlines, f, ensure_ascii=False, indent=2)


