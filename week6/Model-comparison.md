# Model Comparison – Customer Churn Prediction

##  Overview

Multiple models were evaluated to identify the most suitable algorithm for churn prediction.

Models compared:

- Logistic Regression
- Random Forest
- XGBoost
- Neural Network

Evaluation metrics:

- Accuracy
- Precision
- Recall
- F1 Score
- ROC-AUC

Since churn detection has business impact, recall and ROC-AUC were prioritized.

---

##  Performance Results

| Model               | Accuracy | Precision | Recall | F1 Score | ROC-AUC |
|---------------------|----------|-----------|--------|----------|---------|
| Logistic Regression | 0.648    | 0.718     | 0.636  | 0.674    | 0.714 |
| Random Forest       | 0.654    | 0.681     | 0.748  | 0.713    | 0.698 |
| XGBoost             | 0.626    | 0.664     | 0.706  | 0.684    | 0.677 |
| Neural Network      | 0.588    | 0.639     | 0.646  | 0.643    | 0.623 |

---

## Key Observations

### 1️Logistic Regression
- Highest ROC-AUC (0.714)
- Strong precision (0.718)
- Balanced overall performance
- Most interpretable

### 2️ Random Forest
- Highest accuracy (0.654)
- Highest recall (0.748)
- Best F1 score (0.713)
- Slightly lower ROC-AUC than Logistic Regression

### 3️ XGBoost
- Moderate performance
- Lower AUC than Logistic Regression
- Did not outperform Random Forest

### 4️Neural Network
- Lowest performance overall
- Likely underfitting 

---

##  Final Model Selection

Logistic Regression was selected because:

- Highest ROC-AUC (best class separation)
- Strong precision
- Simpler architecture
- Easier debugging
- Lower operational complexity
- More explainable to stakeholders

Although Random Forest achieved slightly higher recall and F1 score, the marginal gain did not justify increased complexity.

---

## Trade-Off Analysis

| Criteria | Logistic Regression | Random Forest |
|-----------|--------------------|--------------|
Interpretability | High | Medium |
Complexity | Low | Medium |
Inference Speed | Fast | Moderate |
Maintenance | Easy | Moderate |
Performance | Strong | Slightly Higher Recall |

---

##  Final Decision Rationale

The chosen model (Logistic Regression) provides the best balance of:

- Predictive power
- Stability
- Interpretability
- Deployment simplicity

This aligns with production-grade ML system requirements.
