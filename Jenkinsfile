pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            agent {
                docker { image 'python:3.12-slim' }
            }
            steps {
                dir('app') {
                    sh '''
                        python -m venv .venv
                        . .venv/bin/activate
                        pip install -r requirements.txt
                    '''
                }
            }
        }

        stage('Test') {
            agent {
                docker { image 'python:3.12-slim' }
            }
            steps {
                dir('app') {
                    sh '''
                        python -m venv .venv
                        . .venv/bin/activate
                        pip install -r requirements.txt pytest
                        pytest test_app.py -v
                    '''
                }
            }
        }

        stage('Package') {
            steps {
                dir('app') {
                    sh 'docker build -t device-service:${BUILD_NUMBER} .'
                }
            }
        }
    }
}