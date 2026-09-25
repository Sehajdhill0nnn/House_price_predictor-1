from __future__ import annotations

import json
from pathlib import Path

import joblib
import numpy as np

from app.config import settings


class ModelUnavailableError(RuntimeError):
    pass


class ModelService:
    def __init__(self, model_dir: Path | None = None):
        self.model_dir = model_dir or settings.model_path
        self.linear = None
        self.forest = None
        self.preprocessor = None
        self.network = None
        self.metrics: dict = {}
        self.load_error: str | None = None
        self._load()

    @property
    def ready(self) -> bool:
        return all(model is not None for model in (self.linear, self.forest, self.preprocessor, self.network))

    def _load(self) -> None:
        try:
            self.preprocessor = joblib.load(self.model_dir / "preprocessing.pkl")
            self.linear = joblib.load(self.model_dir / "linear_regression.pkl")
            self.forest = joblib.load(self.model_dir / "random_forest.pkl")
            import tensorflow as tf
            self.network = tf.keras.models.load_model(self.model_dir / "neural_network.keras")
            self.metrics = json.loads((self.model_dir / "metrics.json").read_text(encoding="utf-8"))
        except Exception as exc:
            self.load_error = str(exc)

    def predict(self, frame) -> dict[str, float]:
        if not self.ready:
            raise ModelUnavailableError(self.load_error or "Trained model artifacts are unavailable")
        transformed = self.preprocessor.transform(frame)
        values = {
            "linear_regression": float(np.asarray(self.linear.predict(transformed)).reshape(-1)[0]),
            "random_forest": float(np.asarray(self.forest.predict(transformed)).reshape(-1)[0]),
            "neural_network": float(np.asarray(self.network.predict(transformed, verbose=0)).reshape(-1)[0]),
        }
        return values


model_service = ModelService()
