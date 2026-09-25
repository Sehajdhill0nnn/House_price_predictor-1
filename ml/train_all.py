"""Train and evaluate Linear Regression, Random Forest, and ANN models."""
from __future__ import annotations

import json
import time
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

try:
    from .preprocessing import FEATURES, TARGET, build_preprocessor, load_dataset
except ImportError:
    from preprocessing import FEATURES, TARGET, build_preprocessor, load_dataset

ROOT = Path(__file__).resolve().parents[1]
MODEL_DIR = ROOT / "backend" / "trained_models"
OUTPUT_DIR = ROOT / "ml" / "outputs"


def metrics(model, x_test, y_test, train_seconds: float, neural_network: bool = False) -> tuple[dict, float]:
    started = time.perf_counter()
    predictions = model.predict(x_test, verbose=0) if neural_network else model.predict(x_test)
    inference_seconds = time.perf_counter() - started
    predictions = np.asarray(predictions).reshape(-1)
    return ({
        "mae": float(mean_absolute_error(y_test, predictions)),
        "mse": float(mean_squared_error(y_test, predictions)),
        "rmse": float(np.sqrt(mean_squared_error(y_test, predictions))),
        "r2": float(r2_score(y_test, predictions)),
        "training_time_seconds": round(train_seconds, 4),
        "prediction_time_seconds": round(inference_seconds / max(len(y_test), 1), 6),
    }, inference_seconds)


def train_all(data_path: str | Path | None = None) -> None:
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    data = load_dataset(data_path)
    x_train, x_test, y_train, y_test = train_test_split(
        data[FEATURES], data[TARGET], test_size=0.2, random_state=42
    )
    preprocessor = build_preprocessor()
    transformed_train = preprocessor.fit_transform(x_train)
    transformed_test = preprocessor.transform(x_test)
    joblib.dump(preprocessor, MODEL_DIR / "preprocessing.pkl")

    results: dict[str, dict] = {}
    importance: list[dict] = []

    linear = LinearRegression()
    started = time.perf_counter()
    linear.fit(transformed_train, y_train)
    results["linear_regression"], _ = metrics(linear, transformed_test, y_test, time.perf_counter() - started)
    joblib.dump(linear, MODEL_DIR / "linear_regression.pkl")

    forest = RandomForestRegressor(
        n_estimators=80, max_depth=None, min_samples_split=2, min_samples_leaf=1,
        max_features=0.8, random_state=42, n_jobs=1,
    )
    started = time.perf_counter()
    forest.fit(transformed_train, y_train)
    results["random_forest"], _ = metrics(forest, transformed_test, y_test, time.perf_counter() - started)
    joblib.dump(forest, MODEL_DIR / "random_forest.pkl")
    names = preprocessor.get_feature_names_out()
    importance = [
        {"feature": name.replace("numerical__", "").replace("categorical__", ""), "importance": float(value)}
        for name, value in sorted(zip(names, forest.feature_importances_), key=lambda pair: pair[1], reverse=True)[:12]
    ]

    import tensorflow as tf
    tf.random.set_seed(42)
    network = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(transformed_train.shape[1],)),
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(64, activation="relu"),
        tf.keras.layers.Dense(32, activation="relu"),
        tf.keras.layers.Dense(1),
    ])
    network.compile(optimizer="adam", loss="mse", metrics=["mae"])
    started = time.perf_counter()
    network.fit(
        transformed_train, y_train, validation_split=0.15, epochs=150, batch_size=32,
        callbacks=[tf.keras.callbacks.EarlyStopping(monitor="val_loss", patience=10, restore_best_weights=True)],
        verbose=0,
    )
    results["neural_network"], _ = metrics(network, transformed_test, y_test, time.perf_counter() - started, neural_network=True)
    network.save(MODEL_DIR / "neural_network.keras")

    payload = {
        "features": FEATURES,
        "target": TARGET,
        "models": results,
        "random_forest_feature_importance": importance,
        "dataset_rows": int(len(data)),
        "test_rows": int(len(y_test)),
    }
    (MODEL_DIR / "metrics.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(pd.DataFrame(results).T.to_string(float_format=lambda value: f"{value:.4f}"))


if __name__ == "__main__":
    train_all()
