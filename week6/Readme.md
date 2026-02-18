# Week 6 – ML Deployment & Monitoring (Churn Prediction)

## 📌 Overview
This project builds, tunes, and deploys a Customer Churn Prediction model as a production-ready API.

It includes:
- Feature Engineering
- Model Training
- Hyperparameter Tuning (Optuna)
- Model Evaluation
- API Deployment (FastAPI)
- Prediction Logging
- Drift Monitoring
- Optional Streamlit Dashboard
- Docker Support

---

##  Project Structure

week6/
│
├── src/
│ ├── training/
│ ├── models/
│ │ └── v1/
│ ├── deployment/
│ │ └── api.py
│ └── monitoring/
│ └── drift_checker.py
│
├── prediction_logs.csv
├── Dockerfile
├── requirements.txt
└── README.md


---



### 1️⃣ Install dependencies
pip install -r requirements.txt


### 2️⃣ Run API
uvicorn src.deployment.api:app --reload
Open:
http://127.0.0.1:8000/docs

## Run streamlit
streamlit run src/deployment/dashboard.py

