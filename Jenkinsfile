stage('Détection de changements') {
    steps {
        bat '''
            cd /d "%WORKSPACE%"

            rem -- Créer les dossiers si nécessaires
            if not exist data (
                mkdir data
            )
            if not exist logs (
                mkdir logs
                ping 127.0.0.1 -n 3 >nul
            )
            if not exist public (
                mkdir public
            )

            rem -- Créer un en-tête si log.txt n’existe pas
            if not exist "logs\\log.txt" (
                echo ===== Journal du pipeline Jenkins ===== > "logs\\log.txt"
            )

            rem -- Si première exécution, copie initiale
            if not exist "data\\jobs_previous.csv" (
                echo [%date% %time%] Première exécution : copie initiale >> "logs\\log.txt"
                copy "data\\jobs.csv" "data\\jobs_previous.csv"
                exit /b 0
            )

            rem -- Calcul des empreintes SHA256
            certutil -hashfile "data\\jobs.csv" SHA256 > new_hash.txt
            certutil -hashfile "data\\jobs_previous.csv" SHA256 > old_hash.txt

            for /f "tokens=1" %%A in (new_hash.txt) do set NEW_HASH=%%A
            for /f "tokens=1" %%A in (old_hash.txt) do set OLD_HASH=%%A

            if "%NEW_HASH%" == "%OLD_HASH%" (
                echo [%date% %time%] Aucune nouvelle offre détectée. >> "logs\\log.txt"
                exit /b 0
            ) else (
                echo [%date% %time%] Nouvelles offres détectées. >> "logs\\log.txt"
                copy /Y "data\\jobs.csv" "data\\jobs_previous.csv" >nul
                echo [%date% %time%] Rapport HTML mis à jour. >> "logs\\log.txt"
            )
        '''
    }
}
