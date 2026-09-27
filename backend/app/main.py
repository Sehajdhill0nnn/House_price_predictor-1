import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database.database import init_db
from app.routes import assistant, datasets, history, models, prediction

logging.basicConfig(level=logging.INFO)
app = FastAPI(title="House Price Prediction API", version="1.0.0")

origins = settings.allowed_origins
is_wildcard = "*" in origins or not origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if is_wildcard else origins,
    allow_origin_regex=r"^https:\/\/.*\.vercel\.app$" if not is_wildcard else None,
    allow_credentials=not is_wildcard,
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


@app.get("/", tags=["health"])
def root():
    return {
        "status": "ok",
        "service": "House Price Prediction API",
        "health": "/api/health",
        "docs": "/docs",
    }


@app.get("/api/health", tags=["health"])
def health():
    return {"status": "ok"}
