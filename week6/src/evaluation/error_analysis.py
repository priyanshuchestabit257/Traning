import joblib
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix


FEATURE_DIR = "src/features/output"
MODEL_PATH = "src/models/best_model.pkl"


def run_error_analysis():
    X_test = pd.read_csv(f"{FEATURE_DIR}/X_test.csv")
    y_test = pd.read_csv(f"{FEATURE_DIR}/y_test.csv").squeeze()

    model = joblib.load(MODEL_PATH)

    y_pred = model.predict(X_test)

    cm = confusion_matrix(y_test, y_pred)

    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
    plt.title("Error Analysis – Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.show()

    print("Error analysis completed")


if __name__ == "__main__":
    run_error_analysis()
