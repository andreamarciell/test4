import os
import requests
from typing import List
from urllib.parse import quote

# The API key is now read from the environment to avoid hardcoding
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

def cerca_articoli_google(nome: str, cognome: str, limiti: int = 5) -> List[str]:
    if not SERPAPI_KEY:
        # missing API key -> nothing to search
        return []

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