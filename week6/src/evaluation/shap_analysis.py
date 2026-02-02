import joblib
import shap
import pandas as pd
import matplotlib.pyplot as plt


FEATURE_DIR = "src/features/output"
MODEL_PATH = "src/models/best_model.pkl"


def load_artifacts():
    X_train = pd.read_csv(f"{FEATURE_DIR}/X_train.csv")
    model = joblib.load(MODEL_PATH)
    return X_train, model


def run_shap():
    X, model = load_artifacts()

    explainer = shap.Explainer(model, X)
    shap_values = explainer(X)

    shap.summary_plot(shap_values, X, show=False)
    plt.tight_layout()
    plt.show()

    print("SHAP summary plot generated")


if __name__ == "__main__":
    run_shap()
