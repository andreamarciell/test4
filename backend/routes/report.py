from fastapi import APIRouter
from sqlmodel import Session, select
from models import Cliente, ProfiloRischio
from db import engine
from services.report_generator import genera_report_docx
import os

router = APIRouter()

@router.get("/report/{cliente_id}")
def genera_report(cliente_id: int):
    with Session(engine) as session:
        cliente = session.exec(select(Cliente).where(Cliente.id == cliente_id)).first()
        profilo = session.exec(
            select(ProfiloRischio).where(ProfiloRischio.cliente_id == cliente_id)
        ).first()
        if not profilo or not cliente:
            return {"errore": "Dati non trovati"}

        cliente_data = {
            "id": cliente.id,
            "nome": cliente.nome,
            "cognome": cliente.cognome,
            "data_nascita": str(cliente.data_nascita),
            "nazionalità": cliente.nazionalità
        }

        profilo_data = {
            "punteggio": profilo.punteggio,
            "livello": profilo.livello,
            "articoli_analizzati": profilo.articoli_analizzati,
            "fonti": profilo.fonti
        }

        output_path = os.path.abspath("reports")
        os.makedirs(output_path, exist_ok=True)
        path_file = genera_report_docx(cliente_data, profilo_data, output_path)
        return {"report_path": path_file}