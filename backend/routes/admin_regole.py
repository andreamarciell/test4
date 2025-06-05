from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from ..db import engine
from ..models import RegolaRischio

router = APIRouter()

@router.get("/regole/")
def lista_regole():
    with Session(engine) as session:
        return session.exec(select(RegolaRischio)).all()

@router.post("/regole/")
def aggiungi_regola(regola: RegolaRischio):
    with Session(engine) as session:
        session.add(regola)
        session.commit()
        session.refresh(regola)
        return regola

@router.put("/regole/{regola_id}")
def modifica_regola(regola_id: int, nuova_regola: RegolaRischio):
    with Session(engine) as session:
        r = session.get(RegolaRischio, regola_id)
        if not r:
            raise HTTPException(status_code=404, detail="Regola non trovata")
        r.nome = nuova_regola.nome
        r.peso = nuova_regola.peso
        r.attiva = nuova_regola.attiva
        session.commit()
        return r