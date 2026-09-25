from fastapi import APIRouter

from app.services.model_service import model_service

router = APIRouter(prefix="/api/models", tags=["models"])


@router.get("/metrics")
def metrics():
    return model_service.metrics


@router.get("/status")
def model_status():
    return {"ready": model_service.ready, "error": model_service.load_error}
