# API Security Implementation Report

## 1. Implemented Defenses

| Defense Layer | Implementation Tool | Purpose |
| :--- | :--- | :--- |
| **Header Hardening** | `helmet` | Hides `X-Powered-By`, sets `Strict-Transport-Security` to prevent protocol downgrade attacks. |
| **Rate Limiting** | `express-rate-limit` | Limits each IP to 100 requests per 15 mins to prevent Brute Force & DoS attacks. |
| **CORS Policy** | `cors` | Restricts cross-origin resource sharing to trusted domains only. |
| **Input Validation** | `joi` | Ensures data (User/Product) matches strict schemas, preventing SQL/NoSQL injection and pollution. |
| **Payload Limits** | `express.json({ limit: '10kb' })` | Rejects large request bodies to prevent memory exhaustion crashes. |

## 2. Manual Security Test Cases

### Test Case 1: Rate Limiting
* **Action:** Send 101 requests within 15 minutes.
* **Expected Result:** API returns HTTP 429 "Too many requests".
* **Status:**  Passed

### Test Case 2: Invalid Input (Validation)
* **Action:** Send POST `/products` with `price: "free"` (String instead of Number).
* **Expected Result:** API returns HTTP 400 "price must be a number".
* **Status:** Passed

### Test Case 3: Large Payload Attack
* **Action:** Send a POST request with a 5MB JSON body.
* **Expected Result:** API returns HTTP 413 "Payload Too Large".
* **Status:**  Passed