import requests
from typing import List
from urllib.parse import quote

SERPAPI_KEY = "de89ead1a44b2aaca95d62ffc20554327dac3ca8559a4ad903fdc733a7fa4f17"

def cerca_articoli_google(nome: str, cognome: str, limiti: int = 5) -> List[str]:
    query = f'"{nome} {cognome}"'
    url = f"https://serpapi.com/search.json?q={quote(query)}&api_key={SERPAPI_KEY}&hl=it&gl=it"

    response = requests.get(url)
    if response.status_code != 200:
        return []

    data = response.json()
    risultati = data.get("organic_results", [])
    link_utili = []

    for item in risultati:
        link = item.get("link")
        if link and "google.com" not in link:
            link_utili.append(link)

        if len(link_utili) >= limiti:
            break

    return link_utili