from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, JSON, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base


class PredictionHistory(Base):
    __tablename__ = "prediction_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    house_features: Mapped[dict] = mapped_column(JSON, nullable=False)
    linear_prediction: Mapped[float] = mapped_column(Float, nullable=False)
    random_forest_prediction: Mapped[float] = mapped_column(Float, nullable=False)
    neural_network_prediction: Mapped[float] = mapped_column(Float, nullable=False)
    average_prediction: Mapped[float] = mapped_column(Float, nullable=False)
