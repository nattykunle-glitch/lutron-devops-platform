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
                        pip install -r requirements.txt pytest flake8
                    '''
                }
                parallel(
                    "Unit Tests": {
                        dir('app') {
                            sh '''
                                . .venv/bin/activate
                                pytest test_app.py -v
                            '''
                        }
                    },
                    "Lint": {
                        dir('app') {
                            sh '''
                                . .venv/bin/activate
                                flake8 app.py --max-line-length=100
                            '''
                        }
                    }
                )
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