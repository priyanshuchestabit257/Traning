# Feature Engineering – Customer Churn Model

## 📌 Overview

Feature engineering transforms raw customer data into meaningful inputs that improve model performance.

In this project, engineered features were created to better capture:
- Customer behavior
- Payment reliability
- Engagement level
- Subscription patterns

---

## 🧾 Raw Input Features

The original dataset included:

- signup_date
- plan_type
- monthly_fee
- avg_weekly_usage_hours
- support_tickets
- payment_failures
- tenure_months
- last_login_days_ago

---

## 🔧 Engineered Features

### 1️⃣ Date-Based Features

From `signup_date`:

- `signup_year`
- `signup_month`

Purpose:
Capture seasonal patterns and customer cohort behavior.


#### low_usage_flag
low_usage_flag = 1 if avg_weekly_usage_hours < threshold else 0

Purpose:
Measure engagement growth or decline over time.

---

### 4️Plan Type Encoding

Categorical variable `plan_type` was one-hot encoded into:

- plan_type_Basic
- plan_type_Premium
- plan_type_Standard

Purpose:
Allow the model to differentiate plan behavior patterns.

---

##  Final Feature Set Used by Model

The trained model expects the following features:

- monthly_fee
- payment_failures
- signup_year
- signup_month
- low_usage_flag
- payment_issue_flag
- tickets_per_tenure
- usage_per_tenure
- plan_type_Basic
- plan_type_Premium
- plan_type_Standard



Failure to maintain consistency causes feature mismatch errors.

---

## Why Feature Engineering Matters

Compared to raw inputs, engineered features:

- Improve model interpretability
- Increase predictive power
- Reduce noise
- Capture behavioral patterns

In testing, models trained with engineered features showed improved recall and AUC compared to raw feature models.

---

## Training-Serving Consistency

A critical deployment lesson:

> The same feature engineering logic must be applied during training and inference.

## Key Takeaway

Feature engineering was essential in improving churn prediction accuracy and ensuring production-readiness of the model.

Proper alignment between training and inference ensures model reliability.

