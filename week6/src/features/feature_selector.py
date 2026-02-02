import json
import pandas as pd
from sklearn.feature_selection import mutual_info_classif


FEATURE_DIR = "src/features/output"
FEATURE_LIST_PATH = "src/features/feature_list.json"
TOP_K = 10


def load_features():
    X_train = pd.read_csv(f"{FEATURE_DIR}/X_train.csv")
    y_train = pd.read_csv(f"{FEATURE_DIR}/y_train.csv").squeeze()
    return X_train, y_train


def select_features(X, y):
    mi_scores = mutual_info_classif(X, y, random_state=42)
    mi_df = pd.DataFrame({
        "feature": X.columns,
        "mi_score": mi_scores
    }).sort_values("mi_score", ascending=False)

    return mi_df.head(TOP_K)["feature"].tolist()


def save_selected_features(features):
    with open(FEATURE_LIST_PATH, "w") as f:
        json.dump(features, f, indent=2)


def run_feature_selection():
    X_train, y_train = load_features()
    selected_features = select_features(X_train, y_train)
    save_selected_features(selected_features)

    print("Feature selection completed")
    print(f"Selected features: {len(selected_features)}")


if __name__ == "__main__":
    run_feature_selection()
