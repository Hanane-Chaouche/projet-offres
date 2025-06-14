pipeline {
    agent any

    stages {
        stage('Installer les dépendances') {
            steps {
                bat 'pip install -r requirements.txt'
            }
        }

        stage('Exécuter le script Python') {
            steps {
                bat 'python scraper.py'
            }
        }

        stage('Archiver le fichier CSV') {
            steps {
                archiveArtifacts artifacts: 'jobs.csv', fingerprint: true
            }
        }
    }
}
