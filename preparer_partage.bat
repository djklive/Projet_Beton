@echo off
echo ========================================
echo   Preparation du Package pour Partage
echo ========================================
echo.

REM Verifier que nous sommes dans le bon dossier
if not exist "app.py" (
    echo ERREUR: app.py introuvable!
    echo Assurez-vous d'executer ce script depuis le dossier du projet.
    pause
    exit /b 1
)

REM Creer le dossier de distribution
if exist "Projet_Patient_Distribution" (
    echo Suppression de l'ancien dossier...
    rmdir /s /q "Projet_Patient_Distribution"
)

echo Creation du dossier de distribution...
mkdir "Projet_Patient_Distribution"

echo.
echo Copie des fichiers...
echo.

REM Copier les fichiers Python
copy "app.py" "Projet_Patient_Distribution\" >nul
if errorlevel 1 (
    echo ERREUR: Impossible de copier app.py
    pause
    exit /b 1
)
echo [OK] app.py

REM Copier requirements.txt
copy "requirements.txt" "Projet_Patient_Distribution\" >nul
echo [OK] requirements.txt

REM Copier les fichiers SQL
copy "*.sql" "Projet_Patient_Distribution\" >nul
echo [OK] Fichiers SQL (*.sql)

REM Copier les fichiers de documentation
copy "*.md" "Projet_Patient_Distribution\" >nul
copy "*.txt" "Projet_Patient_Distribution\" >nul
echo [OK] Documentation (*.md, *.txt)

REM Copier les scripts batch
copy "*.bat" "Projet_Patient_Distribution\" >nul
echo [OK] Scripts (*.bat)

REM Copier config.py.example
if exist "config.py.example" (
    copy "config.py.example" "Projet_Patient_Distribution\" >nul
    echo [OK] config.py.example
)

echo.
echo ========================================
echo   Package prepare avec succes!
echo ========================================
echo.
echo Dossier cree: Projet_Patient_Distribution
echo.
echo PROCHAINES ETAPES:
echo 1. Verifiez le contenu du dossier Projet_Patient_Distribution
echo 2. Compressez ce dossier en .zip
echo 3. Partagez le fichier .zip avec votre ami
echo.
echo Appuyez sur une touche pour ouvrir le dossier...
pause >nul

REM Ouvrir le dossier dans l'explorateur
explorer "Projet_Patient_Distribution"

echo.
echo ========================================
echo   Operation terminee!
echo ========================================


