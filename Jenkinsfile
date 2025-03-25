pipeline{
    agent any

    environment {
        VENV_DIR = 'hotel'
    }

    stages{
        stage('Cloning the Github repo to Jenkins'){
            steps{
                echo 'Cloning the Github repo to Jenkins.......'
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/anvesh4161/Hotel_reservation_MLOps.git']])
            }
        }

        stage('Setting up our virtual environment and installing dependencies'){
            steps{
                echo 'Setting up our virtual environment and installing dependencies.......'
                sh '''
                python -m venv ${VENV_DIR}
                . ${VENV_DIR}/bin/activate

                pip install --upgrade pip
                pip install -e .
                '''
            }
        }
    }
}
