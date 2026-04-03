pipeline {
    agent any
    
    environment {
        REPO_URL = 'https://github.com/impawan/devops-assignment-2024tm93700-ACEest-Fitness.git'
        TARGET_BRANCH = 'main'
        VENV_DIR = 'venv'
        IMAGE_NAME = 'aceest-fitness:jenkins'
    }
    
    triggers {
        // Trigger immediately when GitHub webhook sends push events.
        githubPush()
        // Fallback polling in case webhook is not configured/reachable.
        pollSCM('H/2 * * * *')
    }

    stages {
        stage('Checkout') {
            steps {
                echo "Pulling latest code from ${TARGET_BRANCH} branch..."
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: "*/${TARGET_BRANCH}"]],
                    userRemoteConfigs: [[url: "${REPO_URL}"]]
                ])
                echo "Checkout done."
            }
        }
        
        stage('Validate Main Branch Trigger') {
            steps {
                script {
                    def branchName = sh(
                        script: 'git rev-parse --abbrev-ref HEAD',
                        returnStdout: true
                    ).trim()
                    echo "Current checked-out branch: ${branchName}"
                    if (branchName != TARGET_BRANCH) {
                        error("Stopping build: expected '${TARGET_BRANCH}', found '${branchName}'.")
                    }
                    echo "Branch check passed."
                }
            }
        }

        stage('Build') {
            steps {
                echo "Creating virtual environment..."
                sh "python3 -m venv ${VENV_DIR}"
                echo 'Installing dependencies...'
                sh ". ${VENV_DIR}/bin/activate && pip install -r requirements.txt"
                echo 'Running syntax check...'
                sh ". ${VENV_DIR}/bin/activate && python -m py_compile app.py"
                echo 'Build step completed.'
            }
        }

        stage('Docker Build') {
            steps {
                echo "Building Docker image ${IMAGE_NAME}..."
                sh "docker build -t ${IMAGE_NAME} ."
                echo "Docker image ready."
            }
        }

        stage('Test') {
            steps {
                echo 'Running pytest suite...'
                sh ". ${VENV_DIR}/bin/activate && pytest -q"
                echo 'All tests passed.'
            }
        }
    }
}
