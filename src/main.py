from fastapi import FastAPI
from src.controllers import fetch_router, status_router
app = FastAPI()

app = FastAPI(title="Data Ingestion Service")
app.include_router(fetch_router)
app.include_router(status_router)


@app.get("/")
def read_root():
    return {"message": "Data Ingestion Service"}


@app.get("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)