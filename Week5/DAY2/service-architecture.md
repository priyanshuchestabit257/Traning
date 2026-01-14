# Docker Day 2: MERN Stack with Networking & Volumes

## Project Overview
This project demonstrates a containerized MERN (MongoDB, Express, React, Node) stack application managed by **Docker Compose**. 

The core objective of this task was to implement and verify:
1.  **Docker Networking:** Establishing communication between independent containers (Frontend ↔ Backend ↔ Database).
2.  **Docker Volumes:** Ensuring data persistence for the MongoDB database so data survives container restarts.

---

## Architecture & Concepts

### 1. Multi-Container Orchestration
We use `docker-compose.yml` to spin up three isolated services that work together:
* **Client (`frontend`)**: React + Vite running on Host Port `3000` (Mapped to Container Port `5173`).
* **Server (`backend`)**: Node.js + Express running on Host Port `5000`.
* **Database (`mongo`)**: MongoDB running on standard Port `27017`.

### 2. Networking (`mern_net`)
* **Why we use it:** To allow containers to communicate securely without exposing every internal port to the outside world.
* **Implementation:** A custom bridge network named `mern_net` is created.
* **Service Discovery:** The Node.js backend connects to the database using the hostname `mongo` (e.g., `mongodb://mongo:27017/...`). Docker's internal DNS resolves this name to the correct container IP automatically.

### 3. Volumes (`mongo_data`)
* **Why we use it:** By default, if a container is deleted, its internal data is lost.
* **Implementation:** A named volume `mongo_data` is mounted to `/data/db` inside the MongoDB container.
* **Result:** The actual database files are stored on the host machine. Even if we run `docker compose down`, the user data remains safe.

---

## roject Structure

```text
/mern_app
├── client/              # React Frontend (Vite)
├── server/              # Node.js Backend
│   ├── src/index.js     # Server logic with /api/users routes
│   └── Dockerfile       # Backend image configuration
├── docker-compose.yml   # Orchestration for all services
├── start.sh             # Automation script (Build + Run + Log)
└── README.md            # Project Documentation


# Make the script executable (only needed once)
chmod +x start.sh

# Start the application
./start.sh