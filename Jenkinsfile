pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        JOBS_CSV = 'data/jobs.csv'
        PREV_CSV = 'data/jobs_previous.csv'
        HTML_OUT = 'public/index.html'
        LOG_FILE = 'logs/log.txt'
        DEPLOY_TARGET = '/var/www/html/index.html'
        REMOTE_HOST = 'root@138.197.171.64'
        SSH_KEY = 'id_ed25519_digitalocean'
        PSCP_PATH = 'pscp.exe' // Mets le chemin absolu si besoin
    }

    stages {

        stage('Préparation') {
            steps {
                echo "Préparation des dossiers et du venv"
                bat 'if not exist data mkdir data'
                bat 'if not exist logs mkdir logs'
                bat 'if not exist public mkdir public'
                bat 'python -m venv %VENV_DIR%'
            }
        }

        stage('Install') {
            steps {
                echo "Activation du venv et installation des dépendances"
                bat '''
                    call %VENV_DIR%\\Scripts\\activate
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Scraping') {
            steps {
                echo "Exécution du scraping"
                bat 'call %VENV_DIR%\\Scripts\\activate && python scraper.py'
            }
        }

        stage('Tests') {
            steps {
                echo "Tests de validation sur jobs.csv et index.html"
                bat '''
                    for /f %%A in ('find /v /c "" ^< %JOBS_CSV%') do set NB_LINES=%%A
                    if %NB_LINES% LSS 10 (
                        echo Echec : jobs.csv a moins de 10 lignes!
                        exit /b 1
                    )
                '''
            }
        }

        stage('DetectChanges') {
            steps {
                echo "Détection de changements entre jobs.csv et jobs_previous.csv"
                bat '''
                    setlocal enabledelayedexpansion
                    if exist %PREV_CSV% (
                        certutil -hashfile %JOBS_CSV% SHA256 > new_hash.txt
                        certutil -hashfile %PREV_CSV% SHA256 > old_hash.txt
                        set NEW_HASH=
                        set OLD_HASH=
                        for /f "skip=1 tokens=1" %%A in (new_hash.txt) do (
                            if not defined NEW_HASH set NEW_HASH=%%A
                        )
                        for /f "skip=1 tokens=1" %%A in (old_hash.txt) do (
                            if not defined OLD_HASH set OLD_HASH=%%A
                        )
                        echo NEW_HASH=!NEW_HASH!
                        echo OLD_HASH=!OLD_HASH!
                        if "!NEW_HASH!" == "!OLD_HASH!" (
                            echo [%date% %time%] Aucune nouvelle offre. >> %LOG_FILE%
                            exit /b 0
                        )
                    )
                    copy /Y %JOBS_CSV% %PREV_CSV% >nul
                    endlocal
                '''
            }
        }

        stage('Conversion HTML') {
            steps {
                echo "Conversion CSV → HTML"
                bat 'call %VENV_DIR%\\Scripts\\activate && python html_generator.py'
                bat '''
                    findstr /C:"<table" %HTML_OUT% >nul || (echo Echec : pas de <table> et exit /b 1)
                    find /c "<tr" %HTML_OUT% > lines.txt
                    for /f %%A in (lines.txt) do set NBTR=%%A
                    if %NBTR% LSS 11 (
                        echo Echec : index.html a moins de 10 lignes de données!
                        exit /b 1
                    )
                '''
            }
        }

        stage('Archive') {
            steps {
                echo "Archivage Jenkins"
                archiveArtifacts artifacts: 'data/jobs.csv, data/jobs_previous.csv, public/index.html, logs/log.txt', fingerprint: true
            }
        }

        stage('Deploy') {
            steps {
                echo "Déploiement sur VPS via pscp"
                // Assure-toi que la clé est bien trouvée, format .ppk ou compatible cible
                bat '"%PSCP_PATH%" -i %SSH_KEY% -batch -scp public\\index.html %REMOTE_HOST%:%DEPLOY_TARGET%'
            }
        }
    }

    post {
        always {
            echo "Nettoyage de l'environnement virtuel"
            bat 'rmdir /s /q %VENV_DIR% || exit 0'
        }
        failure {
            echo 'Le pipeline a échoué. Consultez les logs.'
        }
    }
}
