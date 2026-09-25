import shutil
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.config import settings
from app.services.model_service import model_service
from ml.preprocessing import FEATURES, TARGET, load_dataset

router = APIRouter(prefix="/api/datasets", tags=["datasets"])
DATASET_DIR = Path(__file__).resolve().parents[3] / "ml" / "data"
MAX_UPLOAD_BYTES = 25 * 1024 * 1024


@router.get("/schema")
def dataset_schema():
    return {"features": FEATURES, "target": TARGET, "required_columns": FEATURES + [TARGET]}


@router.post("/train", status_code=status.HTTP_202_ACCEPTED)
def upload_and_train(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Upload a CSV file.")
    DATASET_DIR.mkdir(parents=True, exist_ok=True)
    destination = DATASET_DIR / "uploaded_train.csv"
    try:
        with destination.open("wb") as output:
            size = 0
            while chunk := file.file.read(1024 * 1024):
                size += len(chunk)
                if size > MAX_UPLOAD_BYTES:
                    raise HTTPException(status_code=413, detail="CSV file must be smaller than 25 MB.")
                output.write(chunk)
        load_dataset(destination)
    except HTTPException:
        destination.unlink(missing_ok=True)
        raise
    except Exception as exc:
        destination.unlink(missing_ok=True)
        raise HTTPException(status_code=400, detail=f"Dataset validation failed: {exc}") from exc

    try:
        from ml.train_all import train_all
        train_all(destination)
        model_service._load()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Training failed: {exc}") from exc
    return {"status": "trained", "filename": file.filename, "rows": len(load_dataset(destination)), "features": FEATURES}