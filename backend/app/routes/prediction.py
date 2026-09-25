import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.house import HouseFeatures
from app.schemas.prediction import PredictionResponse, PredictionValues
from app.services.model_service import ModelUnavailableError
from app.services.prediction_service import create_prediction

router = APIRouter(prefix="/api", tags=["predictions"])
logger = logging.getLogger(__name__)


@router.post("/predict", response_model=PredictionResponse, status_code=status.HTTP_201_CREATED)
def predict(house: HouseFeatures, db: Session = Depends(get_db)):
    try:
        record = create_prediction(db, house)
    except ModelUnavailableError as exc:
        raise HTTPException(status_code=503, detail=f"Models are not ready. Run python ml/train_all.py first. ({exc})") from exc
    except Exception as exc:
        db.rollback()
        logger.exception("Prediction failed")
        raise HTTPException(status_code=500, detail="Prediction could not be completed") from exc
    return PredictionResponse(
        id=record.id,
        predictions=PredictionValues(
            linear_regression=record.linear_prediction,
            random_forest=record.random_forest_prediction,
            neural_network=record.neural_network_prediction,
        ),
        average_prediction=record.average_prediction,
    )
