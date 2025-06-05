from fastapi import FastAPI
from routes.analisi import router as analisi_router
from routes.dashboard import router as dashboard_router
from routes.report import router as report_router
from routes.admin_regole import router as admin_router
from routes.import_clienti import router as import_router

app = FastAPI()

app.include_router(analisi_router)
app.include_router(dashboard_router)
app.include_router(report_router)
app.include_router(admin_router)
app.include_router(import_router)