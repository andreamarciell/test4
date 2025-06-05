import logging
from newspaper import Article
from typing import Optional

logger = logging.getLogger(__name__)

def estrai_testo_articolo(url: str) -> Optional[str]:
    try:
        articolo = Article(url, language='it')
        articolo.download()
        articolo.parse()
        return articolo.text
    except Exception as e:
        logger.error("Errore nell'estrazione dell'articolo %s: %s", url, e)
        return None
