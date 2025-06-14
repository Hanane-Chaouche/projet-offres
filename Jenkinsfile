pipeline {
    agent any

    stages {
        stage('Installer les dépendances') {
            steps {
                bat 'pip install -r requirements.txt'
            }
        }

        stage('Préparer les dossiers') {
            steps {
                bat '''
                    cd /d "%WORKSPACE%"
                    mkdir data 2>nul || echo Le dossier data existe déjà.
                    mkdir logs 2>nul || echo Le dossier logs existe déjà.
                    mkdir public 2>nul || echo Le dossier public existe déjà.
                    ping 127.0.0.1 -n 3 >nul
                '''
            }
        }

        stage('Scraper les offres') {
            steps {
                bat '''
                    cd /d "%WORKSPACE%"
                    python scraper.py
                '''
            }
        }

        stage('Détection de changements') {
            steps {
                bat '''
                    cd /d "%WORKSPACE%"
                    if not exist logs\\log.txt (
                        echo ===== Journal du pipeline Jenkins ===== > logs\\log.txt
                    )

                    if not exist data\\jobs_previous.csv (
                        echo [%date% %time%] Premiere execution : copie initiale >> logs\\log.txt
                        copy data\\jobs.csv data\\jobs_previous.csv
                        exit /b 0
                    )

                    certutil -hashfile data\\jobs.csv SHA256 > new_hash.txt
                    certutil -hashfile data\\jobs_previous.csv SHA256 > old_hash.txt

                    for /f "tokens=1" %%A in (new_hash.txt) do set NEW_HASH=%%A
                    for /f "tokens=1" %%A in (old_hash.txt) do set OLD_HASH=%%A

                    if "%NEW_HASH%" == "%OLD_HASH%" (
                        echo [%date% %time%] Aucune nouvelle offre detectee. >> logs\\log.txt
                    ) else (
                        echo [%date% %time%] Nouvelles offres detectees. >> logs\\log.txt
                        copy /Y data\\jobs.csv data\\jobs_previous.csv >nul
                        echo [%date% %time%] Rapport HTML mis a jour. >> logs\\log.txt
                    )
                '''
            }
        }

        stage('Generer HTML') {
            steps {
                bat '''
                    cd /d "%WORKSPACE%"
                    python html_generator.py
                '''
            }
        }

        stage('Archiver') {
            steps {
                archiveArtifacts artifacts: 'data/jobs.csv, data/jobs_previous.csv, public/index.html, logs/log.txt', fingerprint: true
            }
        }
    }

    post {
        always {
            echo "Pipeline terminé localement"
        }
    }
}
