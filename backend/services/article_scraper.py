from newspaper import Article
from typing import Optional

def estrai_testo_articolo(url: str) -> Optional[str]:
    try:
        articolo = Article(url, language='it')
        articolo.download()
        articolo.parse()
        return articolo.text
    except:
        return None