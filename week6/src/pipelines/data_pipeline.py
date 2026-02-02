import os
import pandas as pd
import numpy as np
from scipy import stats

RAW_DATA_PATH = "src/data/raw/customer_subscription_churn_usage_patterns.csv"
PROCESSED_DATA_PATH = "src/data/processed/final.csv"


def load_data(path: str) -> pd.DataFrame:
    print("Loading data...")
    df = pd.read_csv(path)
    print(f"Dataset shape: {df.shape}")
    return df


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    print("Handling missing values...")
    for col in df.columns:
        if df[col].dtype in ["int64", "float64"]:
            df[col] = df[col].fillna(df[col].median())
        else:
            df[col] = df[col].fillna(df[col].mode()[0])
    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    print("Removing duplicates...")
    before = df.shape[0]
    df = df.drop_duplicates()
    after = df.shape[0]
    print(f"Removed {before - after} duplicate rows")
    return df


def handle_outliers(df: pd.DataFrame, z_thresh: float = 3.0) -> pd.DataFrame:
    print("Handling outliers using Z-score...")
    numeric_cols = df.select_dtypes(include=np.number).columns

    for col in numeric_cols:
        z_scores = np.abs(stats.zscore(df[col]))
        df[col] = np.where(z_scores > z_thresh,
                           df[col].median(),
                           df[col])
    return df


def save_processed_data(df: pd.DataFrame, path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    print(f"Processed data saved to {path}")


def run_pipeline():
    df = load_data(RAW_DATA_PATH)
    df = handle_missing_values(df)
    df = remove_duplicates(df)
    df = handle_outliers(df)
    save_processed_data(df, PROCESSED_DATA_PATH)


if __name__ == "__main__":
    run_pipeline()
