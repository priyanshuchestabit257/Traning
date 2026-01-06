## 1. Prerequisites
* Node.js v18+
* MongoDB Running
* Redis Server Running (`sudo service redis-server start`)

## 2. Environment Variables
Copy `.env.example` to `.env` and configure:
* `PORT`: API Port
* `MONGO_URI`: Database connection string

## 3. Starting the App (Production)
We use PM2 for process management.
```bash
# Start
pm2 start ecosystem.config.js

# Monitor
pm2 monit

# Logs
pm2 logs