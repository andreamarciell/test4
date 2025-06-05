import spacy
from typing import List, Dict

nlp = spacy.load("it_core_news_sm")

PAROLE_REATO = [
    "omicidio", "estorsione", "truffa", "riciclaggio", "corruzione", 
    "droga", "mafia", "arrestato", "condannato", "indagato"
]

def analizza_testo_articolo(testo: str) -> Dict:
    doc = nlp(testo)

    reati_trovati = []
    date_trovate = []
    nomi_trovati = []

    for ent in doc.ents:
        if ent.label_ == "PER":
            nomi_trovati.append(ent.text)
        if ent.label_ == "DATE":
            date_trovate.append(ent.text)

    parole_chiave = [kw for kw in PAROLE_REATO if kw in testo.lower()]
    reati_trovati.extend(parole_chiave)

    return {
        "nomi_menzionati": list(set(nomi_trovati)),
        "date": list(set(date_trovate)),
        "reati": list(set(reati_trovati))
    }
