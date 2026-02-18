# API Documentation – Week 6

Base URL:
http://127.0.0.1:8000

---

## Endpoints


### POST /predict

Accepts JSON body.

Returns churn probability and prediction.

---

## Validation

Uses Pydantic for:
- Type validation
- Required fields
- Data constraints

---

## Example cURL
curl -X POST http://127.0.0.1:8000/predict

-H "Content-Type: application/json"
-d '{...}'

## To Run 
uvicorn src.deployment.api:app --reload

## for streamlit
streamlit run src/deployment/dashboard.py

