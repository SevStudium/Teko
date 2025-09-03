
#Praxisarbeit Webautomatisierung


# Falls noch nicht vorhanden:
# pip install requests beautifulsoup4


print("Hello")

import requests
from bs4 import BeautifulSoup

url = "https://www.srf.ch/news"
HEADERS = {"User-Agent": "Chrome/120.0.0.0"} 

antwort = requests.get(url, headers=HEADERS, timeout=15)

soup = BeautifulSoup(antwort.text, "html.parser")

headline_text = None
for a in soup.select('a[href*="/news/"]'):
    text = a.get_text(strip=True)
    if text and len(text) > 20:
        headline_text = text
        break

if headline_text:
    print("Erste SRF-Headline (Chrome User-Agent):")
    print(headline_text)
else:
    print("Keine Headline gefunden")

