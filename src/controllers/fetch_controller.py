from fastapi import APIRouter
from fastapi.responses import JSONResponse
from src.services.yahoo_finance import YahooFinanceService
from src.services.background_jobs import BackgroundJobService

fetch_router = APIRouter()

@fetch_router.post("/fetch/company/{symbol}")
def fetch_company_data(symbol):
    yahoo_service = YahooFinanceService()
    background_service = BackgroundJobService()

    job_id = background_service.schedule_fetching_job(symbol)

    return JSONResponse(status_code=202, content={"job_id": job_id, "status": "processing"})