import joblib
from pathlib import Path

BASE_DIR = Path.cwd()
MODEL_PATH = BASE_DIR / "src" / "models" / "v1" / "best_model.pkl"

model = joblib.load(MODEL_PATH)
print(type(model))
print(model.feature_names_in_)

