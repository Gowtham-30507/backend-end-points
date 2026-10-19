from fastapi import FastAPI

from app.routers.adr_reports import router as adr_reports_router
from app.routers.dashboards import router as dashboards_router
from app.routers.doctors import router as doctors_router
from app.routers.feedback import router as feedback_router
from app.routers.journals import router as journals_router
from app.routers.library import router as library_router
from app.routers.manufacturers import router as manufacturers_router
from app.routers.products import router as products_router
from app.routers.referrals import router as referrals_router
from app.routers.research_submissions import router as research_submissions_router

app = FastAPI()
app.include_router(adr_reports_router)
app.include_router(dashboards_router)
app.include_router(manufacturers_router)
app.include_router(doctors_router)
app.include_router(products_router)
app.include_router(library_router)
app.include_router(journals_router)
app.include_router(research_submissions_router)
app.include_router(feedback_router)
app.include_router(referrals_router)


@app.get("/health")
async def health():
    return {"status": "ok"}
