import streamlit as st
import requests
import uuid

st.set_page_config(page_title="Churn Prediction Dashboard")

st.title("Customer Churn Prediction")

# Input fields
signup_date = st.date_input("Signup Date")
plan_type = st.selectbox("Plan Type", ["Basic", "Premium", "Standard"])
monthly_fee = st.number_input("Monthly Fee", min_value=0.0, value=199.0)
avg_weekly_usage_hours = st.number_input("Avg Weekly Usage Hours", min_value=0.0, value=5.0)
support_tickets = st.number_input("Support Tickets", min_value=0, value=0)
payment_failures = st.number_input("Payment Failures", min_value=0, value=0)
tenure_months = st.number_input("Tenure (months)", min_value=0, value=12)
last_login_days_ago = st.number_input("Last Login Days Ago", min_value=0, value=1)

if st.button("Predict Churn"):
    payload = {
        "signup_date": str(signup_date),
        "plan_type": plan_type,
        "monthly_fee": monthly_fee,
        "avg_weekly_usage_hours": avg_weekly_usage_hours,
        "support_tickets": support_tickets,
        "payment_failures": payment_failures,
        "tenure_months": tenure_months,
        "last_login_days_ago": last_login_days_ago
    }

    try:
        response = requests.post("http://localhost:8000/predict", json=payload)
        data = response.json()
        st.write(f"Churn Probability: {data['churn_probability']:.2f}")
        st.write(f"Churn Prediction: {data['churn_prediction']}")
    except Exception as e:
        st.error(f"Error: {e}")
