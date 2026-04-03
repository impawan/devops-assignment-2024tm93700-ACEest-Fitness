# ACEest Fitness & Gym - DevOps Assignment

This repository contains a modular Flask application plus CI/CD automation to satisfy the DevOps assignment requirements.

## Project Structure

- `app.py` - Flask API for client and workout management
- `tests/test_app.py` - Pytest unit tests
- `requirements.txt` - Python dependencies
- `Dockerfile` - Container image build definition
- `.github/workflows/main.yml` - GitHub Actions CI workflow
- `Jenkinsfile` - Jenkins build pipeline

## Local Setup and Run

1. Create and activate a virtual environment:
   - macOS/Linux:
     - `python3 -m venv .venv`
     - `source .venv/bin/activate`
2. Install dependencies:
   - `pip install -r requirements.txt`
3. Run the application:
   - `python app.py`
4. Verify health endpoint:
   - `curl http://127.0.0.1:5000/health`

## Manual Test Execution

Run the full unit test suite:

`pytest -q`

## Docker Usage

Build and run the image:

- `docker build -t aceest-fitness:latest .`
- `docker run --rm -p 5000:5000 aceest-fitness:latest`

## CI/CD Overview (Jenkins + GitHub Actions)

- **GitHub Actions** (`.github/workflows/main.yml`)
  - Triggers on every `push` and `pull_request`
  - Performs build/syntax check with `python -m py_compile`
  - Builds Docker image
  - Runs `pytest` automated tests

- **Jenkins** (`Jenkinsfile`)
  - Uses a staged pipeline: Checkout -> Build -> Docker Build -> Test
  - Re-validates installation, compilation, image build, and tests in a controlled build server environment

Together, these pipelines provide automated quality gates from code commit to build validation.
