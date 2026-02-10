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

## Helmet Security Headers
Verified using:
curl -I http://localhost:3000

Headers present:
- Content-Security-Policy
- X-Frame-Options
- X-Content-Type-Options
- Strict-Transport-Security

## Rate Limiting
Configured: 5 requests/min
Verified by repeated curl requests
Server responds with 429 after limit

