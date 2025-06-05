from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from db import engine
from models import Cliente, ProfiloRischio, TriggerRischio
from services.serpapi_client import cerca_articoli_google
from services.article_scraper import estrai_testo_articolo
from services.nlp_analysis import analizza_testo_articolo
from services.scoring import calcola_rischio
import json

router = APIRouter()

@router.get("/analizza-cliente/{cliente_id}/dettagliato")
def analizza_cliente_completo(cliente_id: int):
    with Session(engine) as session:
        cliente = session.exec(select(Cliente).where(Cliente.id == cliente_id)).first()
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente non trovato.")

        articoli = cerca_articoli_google(cliente.nome, cliente.cognome)
        risultati = []

        for url in articoli:
            testo = estrai_testo_articolo(url)
            if not testo:
                continue
            analisi = analizza_testo_articolo(testo)
            risultati.append({"url": url, "estratti": analisi})

        return {
            "cliente": f"{cliente.nome} {cliente.cognome}",
            "articoli_analizzati": len(risultati),
            "risultati": risultati
        }

@router.post("/profiling-cliente/{cliente_id}")
def profiling_cliente(cliente_id: int):
    with Session(engine) as session:
        cliente = session.exec(select(Cliente).where(Cliente.id == cliente_id)).first()
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente non trovato.")

        articoli = cerca_articoli_google(cliente.nome, cliente.cognome)
        risultati = []

        for url in articoli:
            testo = estrai_testo_articolo(url)
            if not testo:
                continue
            analisi = analizza_testo_articolo(testo)
            risultati.append({"url": url, "estratti": analisi})

        valutazione = calcola_rischio(risultati)

        profilo = ProfiloRischio(
            cliente_id=cliente.id,
            punteggio=valutazione["punteggio"],
            livello=valutazione["livello"],
            articoli_analizzati=len(risultati),
            fonti=json.dumps(valutazione["url_rischiosi"])
        )
        session.add(profilo)

        if valutazione["livello"] == "Alto":
            trigger = TriggerRischio(
                cliente_id=cliente.id,
                motivo="Profiling rischio alto",
                livello="Critico"
            )
            session.add(trigger)

        session.commit()
        return {
            "profilo_rischio": {
                "livello": valutazione["livello"],
                "punteggio": valutazione["punteggio"],
                "url_sospetti": valutazione["url_rischiosi"]
            },
            "trigger_generato": valutazione["livello"] == "Alto"
        }
