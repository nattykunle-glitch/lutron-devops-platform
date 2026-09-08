@Library('mini-devops-shared-lib') _
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
                runTests(path: 'app', framework: 'pytest')
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

    post {
        success {
            sh 'python3 scripts/sync_status.py --status success --build ${BUILD_NUMBER}'
        }
        failure {
            sh 'python3 scripts/sync_status.py --status failure --build ${BUILD_NUMBER}'
        }
    }
}