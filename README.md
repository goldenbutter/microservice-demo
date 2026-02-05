# Microservice Demo (FastAPI + HTML/JS + Docker + Kubernetes)

A lightweight fullstack microservice project built using **FastAPI**, **simple HTML/JavaScript frontend**, fully containerized with **Docker**, orchestrated using **Docker Compose** and **Kubernetes**.

This project is ideal for learning:
- Backend API development with FastAPI  
- Simple static frontend integration  
- Containerization with Docker  
- Multi‑service orchestration  
- Kubernetes deployments  
- CI/CD pipeline creation (optional future addition)  

---

# 🏗 Architecture Overview

### 🧠 **High‑Level Architecture**

```
Browser (Frontend)
     |
     |  HTTP (JavaScript fetch)
     v
Frontend (NGINX container)
     |
     |  HTTP
     v
Backend (FastAPI container)
     |
     |  In-memory list
     v
Fake Database
```

---

# 🎨 Mermaid Architecture Diagram

```mermaid
flowchart LR
    A[User Browser] --> B[Frontend - NGINX]
    B -->|HTTP /items| C[Backend - FastAPI]
    C --> D[(In-Memory Data Store)]
```

---

# 📂 Project Structure

```
microservice-demo/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── crud.py
│   │   ├── models.py
│   │   ├── database.py
│   │   └── schemas.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   ├── styles.css
│   └── Dockerfile
│
├── k8s/
│   ├── backend-deployment.yaml
│   ├── backend-service.yaml
│   ├── frontend-deployment.yaml
│   ├── frontend-service.yaml
│   └── ingress.yaml
│
└── docker-compose.yml
```

---

# 🛠 Tech Stack

**Backend:** FastAPI, Python  
**Frontend:** HTML, JavaScript, CSS  
**Containers:** Docker, Docker Compose  
**Orchestration:** Kubernetes (Deployments + Services + Ingress)  
**Web Server:** NGINX (for frontend)  

---

# ✨ Features

- Create items  
- List items  
- Simple and clean UI  
- Backend + Frontend containerized  
- Docker Compose support  
- Kubernetes deployment manifests  
- Easy to extend with CI/CD or real databases  

---

# 🔌 API Endpoints (FastAPI)

All endpoints return JSON.

### GET `/`
Health check / welcome message.

### GET `/items`
Returns all items.

### POST `/items`
Creates a new item.

Body:
```json
{
  "name": "Laptop",
  "description": "Gaming laptop"
}
```

### GET `/items/{id}`
Returns a single item.

---

# 🐳 Running with Docker Compose

Make sure Docker is installed.

### Build & start:
```
docker compose up --build
```

### Access application:
Frontend → http://localhost:8080  
Backend → http://localhost:8000/docs  

---

# ☸️ Kubernetes Deployment

### Build Docker images inside minikube:
```
minikube start --driver=docker
minikube -p minikube docker-env | Invoke-Expression

docker build -t backend:latest ./backend
docker build -t frontend:latest ./frontend
```

### Apply all k8s manifests:
```
kubectl apply -f k8s/
```

### Enable ingress:
```
minikube addons enable ingress
minikube tunnel
```

### Add to your Local-hosts file:
```
127.0.0.1 microservice.local
```

Visit:
```
http://microservice.local

```

---

# 📸 Screenshots

- **Frontend UI**

<img width="700" height="750" alt="Frontend-port-5500" src="assets\frontend-5500-port-CORS.png" />

- **Swagger UI**

<img width="1700" height="1050" alt="Backend-port-5500" src="assets\backend-8000-port-CORS.png" />

<img width="1700" height="1050" alt="Backend-port-5500" src="assets\backend-test.png" />

- **Docker containers running**

<img width="800" height="550" alt="Frontend-SINGLE-port-8000" src="assets\frontend-docker-SINGLE-port-8000.png" />

<img width="1700" height="1050" alt="Backend-SINGLE-port-8000" src="assets\backend-docker-SINGLE-port-8000.png" />

- **Kubernetes dashboard**

<img width="811" height="532" alt="Kubernetes Test for Frontend" src="assets\k8s-frontend.png" />

<img width="416" height="286" alt="Kubernetes Test for Backend" src="assets\k8s-backend.png" />

---

# 🤝 Contributing

Feel free to:
- Add a database (PostgreSQL, MongoDB)  
- Add GitHub Actions CI/CD  
- Write automated tests  
- Improve UI  

Pull requests welcome!

---

## 🚀 Author
Created by **Bithun Chatterjee**  
GitHub: https://github.com/goldenbutter  