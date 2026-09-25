from sqlalchemy.orm import Session

from app.database.models import PredictionHistory
from app.schemas.house import HouseFeatures
from app.services.model_service import model_service
from ml.preprocessing import input_to_frame


def create_prediction(db: Session, house: HouseFeatures) -> PredictionHistory:
    features = house.model_dump()
    predictions = model_service.predict(input_to_frame(features))
    average = sum(predictions.values()) / len(predictions)
    record = PredictionHistory(
        house_features=features,
        linear_prediction=predictions["linear_regression"],
        random_forest_prediction=predictions["random_forest"],
        neural_network_prediction=predictions["neural_network"],
        average_prediction=average,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record
