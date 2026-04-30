# ACEest Fitness & Gym - DevOps CI/CD Pipeline

This repository contains the source code and DevOps configurations for the ACEest Fitness & Gym application.

## Project Structure
- `app/`: Flask application code.
- `tests/`: Pytest unit tests.
- `k8s/`: Kubernetes deployment manifests.
- `Dockerfile`: Multi-stage Docker build.
- `Jenkinsfile`: CI/CD pipeline definition.
- `sonar-project.properties`: SonarQube configuration.

## Local Development
1. Install requirements: `pip install -r requirements.txt`
2. Run tests: `pytest`
3. Run app: `python -m app.main`

## CI/CD Workflow
1. Developer pushes code to GitHub.
2. Jenkins webhook triggers a build.
3. Jenkins runs Pytest and SonarQube analysis.
4. Jenkins builds the Docker image and pushes to Docker Hub.
5. Jenkins deploys the new image to the Kubernetes cluster using a Rolling Update strategy.

## Deployment Strategies included:
- Rolling Update (default in `k8s/deployment.yaml`)
- Blue-Green (`k8s/deployment-blue-green.yaml`)
