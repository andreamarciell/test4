from fastapi import FastAPI
from sqlmodel import SQLModel
from db import engine
from routes.analisi import router as analisi_router
from routes.dashboard import router as dashboard_router
from routes.report import router as report_router
from routes.admin_regole import router as admin_router
from routes.import_clienti import router as import_router

app = FastAPI()

# Ensure tables are created at startup
SQLModel.metadata.create_all(engine)

app.include_router(analisi_router)
app.include_router(dashboard_router)
app.include_router(report_router)
app.include_router(admin_router)
app.include_router(import_router)