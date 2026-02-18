
# Model Interpretation – Logistic Regression

## Why Logistic Regression?

Logistic Regression achieved:

- Highest ROC-AUC (0.714)
- Strong precision (0.718)
- Competitive F1 score (0.674)

Its linear nature makes it highly interpretable.

---

## Understanding Coefficients

In Logistic Regression:

- Positive coefficient → increases churn probability
- Negative coefficient → decreases churn probability

Key drivers likely include:

- low_usage_flag (positive impact)
- payment_issue_flag (positive impact)
- tickets_per_tenure (positive impact)
- longer tenure (negative impact)
- Premium plan (negative impact)

---

## What ROC-AUC = 0.714 Means

The model has a 71.4% probability of correctly ranking a random churner higher than a non-churner.

This indicates moderate predictive power and meaningful class separation.

---

## Business Value

The model allows:

- Identifying high-risk customers
- Designing retention strategies
- Targeted interventions
- Early churn detection

---

## Future Improvements

- SHAP value visualization
- Threshold tuning for business optimization
- Cost-sensitive learning
- Ensemble stacking
