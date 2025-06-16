stage('DetectChanges') {
    steps {
        echo "Détection de changements"
        bat '''
            setlocal enabledelayedexpansion
            
            REM Créer le dossier my-logs s'il n'existe pas, sinon continuer
            if not exist my-logs\\nul (
                mkdir my-logs
            )

            if not exist data\\jobs_previous.csv (
                copy data\\jobs.csv data\\jobs_previous.csv >nul
                echo [%date% %time%] Première exécution, création jobs_previous.csv >> my-logs\\log.txt
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
                echo [%date% %time%] Aucune nouvelle offre. >> my-logs\\log.txt
            ) else (
                echo [%date% %time%] Nouvelle offre détectée ! À consulter. >> my-logs\\log.txt
                copy /Y data\\jobs.csv data\\jobs_previous.csv >nul
            )
            endlocal
            exit /b 0
        '''
    }
}
