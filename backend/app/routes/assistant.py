from __future__ import annotations

from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel

from app.services.model_service import model_service

router = APIRouter(prefix="/api/assistant", tags=["assistant"])


class AssistantRequest(BaseModel):
    question: str
    predictions: Optional[dict[str, float]] = None


class AssistantResponse(BaseModel):
    answer: str
    suggestions: list[str] = []


def money(value: float) -> str:
    return f"${value:,.0f}"


def answer_question(question: str, predictions: dict[str, float] | None) -> AssistantResponse:
    text = question.lower().strip()
    metrics = model_service.metrics.get("models", {})
    suggestions = [
        "What is this project about?",
        "Explain the preprocessing",
        "How should I present this in a viva?",
        "How do I upload a dataset?",
    ]
    if not text:
        return AssistantResponse(answer="Ask me about the models, metrics, graphs, dataset upload, or your latest prediction.", suggestions=suggestions)
    if any(phrase in text for phrase in ("what is this project", "project objective", "objective", "problem statement", "purpose")):
        return AssistantResponse(answer="This project compares Linear Regression, Random Forest Regression, and a TensorFlow Neural Network for house-price regression. A React dashboard sends validated property details to FastAPI, the saved preprocessing pipeline transforms them, all three models predict, and the results are stored in SQLite history.", suggestions=["Explain the project architecture", "What is the preprocessing?", "How should I present this in a viva?"])
    if any(word in text for word in ("preprocess", "preprocessing", "clean", "missing", "encode", "scale")):
        return AssistantResponse(answer="The pipeline selects 13 numerical and 7 categorical Ames features. Numerical values use median imputation and StandardScaler. Categories use most-frequent imputation and one-hot encoding with unknown categories ignored. The fitted transformer is saved as preprocessing.pkl and reused during API inference, preventing training-serving mismatch.", suggestions=["Why use one-hot encoding?", "Why scale numerical features?", "Explain the dataset features"])
    if any(word in text for word in ("architecture", "backend", "frontend", "full stack", "system design")):
        return AssistantResponse(answer="The flow is React dashboard -> Axios -> FastAPI routes -> prediction service -> persisted preprocessing and model artifacts. SQLAlchemy stores prediction history in SQLite. The model lab reads metrics.json, while the Dataset page uploads a CSV and retrains the models explicitly.", suggestions=["Explain the API endpoints", "Explain the database", "How should I present this in a viva?"])
    if any(word in text for word in ("api", "endpoint", "rest", "fastapi")):
        return AssistantResponse(answer="The main endpoints are GET /api/health, POST /api/predict, GET /api/models/metrics, GET /api/models/status, GET /api/history, DELETE /api/history/{id}, GET /api/datasets/schema, POST /api/datasets/train, and POST /api/assistant/ask. FastAPI and Pydantic validate the request contract before prediction.", suggestions=["Explain input validation", "Explain the database", "How does prediction work?"])
    if any(word in text for word in ("database", "sqlite", "history", "sqlalchemy")):
        return AssistantResponse(answer="SQLite is used for easy local deployment through SQLAlchemy. The prediction_history table stores the timestamp, submitted house features as JSON, each model prediction, and the average prediction. Records can be listed and deleted from the History page.", suggestions=["Explain the API endpoints", "How does prediction work?", "Why use SQLite?"])
    if any(word in text for word in ("validate", "validation", "negative", "invalid", "pydantic")):
        return AssistantResponse(answer="Pydantic checks ranges such as Overall Quality 1-10, positive living area, valid years, and supported categorical values. It also checks that the remodeling year is not earlier than the build year. Invalid requests are rejected before reaching the models.", suggestions=["Explain the preprocessing", "Explain the API endpoints", "What limitations does it have?"])
    if any(word in text for word in ("train", "training", "epoch", "early stopping", "overfit")):
        return AssistantResponse(answer="Training uses a reproducible 80/20 train-test split. Linear Regression is the baseline, Random Forest uses 80 trees, and the ANN uses Dense 128, Dropout, Dense 64, Dense 32, and a regression output. The ANN uses validation data and EarlyStopping to reduce overfitting. Training happens only in the training script or explicit dataset-upload workflow, never during prediction requests.", suggestions=["Explain the Neural Network", "How do I upload a dataset?", "What is training time?"])
    if any(word in text for word in ("limitations", "weakness", "future", "improve", "bias")):
        return AssistantResponse(answer="Important limitations are the geographic and historical scope of the Ames data, possible dataset bias, no uncertainty interval, and dependence on the selected features. Future improvements could add cross-validation, uncertainty estimates, authentication, PostgreSQL, model versioning, and explainability methods such as SHAP.", suggestions=["What is this project about?", "Compare all models", "How should I present this in a viva?"])
    if any(word in text for word in ("viva", "presentation", "teacher", "report", "explain simply")):
        return AssistantResponse(answer="A clear viva sequence is: state the house-price problem, explain the selected dataset features, show the shared preprocessing pipeline, compare the three model families, demonstrate one live prediction, then discuss MAE, RMSE, R², training time, limitations, and future scope. Emphasize that this is regression, so accuracy is not used.", suggestions=["Give me a short abstract", "Explain the project architecture", "Why not use accuracy?"])
    if "abstract" in text:
        return AssistantResponse(answer="This project presents a full-stack house-price prediction system that compares Linear Regression, Random Forest Regression, and a TensorFlow Neural Network. A shared preprocessing pipeline transforms numerical and categorical property features, while FastAPI serves predictions and SQLite stores history. The dashboard reports real regression metrics and visualizes differences between traditional machine learning and deep learning.", suggestions=["How should I present this in a viva?", "What are the objectives?", "Explain the preprocessing"])
    if predictions and any(word in text for word in ("prediction", "price", "estimate", "result")):
        names = {"linear_regression": "Linear Regression", "random_forest": "Random Forest", "neural_network": "Neural Network"}
        ordered = sorted(predictions.items(), key=lambda item: item[1])
        average = sum(predictions.values()) / len(predictions)
        details = ", ".join(f"{names.get(name, name)}: {money(value)}" for name, value in ordered)
        return AssistantResponse(answer=f"For the latest property, the model estimates are {details}. Their simple average is {money(average)}. The spread shows how differently each model interprets the same property features.", suggestions=["Why are the predictions different?", "Explain Random Forest", "What does the average mean?"])
    if any(word in text for word in ("best", "accurate", "winner")):
        if not metrics:
            return AssistantResponse(answer="Metrics are not loaded yet. Open Model Lab after training finishes.", suggestions=suggestions)
        best = min(metrics.items(), key=lambda item: item[1].get("rmse", float("inf")))
        label = {"linear_regression": "Linear Regression", "random_forest": "Random Forest", "neural_network": "Neural Network"}.get(best[0], best[0])
        return AssistantResponse(answer=f"On the saved holdout test, {label} has the lowest RMSE at {best[1]['rmse']:,.0f}. Treat that as the strongest measured result for this dataset, not a universal winner for every property.", suggestions=["Compare all R² values", "What is RMSE?", "Explain the three models"])
    if "linear" in text:
        return AssistantResponse(answer="Linear Regression is the baseline model. It estimates SalePrice from a weighted combination of the transformed numerical and categorical features. It is fast and easy to explain, but it may miss nonlinear relationships.", suggestions=["Explain Random Forest", "Explain Neural Network", "Compare model metrics"])
    if "forest" in text or "tree" in text:
        return AssistantResponse(answer="Random Forest combines many decision trees. Each tree learns nonlinear feature interactions, and the ensemble averages their outputs. Its feature-importance chart shows which transformed inputs influenced the forest most.", suggestions=["What is feature importance?", "Compare model metrics", "Why are predictions different?"])
    if "neural" in text or "ann" in text or "deep" in text or "tensorflow" in text:
        return AssistantResponse(answer="The Neural Network is a feed-forward TensorFlow model with Dense 128, Dropout, Dense 64, Dense 32, and a single regression output. It uses Adam, MSE loss, MAE monitoring, validation data, and early stopping.", suggestions=["Explain Linear Regression", "Explain Random Forest", "What is early stopping?"])
    if "graph" in text or "chart" in text:
        return AssistantResponse(answer="The Model Lab graphs compare MAE, RMSE, R², training time, prediction time, and Random Forest feature importance. The prediction screen also has bar, line, and area views for the latest three-model estimate.", suggestions=["What does R² mean?", "Which model is best?", "Explain feature importance"])
    if "upload" in text or "dataset" in text or "csv" in text:
        return AssistantResponse(answer="Open Dataset in the sidebar and upload a CSV containing the required selected features plus SalePrice. The backend validates the columns, retrains all three models, saves new artifacts, and reloads them for future predictions.", suggestions=["What columns are required?", "How long does training take?", "Make a prediction"])
    if "metric" in text or "mae" in text or "rmse" in text or "r2" in text or "accuracy" in text:
        return AssistantResponse(answer="This is a regression project, so accuracy is not used. MAE is average absolute error, RMSE penalizes larger errors more strongly, and R² measures explained variance. Lower MAE/RMSE and higher R² are generally better.", suggestions=["Which model is best?", "Explain the graphs", "What is training time?"])
    return AssistantResponse(answer="I can explain Linear Regression, Random Forest, the TensorFlow Neural Network, evaluation metrics, graphs, CSV dataset upload, and the latest prediction. Try asking one of those questions.", suggestions=suggestions)


@router.post("/ask", response_model=AssistantResponse)
def ask(request: AssistantRequest):
    return answer_question(request.question, request.predictions)
