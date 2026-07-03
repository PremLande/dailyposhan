pipeline {
  agent none
  stages {
    stage('Checkout') {
      agent any
      steps {
        checkout scm
      }
    }
    stage('Backend Build & Validate') {
      agent {
        docker {
          image 'python:3.12-slim'
          args '-u root:root'
        }
      }
      steps {
        dir('backend-django') {
          sh '''
            python --version
            python -m pip install --upgrade pip
            python -m pip install -r requirements.txt
            python manage.py check
            python -m compileall .
          '''
        }
      }
    }
    stage('Frontend Build & Validate') {
      agent {
        docker {
          image 'node:20-alpine'
          args '-u root:root'
        }
      }
      steps {
        dir('frontend-react') {
          sh '''
            node --version
            npm --version
            npm install
            npm run build
          '''
        }
      }
    }
    stage('Docker Build & Validate') {
      agent {
        docker {
          image 'docker:24.0.5'
          args '-u root:root -v /var/run/docker.sock:/var/run/docker.sock'
        }
      }
      steps {
        sh '''
          docker build -f backend-django/Dockerfile -t dailyposhan-backend:ci ./backend-django
          docker build -f frontend-react/Dockerfile -t dailyposhan-frontend:ci ./frontend-react
          if command -v docker compose >/dev/null 2>&1; then
            docker compose -f docker-compose.yml config
          else
            docker-compose -f docker-compose.yml config
          fi
        '''
      }
    }
  }
  post {
    always {
      deleteDir()
    }
  }
}
