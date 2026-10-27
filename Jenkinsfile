pipeline {
    agent any
    stages {
        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install -r requirements.txt'
            }
        }
        stage('Run Selenium Tests') {
            steps {
                // Jenkins agent must have Chrome installed and be able to launch it.
                bat 'start /B python app.py'
                bat 'ping 127.0.0.1 -n 6 > nul'
                bat 'python -m pytest -v'
            }
        }
        stage('Build Docker Image') {
            steps {
                bat 'docker build -t tsamhitha26/seleniumtestdemoapp:v1 .'
            }
        }
        stage('Login and Push Image') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKERHUB_USERNAME',
                    passwordVariable: 'DOCKERHUB_TOKEN'
                )]) {
                    bat 'docker login -u %DOCKERHUB_USERNAME% -p %DOCKERHUB_TOKEN%'
                    bat 'docker push tsamhitha26/seleniumtestdemoapp:v1'
                }
            }
        }
        stage('Deploy to Kubernetes') {
            steps {
                bat 'kubectl apply -f deployment.yaml'
            }
        }
    }
    post {
        success { echo 'Pipeline completed successfully!' }
        failure { echo 'Pipeline failed. Check the console output.' }
    }
}
