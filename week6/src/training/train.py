import json
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix
)

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier

from xgboost import XGBClassifier


FEATURE_DIR = "src/features/output"
MODEL_PATH = "src/models/best_model.pkl"
METRICS_PATH = "src/evaluation/metrics.json"

RANDOM_STATE = 42
N_SPLITS = 5


# =========================
# LOAD DATA
# =========================
def load_data():
    X_train = pd.read_csv(f"{FEATURE_DIR}/X_train.csv")
    y_train = pd.read_csv(f"{FEATURE_DIR}/y_train.csv").squeeze()
    return X_train, y_train


# =========================
# DEFINE MODELS (EXERCISE ONLY)
# =========================
def get_models():
    return {
        "LogisticRegression": LogisticRegression(
            max_iter=1000,
            class_weight="balanced",
            random_state=RANDOM_STATE
        ),

        "RandomForest": RandomForestClassifier(
            n_estimators=200,
            max_depth=None,
            class_weight="balanced",
            random_state=RANDOM_STATE
        ),

        "XGBoost": XGBClassifier(
            n_estimators=200,
            learning_rate=0.1,
            max_depth=5,
            subsample=0.8,
            colsample_bytree=0.8,
            eval_metric="logloss",
            random_state=RANDOM_STATE
        ),

        "NeuralNetwork": MLPClassifier(
            hidden_layer_sizes=(64, 32),
            max_iter=500,
            random_state=RANDOM_STATE
        )
    }


# =========================
# EVALUATION
# =========================
def evaluate_model(name, model, X, y, cv):
    y_pred = cross_val_predict(model, X, y, cv=cv, method="predict")
    y_proba = cross_val_predict(model, X, y, cv=cv, method="predict_proba")[:, 1]

    return {
        "accuracy": accuracy_score(y, y_pred),
        "precision": precision_score(y, y_pred),
        "recall": recall_score(y, y_pred),
        "f1": f1_score(y, y_pred),
        "roc_auc": roc_auc_score(y, y_proba)
    }, confusion_matrix(y, y_pred)


# =========================
# TRAINING PIPELINE
# =========================
def run_training():
    X, y = load_data()
    models = get_models()
    cv = StratifiedKFold(n_splits=N_SPLITS, shuffle=True, random_state=RANDOM_STATE)

    metrics = {}
    best_model = None
    best_score = -1
    best_name = None
    best_cm = None

    for name, model in models.items():
        print(f"Training {name}...")
        scores, cm = evaluate_model(name, model, X, y, cv)
        metrics[name] = scores

        if scores["roc_auc"] > best_score:
            best_score = scores["roc_auc"]
            best_model = model
            best_name = name
            best_cm = cm

    # Fit best model on full training data
    best_model.fit(X, y)

    # Save model
    joblib.dump(best_model, MODEL_PATH)

    # Save metrics
    os.makedirs("src/evaluation", exist_ok=True)
    with open(METRICS_PATH, "w") as f:
        json.dump(metrics, f, indent=2)

    # Plot confusion matrix
    plt.figure(figsize=(5, 4))
    plt.imshow(best_cm)
    plt.title(f"Confusion Matrix — {best_name}")
    plt.colorbar()
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.tight_layout()
    plt.show()

    print(f"Best Model: {best_name}")
    print(f"ROC-AUC: {best_score:.4f}")


if __name__ == "__main__":
    import os
    run_training()
