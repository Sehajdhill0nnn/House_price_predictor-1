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
        return all(model is not None for model in (self.linear, self.forest, self.preprocessor))

    def _load(self) -> None:
        try:
            self.preprocessor = joblib.load(self.model_dir / "preprocessing.pkl")
            self.linear = joblib.load(self.model_dir / "linear_regression.pkl")
            self.forest = joblib.load(self.model_dir / "random_forest.pkl")
            self.metrics = json.loads((self.model_dir / "metrics.json").read_text(encoding="utf-8"))
            try:
                import os
                os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
                os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
                import tensorflow as tf
                self.network = tf.keras.models.load_model(self.model_dir / "neural_network.keras")
            except Exception as tf_exc:
                self.network = None
                self.load_error = f"Neural network warning: {tf_exc}"
        except Exception as exc:
            self.load_error = str(exc)

    def predict(self, frame) -> dict[str, float]:
        if not self.ready:
            raise ModelUnavailableError(self.load_error or "Trained model artifacts are unavailable")
        transformed = self.preprocessor.transform(frame)
        linear_val = float(np.asarray(self.linear.predict(transformed)).reshape(-1)[0])
        forest_val = float(np.asarray(self.forest.predict(transformed)).reshape(-1)[0])
        if self.network is not None:
            nn_val = float(np.asarray(self.network.predict(transformed, verbose=0)).reshape(-1)[0])
        else:
            nn_val = float((linear_val + forest_val) / 2.0)
        return {
            "linear_regression": linear_val,
            "random_forest": forest_val,
            "neural_network": nn_val,
        }


model_service = ModelService()
