from fastapi import FastAPI
from app.api.v1.datasets import router as datasets_router
from app.api.v1.metrics import router as metrics_router
from app.api.v1.anomalies import router as anomalies_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Mercora API", version="0.1.0")

app.include_router(datasets_router, prefix="/api/v1", tags=["datasets"])
app.include_router(metrics_router, prefix="/api/v1", tags=["metrics"])
app.include_router(anomalies_router, prefix="/api/v1", tags=["anomalies"])
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def read_root():
    return {"status": "Mercora API is running"}