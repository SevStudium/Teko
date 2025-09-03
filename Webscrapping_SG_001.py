
#Praxisarbeit Webautomatisierung


# Falls noch nicht vorhanden:
# pip install requests beautifulsoup4


print("Hello")

import requests
from bs4 import BeautifulSoup

url = "https://www.srf.ch/news"


antwort = requests.get(url)
html_code = antwort.text

soup = BeautifulSoup(html_code, "html.parser")

headlines = soup.find_all("h2")

for h in headlines:
    text = h.get_text(strip=True)
    if len(text) > 5:  # ganz kurze Sachen ignorieren
        print(text)


