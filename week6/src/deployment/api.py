import os
import csv
import uuid
import joblib
import pandas as pd
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_VERSION = os.getenv("MODEL_VERSION", "v1")
MODEL_PATH = BASE_DIR / "models" / MODEL_VERSION / "best_model.pkl"
LOG_PATH = BASE_DIR / "prediction_logs.csv"


app = FastAPI(title="Churn Prediction API")

class PredictionInput(BaseModel):
    signup_date: str = Field(..., example="2023-12-11")
    plan_type: str = Field(..., example="Basic")  # Basic / Premium / Standard
    monthly_fee: float = Field(..., gt=0)
    avg_weekly_usage_hours: float = Field(..., ge=0)
    support_tickets: int = Field(..., ge=0)
    payment_failures: int = Field(..., ge=0)
    tenure_months: int = Field(..., ge=0)
    last_login_days_ago: int = Field(..., ge=0)


def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model not found at {MODEL_PATH}")
    return joblib.load(MODEL_PATH)
    

model = load_model()
if not hasattr(model, "multi_class"):
    model.multi_class = "auto"

def log_prediction(request_id, features, prob, prediction):
    file_exists = LOG_PATH.exists()

    with open(LOG_PATH, "a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow([
                "timestamp",
                "request_id",
                *features.keys(),
                "churn_probability",
                "churn_prediction"
            ])

        writer.writerow([
            datetime.utcnow().isoformat(),
            request_id,
            *features.values(),
            prob,
            prediction
        ])


def prepare_features(data: PredictionInput) -> pd.DataFrame:
    df = pd.DataFrame([data.dict()])

    # ---- date features
    signup_dt = pd.to_datetime(df["signup_date"])
    df["signup_year"] = signup_dt.dt.year
    df["signup_month"] = signup_dt.dt.month

    # ---- flags
    df["low_usage_flag"] = (df["avg_weekly_usage_hours"] < 5).astype(int)
    df["inactive_flag"] = (df["last_login_days_ago"] > 30).astype(int)
    df["payment_issue_flag"] = (df["payment_failures"] > 0).astype(int)
    df["high_support_flag"] = (df["support_tickets"] >= 5).astype(int)

    # ---- ratios
    df["tickets_per_tenure"] = df["support_tickets"] / (df["tenure_months"] + 1e-6)
    df["usage_per_tenure"] = df["avg_weekly_usage_hours"] / (df["tenure_months"] + 1e-6)
    df["fee_per_usage_hour"] = df["monthly_fee"] / (df["avg_weekly_usage_hours"] + 1e-6)

    # ---- one-hot encoding (MATCH TRAINING)
    df["plan_type_Basic"] = (df["plan_type"] == "Basic").astype(int)
    df["plan_type_Premium"] = (df["plan_type"] == "Premium").astype(int)
    df["plan_type_Standard"] = (df["plan_type"] == "Standard").astype(int)

    # ---- EXACT FEATURE ORDER USED DURING TRAINING
    final_features = [
        "monthly_fee",
        "avg_weekly_usage_hours",
        "support_tickets",
        "payment_failures",
        "tenure_months",
        "last_login_days_ago",
        "signup_year",
        "signup_month",
        "low_usage_flag",
        "inactive_flag",
        "payment_issue_flag",
        "fee_per_usage_hour",
        "high_support_flag",
        "tickets_per_tenure",
        "usage_per_tenure",
        "plan_type_Basic",
        "plan_type_Premium",
        "plan_type_Standard",
    ]

    return df[final_features]


@app.post("/predict")
def predict(data: PredictionInput):
    try:
        request_id = str(uuid.uuid4())

        X = prepare_features(data)

        prob = model.predict_proba(X)[0][1]
        prediction = int(prob >= 0.5)

        log_prediction(request_id, data.dict(), prob, prediction)

        return {
            "request_id": request_id,
            "model_version": MODEL_VERSION,
            "churn_probability": float(prob),
            "churn_prediction": prediction
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
