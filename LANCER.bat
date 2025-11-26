@echo off
REM Script de lancement rapide pour Windows
REM Double-cliquez sur ce fichier pour lancer l'application

echo ========================================
echo   Application Dossier Patient
echo   Demarrage en cours...
echo ========================================
echo.

REM Activer l'environnement virtuel
call venv\Scripts\activate.bat

if errorlevel 1 (
    echo ERREUR: Impossible d'activer l'environnement virtuel
    echo Assurez-vous d'etre dans le bon dossier
    pause
    exit /b 1
)

echo [OK] Environnement virtuel active
echo.

REM Lancer l'application
echo Lancement de l'application...
echo Appuyez sur Ctrl+C pour arreter le serveur
echo.
echo URL: http://localhost:8000
echo.

python app.py

pause

