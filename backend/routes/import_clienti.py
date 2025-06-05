from fastapi import APIRouter, UploadFile, File, HTTPException
from sqlmodel import Session, select
from db import engine
from models import Cliente
import csv
from io import StringIO
from datetime import datetime

router = APIRouter()

@router.post("/importa-clienti/")
async def importa_clienti(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Il file deve essere un CSV.")

    contents = await file.read()
    decoded = contents.decode('utf-8')
    reader = csv.DictReader(StringIO(decoded))

    clienti_importati = 0
    with Session(engine) as session:
        for row in reader:
            try:
                data_nascita = datetime.strptime(row['data_nascita'], '%Y-%m-%d').date()
            except ValueError:
                continue

            cliente = Cliente(
                nome=row['nome'].strip(),
                cognome=row['cognome'].strip(),
                data_nascita=data_nascita,
                nazionalità=row['nazionalità'].strip(),
                codice_fiscale=row.get('codice_fiscale', '').strip() or None
            )

            esiste = session.exec(
                select(Cliente).where(
                    Cliente.nome == cliente.nome,
                    Cliente.cognome == cliente.cognome,
                    Cliente.data_nascita == cliente.data_nascita
                )
            ).first()
            if esiste:
                continue

            session.add(cliente)
            clienti_importati += 1

        session.commit()
    return {"importati": clienti_importati}