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

                       stage('Setup Test Env') {
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
            }
        }

        stage('Test') {
            parallel {
                stage('Unit Tests') {
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
                stage('Lint') {
                    agent {
                        docker { image 'python:3.12-slim' }
                    }
                    steps {
                        dir('app') {
                            sh '''
                                python -m venv .venv
                                . .venv/bin/activate
                                pip install flake8
                                flake8 app.py --max-line-length=100
                            '''
                        }
                    }
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