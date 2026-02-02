import os
import json
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline


DATA_PATH = "src/data/processed/final.csv"
FEATURE_DIR = "src/features/output"
FEATURE_LIST_PATH = "src/features/feature_list.json"

TARGET_COLUMN = "churn"
TEST_SIZE = 0.2
RANDOM_STATE = 42


def load_data():
    df = pd.read_csv(DATA_PATH)
    return df


def create_features(df):
    df = df.copy()

    # --- Target encoding (only label, not leakage) ---
    df[TARGET_COLUMN] = df[TARGET_COLUMN].map({"Yes": 1, "No": 0})

    # --- Date features ---
    df["signup_date"] = pd.to_datetime(df["signup_date"])
    df["signup_year"] = df["signup_date"].dt.year
    df["signup_month"] = df["signup_date"].dt.month
    df.drop(columns=["signup_date"], inplace=True)

    # --- Usage behavior ---
    df["low_usage_flag"] = (df["avg_weekly_usage_hours"] < 5).astype(int)
    df["inactive_flag"] = (df["last_login_days_ago"] > 30).astype(int)

    # --- Financial stress ---
    df["payment_issue_flag"] = (df["payment_failures"] > 0).astype(int)
    df["fee_per_usage_hour"] = df["monthly_fee"] / (df["avg_weekly_usage_hours"] + 1)

    # --- Support friction ---
    df["high_support_flag"] = (df["support_tickets"] >= 5).astype(int)
    df["tickets_per_tenure"] = df["support_tickets"] / (df["tenure_months"] + 1)

    # --- Tenure mismatch ---
    df["usage_per_tenure"] = df["avg_weekly_usage_hours"] / (df["tenure_months"] + 1)

    return df


def split_data(df):
    X = df.drop(columns=[TARGET_COLUMN, "user_id"])
    y = df[TARGET_COLUMN]

    return train_test_split(
        X, y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y
    )


def build_preprocessor(X):
    num_cols = X.select_dtypes(include=np.number).columns.tolist()
    cat_cols = X.select_dtypes(exclude=np.number).columns.tolist()

    num_pipeline = Pipeline([
        ("scaler", StandardScaler())
    ])

    cat_pipeline = Pipeline([
        ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    ])

    preprocessor = ColumnTransformer([
        ("num", num_pipeline, num_cols),
        ("cat", cat_pipeline, cat_cols)
    ])

    return preprocessor, num_cols, cat_cols


def save_outputs(X_train, X_test, y_train, y_test, feature_names):
    os.makedirs(FEATURE_DIR, exist_ok=True)

    X_train.to_csv(f"{FEATURE_DIR}/X_train.csv", index=False)
    X_test.to_csv(f"{FEATURE_DIR}/X_test.csv", index=False)
    y_train.to_csv(f"{FEATURE_DIR}/y_train.csv", index=False)
    y_test.to_csv(f"{FEATURE_DIR}/y_test.csv", index=False)

    with open(FEATURE_LIST_PATH, "w") as f:
        json.dump(feature_names, f, indent=2)


def run_pipeline():
    df = load_data()
    df = create_features(df)

    X_train, X_test, y_train, y_test = split_data(df)

    preprocessor, num_cols, cat_cols = build_preprocessor(X_train)

    X_train_t = preprocessor.fit_transform(X_train)
    X_test_t = preprocessor.transform(X_test)

    feature_names = (
        num_cols +
        list(
            preprocessor.named_transformers_["cat"]
            .named_steps["encoder"]
            .get_feature_names_out(cat_cols)
        )
    )

    X_train_df = pd.DataFrame(X_train_t, columns=feature_names)
    X_test_df = pd.DataFrame(X_test_t, columns=feature_names)

    save_outputs(X_train_df, X_test_df, y_train, y_test, feature_names)

    print("✅ Day 2 completed with dataset-specific features")
    print(f"Total features: {len(feature_names)}")


if __name__ == "__main__":
    run_pipeline()
