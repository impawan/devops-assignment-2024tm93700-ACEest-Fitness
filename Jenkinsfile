pipeline {
    agent any
    
    triggers {
        githubPush()
        pollSCM('* * * * *')
    }

    environment {
        DOCKERHUB_CREDENTIALS_ID = 'dockerhub-credentials'
        DOCKER_IMAGE = 'yourdockerhubuser/aceest-fitness'
        IMAGE_TAG = "v${env.BUILD_ID}"
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Test & Coverage') {
            steps {
                sh '''
                pip install -r requirements.txt
                pytest --junitxml=reports/pytest.xml --cov=app --cov-report=xml:reports/coverage.xml
                '''
            }
            post {
                always {
                    junit 'reports/pytest.xml'
                }
            }
        }
        stage('SonarQube Analysis') {
            steps {
                // Ensure SonarQube Scanner is configured in Jenkins globally
                // with the name 'sonar-scanner'
                script {
                    def scannerHome = tool 'sonar-scanner'
                    withSonarQubeEnv('sonarqube-server') {
                        sh "${scannerHome}/bin/sonar-scanner"
                    }
                }
            }
        }
        stage('Build Image') {
            steps {
                script {
                    dockerImage = docker.build("${DOCKER_IMAGE}:${IMAGE_TAG}")
                }
            }
        }
        stage('Push Image') {
            when {
                branch 'main'
            }
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', DOCKERHUB_CREDENTIALS_ID) {
                        dockerImage.push()
                        dockerImage.push('latest')
                    }
                }
            }
        }
        stage('Deploy to Kubernetes (Minikube)') {
            when {
                branch 'main'
            }
            steps {
                sh '''
                # Substitute the image tag in deployment and apply
                sed -i "s|image: yourdockerhubuser/aceest-fitness:latest|image: ${DOCKER_IMAGE}:${IMAGE_TAG}|g" k8s/deployment.yaml
                kubectl apply -f k8s/
                '''
            }
        }
    }
}
