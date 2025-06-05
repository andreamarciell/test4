from fastapi import APIRouter, Query
from sqlmodel import Session, select
from ..db import engine
from ..models import ProfiloRischio, TriggerRischio

router = APIRouter()

@router.get("/tutti-profili-rischio")
def tutti_profili_rischio():
    with Session(engine) as session:
        return session.exec(select(ProfiloRischio)).all()

@router.get("/clienti/{cliente_id}/profili-rischio")
def get_profili_rischio(cliente_id: int):
    with Session(engine) as session:
        profili = session.exec(
            select(ProfiloRischio).where(ProfiloRischio.cliente_id == cliente_id)
        ).all()
        return profili

@router.get("/trigger-aml/")
def get_trigger(stato: str = None, livello: str = None):
    with Session(engine) as session:
        query = select(TriggerRischio)
        if stato:
            query = query.where(TriggerRischio.stato == stato)
        if livello:
            query = query.where(TriggerRischio.livello == livello)
        return session.exec(query).all()
