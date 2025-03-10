import subprocess
import threading
import sys, os
from fastapi import FastAPI
from redis import Redis
from rq import Queue, SimpleWorker
from contextlib import asynccontextmanager
from loguru import logger

from src.controllers import fetch_router, status_router
from src.config import Config


# Create Redis connection and Queue
redis_conn = Redis.from_url(Config.REDIS_URL)
queue = Queue("financial_jobs", connection=redis_conn)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event that starts and stops RQ worker."""
    logger.info("Starting RQ Worker...")
    worker_process = subprocess.Popen(
        [sys.executable, "-m", "src.worker"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env={**os.environ, "PYTHONPATH": "."},
    )
    logger.info("RQ Worker process started with PID: {}", worker_process.pid)

    # Read the output and error in real time
    def log_worker_output():
        for line in worker_process.stdout:
            logger.info(f"RQ Worker Output: {line.strip()}")
        for line in worker_process.stderr:
            logger.error(f"RQ Worker Error: {line.strip()}")

    threading.Thread(target=log_worker_output, daemon=True).start()

    try:
        yield
    finally:
        logger.info("Shutting down RQ Worker...")
        worker_process.terminate()

app = FastAPI(title="Data Ingestion Service", lifespan=lifespan)
app.include_router(fetch_router)
app.include_router(status_router)

@app.get("/")
async def read_root():
    return {"message": "Data Ingestion Service"}


@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)