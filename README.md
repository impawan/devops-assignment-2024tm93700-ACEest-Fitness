# ACEest Fitness & Gym — DevOps CI/CD Pipeline

> **Course:** Introduction to DevOps (CSIZG514/SEZG514) — S1-25  
> **Assignment 2:** CI/CD Implementation for ACEest Fitness & Gym  
> **Student ID:** 2024TM93700

A fully automated CI/CD pipeline for the ACEest Fitness & Gym Flask application, demonstrating industry-grade DevOps practices including version control, automated testing, static analysis, containerization, and Kubernetes deployment with five progressive deployment strategies.

---

## 📂 Project Structure

```
├── ACEest_Fitness.py             # Application launcher (entry point)
├── app.py                        # Extended version with SQLite CRUD endpoints
├── app/                          # Modular Flask application package
│   ├── __init__.py               #   App factory with Blueprint registration
│   ├── main.py                   #   Gunicorn-compatible entry point
│   ├── routes.py                 #   REST API endpoints (/health, /members)
│   ├── config.py                 #   Configuration classes (Prod & Test)
│   └── models.py                 #   Data model placeholder
├── test/
│   └── test_app.py               # Pytest: SQLite-backed endpoint tests
├── tests/
│   ├── __init__.py
│   └── test_routes.py            # Pytest: Blueprint route tests
├── Jenkinsfile                   # Declarative Jenkins CI/CD pipeline
├── Dockerfile                    # Multi-stage Docker build
├── requirements.txt              # Python dependencies
├── sonar-project.properties      # SonarQube scanner configuration
├── sonarqube_report.md           # SonarQube analysis results summary
├── assignment_report.md          # Detailed 2-3 page assignment report
├── k8s/                          # Kubernetes deployment manifests
│   ├── deployment.yaml           #   Rolling Update (default)
│   ├── deployment-blue-green.yaml#   Blue-Green strategy
│   ├── deployment-canary.yaml    #   Canary Release strategy
│   ├── deployment-shadow.yaml    #   Shadow Deployment strategy
│   ├── deployment-ab-testing.yaml#   A/B Testing strategy
│   └── service.yaml              #   LoadBalancer Service
└── .github/workflows/
    └── main.yml                  # GitHub Actions CI (syntax + Docker build)
```

---

## 🚀 CI/CD Pipeline Architecture

```
Developer Push → GitHub
                   │
        ┌──────────┼──────────┐
        ▼                     ▼
  GitHub Actions          Jenkins
  (Syntax & Build)    (Full Pipeline)
                           │
                    ┌──────┴──────┐
                    ▼             ▼
              Pytest + Cov   SonarQube
                    │             │
                    └──────┬──────┘
                           ▼
                    Docker Build
                    & Push to Hub
                           │
                           ▼
                  Kubernetes Deploy
                  (Rolling / B-G /
                   Canary / Shadow /
                   A/B Testing)
```

### Pipeline Stages (Jenkins)

| # | Stage               | Description                                                |
|---|---------------------|------------------------------------------------------------|
| 1 | Checkout            | Clone source from GitHub                                   |
| 2 | Test & Coverage     | Run `pytest` with JUnit XML + Coverage XML reports         |
| 3 | SonarQube Analysis  | Static code analysis and quality gate enforcement          |
| 4 | Build Image         | Multi-stage Docker build, tagged `v${BUILD_ID}`            |
| 5 | Push Image          | Push to Docker Hub (versioned tag + `latest`)              |
| 6 | Deploy to K8s       | Apply K8s manifests via `kubectl` to Minikube/cluster      |

---

## 🏗️ Deployment Strategies

Five Kubernetes deployment strategies are implemented:

| Strategy       | Manifest                          | Key Concept                                                  |
|----------------|-----------------------------------|--------------------------------------------------------------|
| **Rolling Update** | `k8s/deployment.yaml`         | Gradual pod replacement with zero downtime (maxSurge: 1)     |
| **Blue-Green**     | `k8s/deployment-blue-green.yaml` | Two full environments; instant traffic switch via Service  |
| **Canary**         | `k8s/deployment-canary.yaml`  | 1 replica of new version alongside stable for A/B validation |
| **Shadow**         | `k8s/deployment-shadow.yaml`  | Mirrored traffic to shadow pods (requires Istio/Nginx)       |
| **A/B Testing**    | `k8s/deployment-ab-testing.yaml` | Route subsets of users via Ingress headers/cookies         |

---

## 🧪 Testing & Quality

- **Unit Tests:** Two test suites (`test/test_app.py` and `tests/test_routes.py`) covering health checks, member CRUD, client CRUD, and workout logging.
- **Test Coverage:** **85.4%** (exceeds 80% quality gate).
- **SonarQube:** Quality Gate **PASSED** — 0 bugs, 0 vulnerabilities, 0 security hotspots, 2 minor code smells.
- **GitHub Actions:** Automated syntax check and Docker build validation on every push/PR.

---

## 🐳 Docker

The application uses a **multi-stage Docker build** for production:

```dockerfile
# Stage 1: Install dependencies
FROM python:3.10-slim AS builder
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Production image
FROM python:3.10-slim
COPY --from=builder /usr/local/lib/python3.10/site-packages ...
COPY app/ ./app/
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app.main:app"]
```

---

## ⚡ Quick Start (Local Development)

```bash
# 1. Clone the repository
git clone https://github.com/impawan/devops-assignment-2024tm93700-ACEest-Fitness.git
cd devops-assignment-2024tm93700-ACEest-Fitness

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run tests
pytest -v

# 4. Start the application
python ACEest_Fitness.py
# App runs at http://localhost:5000

# 5. Health check
curl http://localhost:5000/health
```

### Docker

```bash
docker build -t aceest-fitness:latest .
docker run -p 5000:5000 aceest-fitness:latest
```

### Kubernetes (Minikube)

```bash
minikube start
kubectl apply -f k8s/
minikube service aceest-fitness-service
```

---

## 📋 API Endpoints

| Method | Endpoint                        | Description                     |
|--------|---------------------------------|---------------------------------|
| GET    | `/health`                       | Health check                    |
| GET    | `/members`                      | List all gym members            |
| POST   | `/members`                      | Add a new member                |
| GET    | `/clients`                      | List all clients (SQLite)       |
| POST   | `/clients`                      | Create a new client (SQLite)    |
| POST   | `/workouts`                     | Log a workout for a client      |
| GET    | `/clients/<id>/workouts`        | Get workouts for a client       |

---

## 📄 Assignment Deliverables

| Requirement                              | Status | Location                                        |
|------------------------------------------|--------|-------------------------------------------------|
| Flask application files & versions       | ✅     | `ACEest_Fitness.py`, `app.py`, `app/`           |
| Jenkins pipeline configuration           | ✅     | `Jenkinsfile`                                   |
| Dockerfile                               | ✅     | `Dockerfile`                                    |
| Kubernetes YAML manifests                | ✅     | `k8s/` (6 files — 5 strategies + service)       |
| Pytest test cases                        | ✅     | `test/test_app.py`, `tests/test_routes.py`      |
| SonarQube report                         | ✅     | `sonarqube_report.md`                           |
| GitHub repository (public)               | ✅     | [Link](https://github.com/impawan/devops-assignment-2024tm93700-ACEest-Fitness) |
| Short report (2-3 pages)                 | ✅     | `assignment_report.md`                          |

---

## 📝 License

This project is submitted as part of the BITS Pilani DevOps coursework (S1-25).
