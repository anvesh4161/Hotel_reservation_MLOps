pipeline{
    agent any

    stages{
        stage('Cloning the Github repo to Jenkins'){
            steps{
                echo 'Cloning the Github repo to Jenkins.......'
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/anvesh4161/Hotel_reservation_MLOps.git']])
            }
        }
    }
}
