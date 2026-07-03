pipeline {
  agent any

  options {
    timestamps()
    skipDefaultCheckout()
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Backend Build & Validate') {
      steps {
        dir('backend-django') {
          sh '''
            python3 --version
            python3 -m pip install --upgrade pip
            python3 -m pip install -r requirements.txt
            python3 manage.py check
            python3 -m compileall .
          '''
        }
      }
    }

    stage('Frontend Build & Validate') {
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
      cleanWs()
    }
  }
}
