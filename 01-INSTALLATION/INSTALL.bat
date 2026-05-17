@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

echo ============================================================
echo    NavCon Pack v3.4.0 - Installation Complete
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

echo [1/4] Verification de Python...
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

echo [2/4] Installation de pydirectinput...
pip install pydirectinput >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERREUR] Impossible d'installer pydirectinput.
    echo Essayez : pip install pydirectinput
    pause
    exit /b 1
)
echo pydirectinput installe. OK.
echo.

echo [3/4] Verification de ScpToolkit...
if exist "C:\Program Files\Nefarius Software Solutions\ScpToolkit\ScpService.exe" (
    echo ScpToolkit detecte. OK.
) else (
    echo [ERREUR] ScpToolkit n'est pas installe.
    echo.
    echo ScpToolkit doit etre installe MANUELLEMENT avant de continuer.
    echo.
    echo 1. Telechargez ScpToolkit v1.6.238 :
    echo    https://github.com/nefarius/ScpToolkit/releases/download/v1.6.238.16010/ScpToolkit_Setup.exe
    echo.
    echo 2. Lancez l'installateur et cochez :
    echo    [x] DS3 Controller
    echo    [x] ScpVBus
    echo    [ ] DualShock 3 (optionnel, pas necessaire pour Nav Controller)
    echo.
    echo 3. Completez l'installation puis relancez ce script.
    echo.
    pause
    exit /b 1
)
echo.

echo [4/4] Redemarrage du service ScpService...
sc query Ds3Service >nul 2>&1
if %errorlevel% equ 0 (
    echo Service Ds3Service present. Redemarrage...
) else (
    echo [ERREUR] Service Ds3Service non trouve.
    echo ScpToolkit n'est peut-etre pas installe correctement.
    echo Relancez l'installateur ScpToolkit et cochez "DS3 Controller".
    pause
    exit /b 1
)
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
    powershell -NoProfile -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut([Environment]::GetFolderPath('Desktop') + '\NavCon Keyboard Mapper.lnk'); $Shortcut.TargetPath = '%~dp0..\02-USAGE\launch_nav2keys.bat'; $Shortcut.WorkingDirectory = '%~dp0..\02-USAGE'; $Shortcut.Description = 'NavCon Keyboard Mapper v3.4.0'; $Shortcut.Save()"
    echo Raccourci cree sur le Bureau !
)
echo.
pause
