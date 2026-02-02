import os
import json
import joblib
import optuna
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score


FEATURE_DIR = "src/features/output"
MODEL_PATH = "src/models/best_model.pkl"
RESULTS_DIR = "src/tuning"
RESULTS_PATH = f"{RESULTS_DIR}/results.json"

RANDOM_STATE = 42
N_TRIALS = 50   # good balance for review + speed


# =========================
# LOAD DATA
# =========================
def load_data():
    X_train = pd.read_csv(f"{FEATURE_DIR}/X_train.csv")
    y_train = pd.read_csv(f"{FEATURE_DIR}/y_train.csv").squeeze()
    return X_train, y_train


# =========================
# OPTUNA OBJECTIVE
# =========================
def objective(trial):
    X, y = load_data()

    C = trial.suggest_float("C", 1e-3, 10.0, log=True)
    penalty = trial.suggest_categorical("penalty", ["l1", "l2"])
    class_weight = trial.suggest_categorical("class_weight", [None, "balanced"])

    model = LogisticRegression(
        C=C,
        penalty=penalty,
        solver="liblinear",   # supports both l1 & l2
        class_weight=class_weight,
        max_iter=2000,
        random_state=RANDOM_STATE
    )

    cv = StratifiedKFold(
        n_splits=5,
        shuffle=True,
        random_state=RANDOM_STATE
    )

    score = cross_val_score(
        model,
        X,
        y,
        cv=cv,
        scoring="roc_auc",
        n_jobs=-1
    ).mean()

    return score


# =========================
# RUN OPTUNA
# =========================
def run_tuning():
    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=N_TRIALS)

    best_params = study.best_params
    best_score = study.best_value

    # Train final model on full training data
    X, y = load_data()

    best_model = LogisticRegression(
        **best_params,
        solver="liblinear",
        max_iter=2000,
        random_state=RANDOM_STATE
    )

    best_model.fit(X, y)

    # Ensure directories exist
    os.makedirs("src/models", exist_ok=True)
    os.makedirs(RESULTS_DIR, exist_ok=True)

    # Save model
    joblib.dump(best_model, MODEL_PATH)

    # Save tuning results
    results = {
        "model": "LogisticRegression",
        "optimization": "Optuna (Bayesian)",
        "best_score": best_score,
        "best_params": best_params,
        "n_trials": N_TRIALS
    }

    with open(RESULTS_PATH, "w") as f:
        json.dump(results, f, indent=2)

    print("Optuna tuning completed")
    print("Best ROC-AUC:", best_score)
    print("Best Params:", best_params)


if __name__ == "__main__":
    run_tuning()
