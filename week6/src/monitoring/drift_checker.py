import pandas as pd

REFERENCE_DATA = "src/features/output/X_train.csv"
PREDICTION_LOGS = "prediction_logs.csv"
THRESHOLD = 0.2


def check_drift():
    ref = pd.read_csv(REFERENCE_DATA)
    logs = pd.read_csv(PREDICTION_LOGS)

    drift_report = {}

    for col in ref.columns:
        if col in logs.columns:
            ref_mean = ref[col].mean()
            prod_mean = logs[col].mean()
            drift = abs(ref_mean - prod_mean) / (ref_mean + 1e-6)

            drift_report[col] = drift

    flagged = {k: v for k, v in drift_report.items() if v > THRESHOLD}

    return flagged


if __name__ == "__main__":
    drift = check_drift()
    if drift:
        print("Drift detected:", drift)
    else:
        print("No significant drift detected")
