pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                sh 'python3 -m venv venv'
                sh '. venv/bin/activate && pip install -r requirements.txt'
                sh '. venv/bin/activate && python -m py_compile app.py'
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t aceest-fitness:jenkins .'
            }
        }

        stage('Test') {
            steps {
                sh '. venv/bin/activate && pytest -q'
            }
        }
    }
}
