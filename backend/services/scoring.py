from models import RegolaRischio
from sqlmodel import Session, select
from db import engine
from typing import List, Dict

def calcola_rischio(articoli: List[Dict]) -> Dict:
    with Session(engine) as session:
        regole_attive = session.exec(
            select(RegolaRischio).where(RegolaRischio.attiva == True)
        ).all()
        mappa_pesi = {r.nome: r.peso for r in regole_attive}

    punteggio = 0
    url_rischiosi = {}

    for articolo in articoli:
        score_articolo = 0
        estratti = articolo["estratti"]
        reati = estratti.get("reati", [])

        if reati:
            score_articolo += mappa_pesi.get("reato_generico", 70)

        if any(r in reati for r in ["mafia", "corruzione", "droga"]):
            score_articolo += mappa_pesi.get("parola_mafia", 100)

        if any(term in reati for term in ["arrestato", "condannato"]):
            score_articolo += mappa_pesi.get("arrestato_o_condannato", 90)

        if score_articolo > 0:
            url_rischiosi[articolo["url"]] = score_articolo
            punteggio += score_articolo

    if len(url_rischiosi) >= 2:
        punteggio += mappa_pesi.get("articoli_multipli", 30)

    livello = "Basso"
    if punteggio >= 120:
        livello = "Alto"
    elif punteggio >= 60:
        livello = "Medio"

    return {
        "punteggio": punteggio,
        "livello": livello,
        "url_rischiosi": url_rischiosi
    }