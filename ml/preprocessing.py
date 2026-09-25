"""Shared dataset and preprocessing definitions for training and inference."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.datasets import fetch_openml
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

NUMERICAL_FEATURES = [
    "OverallQual", "GrLivArea", "GarageCars", "GarageArea", "TotalBsmtSF",
    "1stFlrSF", "2ndFlrSF", "FullBath", "BedroomAbvGr", "TotRmsAbvGrd",
    "YearBuilt", "YearRemodAdd", "LotArea",
]
CATEGORICAL_FEATURES = ["Neighborhood", "KitchenQual", "ExterQual", "BsmtQual", "GarageType", "Heating", "CentralAir"]
FEATURES = NUMERICAL_FEATURES + CATEGORICAL_FEATURES
TARGET = "SalePrice"

INPUT_TO_DATASET = {
    "overall_qual": "OverallQual", "gr_liv_area": "GrLivArea", "garage_cars": "GarageCars",
    "garage_area": "GarageArea", "total_bsmt_sf": "TotalBsmtSF", "first_flr_sf": "1stFlrSF",
    "second_flr_sf": "2ndFlrSF", "full_bath": "FullBath", "bedroom_abv_gr": "BedroomAbvGr",
    "tot_rms_abv_grd": "TotRmsAbvGrd", "year_built": "YearBuilt", "year_remod_add": "YearRemodAdd",
    "lot_area": "LotArea", "neighborhood": "Neighborhood", "kitchen_qual": "KitchenQual",
    "exter_qual": "ExterQual", "bsmt_qual": "BsmtQual", "garage_type": "GarageType",
    "heating": "Heating", "central_air": "CentralAir",
}


def load_dataset(path: str | Path | None = None) -> pd.DataFrame:
    """Load a local Ames train.csv, falling back to the OpenML house_prices dataset."""
    local_path = Path(path) if path else Path(__file__).parent / "data" / "train.csv"
    if local_path.exists():
        frame = pd.read_csv(local_path)
    else:
        try:
            frame = fetch_openml(name="house_prices", as_frame=True, parser="auto").frame
        except Exception as exc:
            raise FileNotFoundError(
                "Place the Kaggle Ames train.csv at ml/data/train.csv, or allow network access for dataset download."
            ) from exc
    missing = [column for column in FEATURES + [TARGET] if column not in frame.columns]
    if missing:
        raise ValueError(f"Dataset is missing required columns: {', '.join(missing)}")
    frame = frame[FEATURES + [TARGET]].copy()
    frame = frame.dropna(subset=[TARGET])
    if frame.empty:
        raise ValueError("Dataset has no rows with a valid SalePrice target.")
    return frame


def build_preprocessor() -> ColumnTransformer:
    numerical = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])
    categorical = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ])
    return ColumnTransformer([
        ("numerical", numerical, NUMERICAL_FEATURES),
        ("categorical", categorical, CATEGORICAL_FEATURES),
    ])


def input_to_frame(payload: dict[str, Any]) -> pd.DataFrame:
    values = {INPUT_TO_DATASET[key]: value for key, value in payload.items()}
    return pd.DataFrame([values], columns=FEATURES)
