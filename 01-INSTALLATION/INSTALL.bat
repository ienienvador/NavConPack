@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

echo ============================================================
echo    NavCon Pack v3.3.0 - Installation Complete
echo    Navigation Controller -^> Clavier pour PC
echo ============================================================
echo.

REM === Verifier admin ===
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERREUR] Ce script doit etre execute en administrateur.
    echo Clic droit sur INSTALL.bat -^> "Executer en tant qu'administrateur"
    pause
    exit /b 1
)

echo [1/5] Verification de Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python non installe.
    echo.
    echo Telechargez Python 3.12+ depuis :
    echo   https://www.python.org/downloads/
    echo.
    echo IMPORTANT : Cochez "Add Python to PATH" lors de l'installation.
    echo.
    echo Appuyez sur une touche pour ouvrir la page de telechargement...
    pause >nul
    start https://www.python.org/downloads/
    echo.
    echo Une fois Python installe, relancez ce script.
    pause
    exit /b 1
)

for /f "tokens=2" %%v in ('python --version 2^>^&1') do set pyver=%%v
echo Python %pyver% detecte. OK.
echo.

echo [2/5] Installation de pydirectinput...
pip install pydirectinput >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERREUR] Impossible d'installer pydirectinput.
    echo Essayez : pip install pydirectinput
    pause
    exit /b 1
)
echo pydirectinput installe. OK.
echo.

echo [3/5] Verification de ScpToolkit...
set "SCP_FRESH_INSTALL=0"
if exist "C:\Program Files\Nefarius Software Solutions\ScpToolkit\ScpService.exe" (
    echo ScpToolkit deja installe. OK.
    echo Aucune reinstallation necessaire.
    echo Les drivers existants seront preserves.
) else (
    set "SCP_FRESH_INSTALL=1"
    echo ScpToolkit non installe. Telechargement depuis la source officielle...
    echo Source : https://github.com/nefarius/ScpToolkit
    echo.
    
    set "SCP_URL=https://github.com/nefarius/ScpToolkit/releases/download/v1.6.238.16010/ScpToolkit_Setup.exe"
    set "SCP_DL=%~dp0ScpToolkit_Setup.exe"
    
    echo Telechargement en cours...
    powershell -NoProfile -Command "Invoke-WebRequest -Uri '%SCP_URL%' -OutFile '%SCP_DL%' -UseBasicParsing"
    
    if exist "%SCP_DL%" (
        echo Telechargement termine. Lancement de l'installateur...
        echo Suivez les etapes de l'installateur.
        echo Cochez "DS3 Controller" et "ScpVBus" lors de l'installation.
        echo.
        start /wait "" "%SCP_DL%"
        del "%SCP_DL%" >nul 2>&1
        echo.
        echo ScpToolkit installe.
    ) else (
        echo [ERREUR] Telechargement echoue.
        echo.
        echo Telechargez ScpToolkit manuellement depuis :
        echo   https://github.com/nefarius/ScpToolkit/releases
        echo.
        pause
        exit /b 1
    )
)
echo.

echo [4/5] Configuration du driver Navigation Controller...
echo.

if "!SCP_FRESH_INSTALL!"=="1" (
    echo Premiere installation - configuration du driver...
    echo.
    
    set "SCP_PATH=C:\Program Files\Nefarius Software Solutions\ScpToolkit"
    echo Installation du driver DS3/Nav Controller...
    set "INF_PATH=!SCP_PATH!\Driver\Ds3Controller_a177e5d2-2e65-4087-bff1-65cf1933efdb.inf"
    
    if exist "!INF_PATH!" (
        pnputil /add-driver "!INF_PATH!" /install >nul 2>&1
        echo Driver installe. OK.
    ) else (
        echo [INFO] INF non trouve a l'emplacement standard.
        echo Le driver sera installe automatiquement par ScpToolkit au branchement.
    )
) else (
    echo ScpToolkit deja configure - drivers preserves.
    echo Aucune modification de driver necessaire.
)
echo.

echo [5/5] Redemarrage du service ScpService...
net stop Ds3Service >nul 2>&1
timeout /t 2 /nobreak >nul
net start Ds3Service >nul 2>&1
if %errorlevel% equ 0 (
    echo Service ScpService redemarre. OK.
) else (
    echo [INFO] Service non trouve. ScpToolkit n'est peut-etre pas installe correctement.
)
echo.

echo ============================================================
echo    Installation terminee !
echo ============================================================
echo.
echo Pour utiliser la manette :
echo   1. Allez dans le dossier 02-USAGE
echo   2. Allumez le Navigation Controller
echo   3. Double-cliquez sur launch_nav2keys.bat
echo   4. Lancez votre jeu
echo.
echo La manette agira comme un clavier dans le jeu.
echo.

REM === Creer un raccourci sur le Bureau ===
echo Souhaitez-vous creer un raccourci sur le Bureau ?
set /p choice="Oui/Non (O/N) : "
if /i "%choice%"=="O" (
    echo Creation du raccourci...
    powershell -NoProfile -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut([Environment]::GetFolderPath('Desktop') + '\NavCon Keyboard Mapper.lnk'); $Shortcut.TargetPath = '%~dp0..\02-USAGE\launch_nav2keys.bat'; $Shortcut.WorkingDirectory = '%~dp0..\02-USAGE'; $Shortcut.Description = 'NavCon Keyboard Mapper v3.3.0'; $Shortcut.Save()"
    echo Raccourci cree sur le Bureau !
)
echo.
pause
