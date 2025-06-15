pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        JOBS_CSV = 'data/jobs.csv'
        PREV_CSV = 'data/jobs_previous.csv'
        HTML_OUT = 'public/index.html'
        LOG_FILE = 'logs/log.txt'
        DEPLOY_TARGET = '/var/www/html/index.html'
        REMOTE_HOST = 'root@192.168.X.X'
        SSH_KEY = 'C:\\chemin\\id_ed25519'
        PSCP_PATH = 'C:\\chemin\\pscp.exe'
    }

    stages {

        stage('Prepare') {
            steps {
                echo "Création des dossiers et du venv"
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

        stage('Tests CSV') {
            steps {
                echo "Validation du fichier jobs.csv"
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
                echo "Détection de changements"
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
                        if "!NEW_HASH!" == "!OLD_HASH!" (
                            echo [%date% %time%] Aucune nouvelle offre. >> %LOG_FILE%
                            endlocal
                            exit /b 0
                        )
                    )
                    copy /Y %JOBS_CSV% %PREV_CSV% >nul
                    endlocal
                    exit /b 0
                '''
            }
        }

        stage('Conversion HTML') {
            steps {
                echo "Conversion CSV → HTML"
                bat 'call %VENV_DIR%\\Scripts\\activate && python html_generator.py'
            }
        }

        stage('Validate HTML') {
            steps {
                echo "Validation de la structure du HTML (batch Windows)"
                bat '''
                    findstr /C:"<table" public\\index.html >nul
                    if errorlevel 1 (
                        echo Echec : pas de <table> dans index.html
                        exit /b 1
                    )
                    find /c "<tr" public\\index.html > lines.txt
                    for /f %%A in (lines.txt) do set NBTR=%%A
                    if %NBTR% LSS 10 (
                        echo Echec : index.html a moins de 10 lignes de donnees !
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
