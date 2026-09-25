from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import PredictionHistory
from app.schemas.prediction import HistoryResponse, PredictionResponse, PredictionValues

router = APIRouter(prefix="/api/history", tags=["history"])


def serialize(record: PredictionHistory) -> HistoryResponse:
    return HistoryResponse(
        id=record.id,
        created_at=record.created_at,
        house_features=record.house_features,
        predictions=PredictionValues(
            linear_regression=record.linear_prediction,
            random_forest=record.random_forest_prediction,
            neural_network=record.neural_network_prediction,
        ),
        average_prediction=record.average_prediction,
    )


@router.get("", response_model=list[HistoryResponse])
def history(db: Session = Depends(get_db)):
    records = db.query(PredictionHistory).order_by(PredictionHistory.created_at.desc()).limit(100).all()
    return [serialize(record) for record in records]


@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_history(record_id: int, db: Session = Depends(get_db)):
    record = db.get(PredictionHistory, record_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Prediction history record not found")
    db.delete(record)
    db.commit()
