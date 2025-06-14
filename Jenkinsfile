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
                    echo Dossier courant : %cd%
                    if not exist "%cd%\\data" mkdir "%cd%\\data"
                    if not exist "%cd%\\logs" mkdir "%cd%\\logs"
                    if not exist "%cd%\\public" mkdir "%cd%\\public"

                    rem Attente fiable via ping
                    ping 127.0.0.1 -n 4 >nul
                '''
            }
        }

        stage('Scraper les offres') {
            steps {
                bat 'python scraper.py'
            }
        }

        stage('Détection de changements') {
            steps {
                bat '''
                    if not exist "%cd%\\logs\\log.txt" echo ===== Journal du pipeline Jenkins ===== > "%cd%\\logs\\log.txt"

                    if not exist "%cd%\\data\\jobs_previous.csv" (
                        echo [%date% %time%] Premiere execution : copie initiale >> "%cd%\\logs\\log.txt"
                        copy "%cd%\\data\\jobs.csv" "%cd%\\data\\jobs_previous.csv"
                        exit /b 0
                    )

                    certutil -hashfile "%cd%\\data\\jobs.csv" SHA256 > "%cd%\\new_hash.txt"
                    certutil -hashfile "%cd%\\data\\jobs_previous.csv" SHA256 > "%cd%\\old_hash.txt"

                    for /f "tokens=1" %%A in (%cd%\\new_hash.txt) do set NEW_HASH=%%A
                    for /f "tokens=1" %%A in (%cd%\\old_hash.txt) do set OLD_HASH=%%A

                    if "%NEW_HASH%" == "%OLD_HASH%" (
                        echo [%date% %time%] Aucune nouvelle offre detectee. >> "%cd%\\logs\\log.txt"
                    ) else (
                        echo [%date% %time%] Nouvelles offres detectees. >> "%cd%\\logs\\log.txt"
                        copy /Y "%cd%\\data\\jobs.csv" "%cd%\\data\\jobs_previous.csv" >nul
                        echo [%date% %time%] Rapport HTML mis a jour. >> "%cd%\\logs\\log.txt"
                    )
                '''
            }
        }

        stage('Generer HTML') {
            steps {
                bat 'python html_generator.py'
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
