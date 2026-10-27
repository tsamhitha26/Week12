
pipeline {
    agent any

    stages {
        stage('Install Dependencies') {
            steps {
                bat '"C:\\Users\\sneha\\AppData\\Local\\Programs\\Python\\Python311\\python.exe" -m pip install -r requirements.txt'
            }
        }

        stage('Run Selenium Tests') {
            steps {
                bat 'start /B "" "C:\\Users\\sneha\\AppData\\Local\\Programs\\Python\\Python311\\python.exe" app.py'
                bat 'ping 127.0.0.1 -n 6 > nul'
                bat '"C:\\Users\\sneha\\AppData\\Local\\Programs\\Python\\Python311\\python.exe" -m pytest -v'
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
                    bat 'echo %DOCKERHUB_TOKEN%| docker login -u %DOCKERHUB_USERNAME% --password-stdin'
                    bat 'docker push tsamhitha26/seleniumtestdemoapp:v1'
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                bat 'kubectl apply -f deployment.yaml'
                bat 'kubectl apply -f service.yaml'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check the console output.'
        }
    }
}
