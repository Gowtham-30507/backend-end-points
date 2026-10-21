from fastapi import FastAPI

from functions.dashboards import router as dashboards_router
from functions.journal_ingestion import router as journal_ingestion_router
from databases.adr_reports import router as adr_reports_router
from databases.doctors import router as doctors_router
from databases.feedback import router as feedback_router
from databases.journals import router as journals_router
from databases.library import router as library_router
from databases.manufacturers import router as manufacturers_router
from databases.products import router as products_router
from databases.referrals import router as referrals_router
from databases.research_submissions import router as research_submissions_router
from app.routers.auth import router as auth_router

from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from database.session import check_db_connection

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router)
app.include_router(adr_reports_router)
app.include_router(dashboards_router)
app.include_router(manufacturers_router)
app.include_router(doctors_router)
app.include_router(products_router)
app.include_router(library_router)
app.include_router(journals_router)
app.include_router(journal_ingestion_router)
app.include_router(research_submissions_router)
app.include_router(feedback_router)
app.include_router(referrals_router)


@app.get("/health")
async def health():
    db_status = check_db_connection()
    return {"status": "ok", "database": db_status}
