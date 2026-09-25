from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel


class PredictionValues(BaseModel):
    linear_regression: float
    random_forest: float
    neural_network: float


class PredictionResponse(BaseModel):
    id: Optional[int] = None
    predictions: PredictionValues
    average_prediction: float


class HistoryResponse(PredictionResponse):
    created_at: datetime
    house_features: dict[str, Any]
