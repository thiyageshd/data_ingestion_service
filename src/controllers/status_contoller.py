from fastapi import APIRouter
from fastapi.responses import JSONResponse
from src.services.background_jobs import BackgroundJobService

status_router = APIRouter()

@status_router.get("/status/{job_id}")
def get_job_status(job_id):
    background_service = BackgroundJobService()
    status = background_service.get_job_status(job_id)
    return JSONResponse(content={"job_id": job_id, "status": status})