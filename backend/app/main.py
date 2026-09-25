import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database.database import init_db
from app.routes import assistant, datasets, history, models, prediction

logging.basicConfig(level=logging.INFO)
app = FastAPI(title="House Price Prediction API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(prediction.router)
app.include_router(history.router)
app.include_router(models.router)
app.include_router(datasets.router)
app.include_router(assistant.router)


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/api/health", tags=["health"])
def health():
    return {"status": "ok"}
