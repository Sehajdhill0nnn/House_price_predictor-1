# House Price Prediction: A Comparative Study of Machine Learning and Deep Learning

A full-stack university project that compares Linear Regression, Random Forest Regression, and a TensorFlow/Keras feed-forward ANN on selected features from the Ames Housing dataset. The same persisted preprocessing pipeline is used during training and API inference.

## Features

- Data cleaning, imputation, one-hot encoding, and numerical scaling
- Three regression models with real holdout metrics
- FastAPI REST API with Pydantic validation
- SQLite prediction history through SQLAlchemy
- React/Vite dashboard with charts and model comparison
- Random Forest permutation feature importance
- EDA plot generation for a project report
- Docker Compose support for backend and frontend

XGBoost and external AI prediction APIs are intentionally not used.

## Stack

Python 3.11+, Pandas, NumPy, scikit-learn, Joblib, TensorFlow/Keras, FastAPI, Uvicorn, Pydantic, SQLAlchemy, SQLite, React, Vite, Axios, Recharts, and Lucide React.

## Dataset setup

Download the Kaggle Ames Housing `train.csv` and place it at `ml/data/train.csv`. The repository also includes a convenience downloader for a public Ames-compatible mirror:

```bash
python ml/download_data.py
```

For a formal submission, cite the original Kaggle dataset: *House Prices: Advanced Regression Techniques*, Kaggle, https://www.kaggle.com/competitions/house-prices-advanced-regression-techniques.

## Local installation

Use Python 3.11 or newer. The current machine's system Python is 3.9, so install/select a 3.11 interpreter before training.

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r ml/requirements.txt
python -m pip install -r backend/requirements.txt
cd frontend && npm install && cd ..
```

## Train the models

From the repository root:

```bash
python ml/train_all.py
```

This saves `linear_regression.pkl`, `random_forest.pkl`, `preprocessing.pkl`, `neural_network.keras`, and real evaluation values in `backend/trained_models/`. Training is never performed by the API.

Generate report plots with:

```bash
python ml/eda.py
```

Plots and missing-value analysis are written to `ml/outputs/`.

## Run the application

Terminal 1, from the repository root:

```bash
source .venv/bin/activate
cd backend
PYTHONPATH=.. uvicorn app.main:app --reload --port 8000
```

Terminal 2:

```bash
cd frontend
npm run dev
```

Open http://localhost:5173. API documentation is available at http://localhost:8000/docs.

Create `.env` from `.env.example` to customize `DATABASE_URL`, `CORS_ORIGINS`, or `MODEL_DIR`. SQLite is the default; switching to PostgreSQL only requires a SQLAlchemy-compatible database URL and its driver.

## REST API

- `GET /api/health` returns service status.
- `POST /api/predict` validates a house profile, predicts with all three loaded models, and stores the result.
- `GET /api/models/metrics` returns the saved holdout metrics and Random Forest importance.
- `GET /api/models/status` reports whether artifacts are loaded.
- `GET /api/history` returns the latest 100 saved predictions.
- `DELETE /api/history/{id}` deletes one saved prediction.

Example request:

```json
{
  "overall_qual": 7,
  "gr_liv_area": 1800,
  "garage_cars": 2,
  "garage_area": 500,
  "total_bsmt_sf": 900,
  "first_flr_sf": 1000,
  "second_flr_sf": 800,
  "full_bath": 2,
  "bedroom_abv_gr": 3,
  "tot_rms_abv_grd": 7,
  "year_built": 2005,
  "year_remod_add": 2010,
  "lot_area": 9000,
  "neighborhood": "NAmes",
  "kitchen_qual": "Gd",
  "exter_qual": "Gd",
  "bsmt_qual": "Gd",
  "garage_type": "Attchd",
  "heating": "GasA",
  "central_air": "Y"
}
```

## Project structure

```text
ml/                     training, preprocessing, EDA, and dataset setup
backend/app/            FastAPI routes, services, schemas, and database
backend/trained_models/ generated model artifacts and metrics
frontend/src/           React dashboard components and pages
docs/                   university report outline
```

## Methodology

The selected numerical fields are median-imputed and standardized. Categorical fields are mode-imputed and one-hot encoded with unknown categories ignored by the transformer. Linear Regression uses the transformed matrix directly. Random Forest uses a tuned, reproducible configuration with 300 trees. The ANN uses Dense(128)-Dropout(0.2)-Dense(64)-Dense(32)-Dense(1), Adam, MSE loss, MAE monitoring, validation split, and EarlyStopping.

Evaluation uses MAE, MSE, RMSE, R², training time, and per-row inference time on a fixed 20% holdout split. Values shown in the dashboard are loaded from `metrics.json`; none are hardcoded.

## Docker

With Docker installed:

```bash
docker compose up --build
```

The frontend is served at http://localhost:5173 and the API at http://localhost:8000. Train artifacts must be generated before prediction; mount or copy them into `backend/trained_models/`.

## University report outline

See [docs/report_outline.md](docs/report_outline.md) for sections covering the abstract, literature review, preprocessing, model methodology, architecture, database, experiments, results, limitations, and future scope. Add screenshots from the running dashboard and the generated EDA plots to the final submission.

## Future improvements

Cross-validation, calibrated uncertainty intervals, SHAP-based explanation, PostgreSQL deployment, authentication, model versioning, and automated CI/CD can be added without changing the prediction API contract.
