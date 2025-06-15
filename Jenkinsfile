pipeline {
    agent any

    environment {
        VENV_DIR   = 'venv'
        JOBS_CSV   = 'data/jobs.csv'
        PREV_CSV   = 'data/jobs_previous.csv'
        HTML_FILE  = 'public\\index.html' // antislash Windows partout
        LOG_FILE   = 'logs\\log.txt'
        SSH_KEY_PATH = 'C:\\Users\\chame\\.ssh\\id_ed25519_digitalocean'
        VPS_USER   = 'root'
        VPS_HOST   = '138.197.171.64'
        VPS_PATH   = '/var/www/html/index.html'
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
                bat """
                    call %VENV_DIR%\\Scripts\\activate
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                """
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
                    setlocal enabledelayedexpansion
                    if exist %JOBS_CSV% (
                        for /f %%A in ('find /v /c "" ^< %JOBS_CSV%') do (
                            set NB_LINES=%%A
                            echo Lignes trouvées : !NB_LINES!
                            if !NB_LINES! LSS 10 (
                                echo Echec : jobs.csv a moins de 10 lignes!
                                exit /b 1
                            )
                        )
                    ) else (
                        echo Echec : jobs.csv introuvable!
                        exit /b 1
                    )
                    endlocal
                '''
            }
        }
        stage('DetectChanges') {
            steps {
                echo "Détection de changements"
                bat """
                    setlocal enabledelayedexpansion
                    if not exist logs mkdir logs
                    if not exist %PREV_CSV% (
                        copy %JOBS_CSV% %PREV_CSV% >nul
                        echo [%date% %time%] Première exécution, création jobs_previous.csv >> logs\\log.txt
                        endlocal
                        exit /b 0
                    )
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
                        echo [%date% %time%] Aucune nouvelle offre. >> logs\\log.txt
                        endlocal
                        exit /b 0
                    )
                    copy /Y %JOBS_CSV% %PREV_CSV% >nul
                    endlocal
                    exit /b 0
                """
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
                bat """
                    if exist %HTML_FILE% (
                        echo OK: index.html trouvé
                    ) else (
                        echo Echec : index.html introuvable!
                        exit /b 1
                    )
                    findstr /C:"<table" %HTML_FILE% >nul
                    if errorlevel 1 (
                        echo Echec : pas de <table> dans index.html
                        exit /b 1
                    )
                    find /c "<tr" %HTML_FILE% > lines.txt
                    for /f "tokens=2 delims=:" %%A in (lines.txt) do set NBTR=%%A
                    if not defined NBTR (
                        echo Echec : impossible de compter les <tr>!
                        exit /b 1
                    )
                    if %NBTR% LSS 10 (
                        echo Echec : index.html a moins de 10 lignes de donnees !
                        exit /b 1
                    )
                """
            }
        }
        stage('Archive') {
            steps {
                echo "Archivage Jenkins"
                archiveArtifacts artifacts: 'data/jobs.csv, data/jobs_previous.csv, public/index.html, logs/log.txt', allowEmptyArchive: false
            }
        }
        stage('Deploy') {
            steps {
                echo "Déploiement sur VPS via scp"
                bat """
                    if exist "%SSH_KEY_PATH%" (
                        echo OK: clé SSH trouvée
                    ) else (
                        echo ERREUR: clé SSH introuvable!
                        exit /b 1
                    )
                    if exist "%HTML_FILE%" (
                        echo OK: index.html trouvé
                    ) else (
                        echo ERREUR: index.html introuvable!
                        exit /b 1
                    )
                    scp -i "%SSH_KEY_PATH%" -o StrictHostKeyChecking=no %HTML_FILE% %VPS_USER%@%VPS_HOST%:%VPS_PATH%
                """
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
