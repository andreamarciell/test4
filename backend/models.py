from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date

class Cliente(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    cognome: str
    data_nascita: date
    nazionalità: str
    codice_fiscale: Optional[str] = None
    data_importazione: date = Field(default_factory=date.today)

class ProfiloRischio(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cliente_id: int = Field(foreign_key="cliente.id")
    data: date = Field(default_factory=date.today)
    punteggio: int
    livello: str
    articoli_analizzati: int
    fonti: str

class TriggerRischio(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cliente_id: int = Field(foreign_key="cliente.id")
    motivo: str
    livello: str
    data: date = Field(default_factory=date.today)
    stato: str = "nuovo"

class RegolaRischio(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    peso: int
    attiva: bool = True