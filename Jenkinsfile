pipeline {
  agent any

  environment {
    VENV_DIR = '.venv'
    COVERAGE_THRESHOLD = '70'
  }

  stages {
    stage('Clone Repo') {
      steps {
        git 'https://github.com/Sanchez10/alu-music-teste-alura.git'
      }
    }

    stage('Setup Python Environment') {
      steps {
        sh '''
          python -m venv ${VENV_DIR}
          source ${VENV_DIR}/bin/activate
          pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov
        '''
      }
    }

    stage('Run Tests and Coverage') {
      steps {
        sh '''
          source ${VENV_DIR}/bin/activate
          pytest --cov=app \
                 --cov-report=term-missing \
                 --cov-report=html:coverage_html \
                 --cov-fail-under=${COVERAGE_THRESHOLD}
        '''
      }
    }

    stage('Archive Coverage Report') {
      steps {
        // Salva a cobertura HTML como artefato acessível no Jenkins
        archiveArtifacts artifacts: 'coverage_html/**', fingerprint: true
      }
    }
  }

  post {
    success {
      echo 'Pipeline finalizado com sucesso!'
    }
    failure {
      echo 'Pipeline falhou. Verifique os testes e cobertura.'
    }
  }
}
