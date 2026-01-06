## Task 1 Report: Production Backend Architecture

## 1. Overview
This document summarizes the work completed for **Task 1: System Architecture & Initialization. The goal was to move from a basic Node.js setup to a scalable, production-ready backend using a **layered architecture**.

The current system supports:
- Multi-environment configuration  
- Clear separation of concerns  
- Basic observability through structured logging  

This provides a clean foundation for further feature development.

---

## 2. Architecture Design
The backend is organized using a **3-layer architecture** that separates the HTTP layer, business logic, and database concerns. This makes the codebase easier to maintain, test, and scale.

### Project Structure
- **`src/loaders/`**  
  Responsible for application startup. Database and Express are initialized independently.
- **`src/config/`**  
  Centralized environment configuration. All secrets and environment variables are loaded from here.
- **`src/utils/`**  
  Shared utilities, including a custom Winston logger.
- **`src/app.js`**  
  Clean entry point that delegates all setup to the loaders.

---

## 3. Key Implementations

### A. Multi-Environment Configuration
The application automatically loads environment-specific configuration based on `NODE_ENV`. This allows the same codebase to run across different environments without manual changes.

| Environment | File | Usage |
|------------|------|--------|
| Development | `.env.dev` | Default dev setup (Port 3000) |
| Production | `.env.prod` | Production-like settings (Port 8000) |
| Local | `.env.local` | Developer-specific overrides (ignored by Git) |

---

### B. Loader Pattern
Startup logic is split into modular loaders instead of being handled in a single file:
- **`src/loaders/db.js`**: Handles MongoDB connection and error handling.  
- **`src/loaders/app.js`**: Controls initialization order (DB → Middlewares → Routes).  

This keeps `app.js` minimal and makes startup logic easier to reason about and extend.

---

### C. Observability (Logging)
Replaced `console.log` with **Winston** for structured and persistent logging:
- **Console logs**: Colorized and formatted for local development.  
- **File logs**: JSON output written to `src/logs/app.log` for debugging and auditing.

---

## 4. Verification
The setup was validated by running the application in all environments (`dev`, `prod`, `local`). On startup, the following checks are logged:

- ✔ Database connection established  
- ✔ Middlewares initialized  
- ✔ Routes registered  
- ✔ Server started on the correct port (3000 for dev, 8000 for prod)

This confirms that the loader flow and configuration handling work as expected.

---

## 5. Deliverables
- **[x] `/src/loaders/app.js`** – Application orchestrator  
- **[x] `/src/loaders/db.js`** – Database connection handler  
- **[x] `/src/utils/logger.js`** – Winston-based logger  
- **[x] Config loader** – Support for `.env.dev`, `.env.prod`, `.env.local`