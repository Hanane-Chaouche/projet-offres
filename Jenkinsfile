pipeline {
    agent any

    environment {
        VENV_DIR      = 'venv'
        JOBS_CSV      = 'data/jobs.csv'
        PREV_CSV      = 'data/jobs_previous.csv'
        HTML_FILE     = 'public\\index.html'
        LOG_FILE      = 'logs\\log.txt'
        SSH_KEY_PATH  = "C:\\ProgramData\\Jenkins\\.jenkins\\workspace\\id_ed25519_digitalocean.ppk"
        VPS_USER      = 'hanane'
        VPS_HOST      = '138.197.171.64'
        VPS_PATH      = '/var/www/html/index.html'
        PSCP_EXE = 'C:\\jenkins-keys\\pscp.exe'
    }

    stages {

        stage('Prepare') {
            steps {
                echo "Création du venv"
                bat 'python -m pip install --upgrade pip'
                bat 'python -m venv %VENV_DIR%'
            }
        }

        stage('Install') {
            steps {
                echo "Activation du venv et installation des dépendances"
                bat """
                    call %VENV_DIR%\\Scripts\\activate
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
                bat '''
                    setlocal enabledelayedexpansion

                    if not exist logs1\\nul (
                        mkdir logs1
                    )

                    if not exist data\\jobs_previous.csv (
                        copy data\\jobs.csv data\\jobs_previous.csv >nul
                        echo [%date% %time%] Première exécution, création jobs_previous.csv >> logs1\\log.txt
                        endlocal
                        exit /b 0
                    )

                    certutil -hashfile data\\jobs.csv SHA256 > new_hash.txt
                    certutil -hashfile data\\jobs_previous.csv SHA256 > old_hash.txt

                    set NEW_HASH=
                    set OLD_HASH=
                    for /f "skip=1 tokens=1" %%A in (new_hash.txt) do (
                        if not defined NEW_HASH set NEW_HASH=%%A
                    )
                    for /f "skip=1 tokens=1" %%A in (old_hash.txt) do (
                        if not defined OLD_HASH set OLD_HASH=%%A
                    )

                    if "!NEW_HASH!" == "!OLD_HASH!" (
                        echo [%date% %time%] Aucune nouvelle offre. >> logs1\\log.txt
                    ) else (
                        echo [%date% %time%] Nouvelle offre détectée ! À consulter. >> logs1\\log.txt
                        copy /Y data\\jobs.csv data\\jobs_previous.csv >nul
                    )

                    del new_hash.txt old_hash.txt
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
                archiveArtifacts artifacts: 'data/jobs.csv, data/jobs_previous.csv, public/index.html, logs1/log.txt', allowEmptyArchive: false
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
                   
                    %PSCP_EXE% -i %SSH_KEY_PATH% %HTML_FILE% %VPS_USER%@%VPS_HOST%:%VPS_PATH%
              

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
