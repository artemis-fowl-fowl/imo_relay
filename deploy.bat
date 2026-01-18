@echo off
REM Script de déploiement pour Windows

echo.
echo 🚀 Preparation du deploiement...
echo.

REM 1. Verifier la structure
echo 🔍 Verification de la structure...
echo.

setlocal enabledelayedexpansion

set "files[0]=README.md"
set "files[1]=LICENSE"
set "files[2]=CHANGELOG.md"
set "files[3]=hacs.json"
set "files[4]=custom_components\imo_relay\manifest.json"
set "files[5]=custom_components\imo_relay\__init__.py"
set "files[6]=custom_components\imo_relay\modbus_client.py"
set "files[7]=custom_components\imo_relay\switch.py"

for /L %%i in (0,1,7) do (
    if exist "!files[%%i]!" (
        echo ✅ !files[%%i]!
    ) else (
        echo ❌ !files[%%i]! - MANQUANT
    )
)

echo.
echo.
echo ==========================================
echo 📋 PROCHAINES ÉTAPES:
echo ==========================================
echo.
echo 1️⃣  Creer un repo sur GitHub:
echo    https://github.com/new
echo    Name: imo_relay
echo    Public: YES
echo    License: MIT
echo.
echo 2️⃣  Pousser le code:
echo    git remote add origin https://github.com/VOTRE_USERNAME/imo_relay.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo 3️⃣  Ajouter des tags (optionnel):
echo    git tag -a v1.0.0 -m "Release 1.0.0"
echo    git push origin v1.0.0
echo.
echo 4️⃣  Soumettre a HACS:
echo    https://hacs.xyz/docs/publish/integration
echo    Ou ajouter en tant que repo personnel via HACS UI
echo.
echo ==========================================
echo ✨ C'est pret pour le deploiement!
echo ==========================================
echo.

pause
