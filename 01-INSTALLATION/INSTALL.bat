@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

echo ============================================================
echo    NavCon Pack v3.6.0 - Verification systeme
echo    Navigation Controller -^> Clavier pour PC
echo ============================================================
echo.

REM === Verifier admin ===
echo [1/4] Verification des droits administrateur...
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [NON] Droits administrateur manquants.
    echo.
    echo Clic droit sur INSTALL.bat -^> "Executer en tant qu'administrateur"
    pause
    exit /b 1
)
echo [OK] Droits administrateur confirmes.
echo.

echo [2/4] Verification de Python...
python --version >nul 2>&1
if %errorlevel% neq 0 goto PY_NON
for /f "tokens=2" %%v in ('python --version 2^>^&1') do set pyver=%%v
echo [OK] Python %pyver% detecte.
echo.
goto PY_FIN

:PY_NON
echo [NON] Python non installe.
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

:PY_FIN

echo [3/4] Installation de pydirectinput...
pip install pydirectinput >nul 2>&1
if %errorlevel% neq 0 goto PIP_NON
echo [OK] pydirectinput installe.
echo.
goto PIP_FIN

:PIP_NON
echo [NON] Impossible d'installer pydirectinput.
echo Essayez : pip install pydirectinput
pause
exit /b 1

:PIP_FIN

echo [4/4] Verification des logiciels requis...
echo.

REM ============================================================
REM  ScpToolkit - requis
REM ============================================================
echo --- ScpToolkit ---
if exist "C:\Program Files\Nefarius Software Solutions\ScpToolkit\ScpService.exe" (
    echo [OK] ScpToolkit est installe.
    sc query Ds3Service >nul 2>&1
    if !errorlevel! equ 0 (
        echo [OK] Service Ds3Service present.
    ) else (
        echo [NON] Service Ds3Service non trouve.
        echo       Reinstallez ScpToolkit en cochant "DS3 Controller".
    )
) else (
    echo [NON] ScpToolkit n'est pas installe.
    echo.
    echo Installation manuelle requise :
    echo   1. Telechargez ScpToolkit v1.6.238 :
    echo      https://github.com/nefarius/ScpToolkit/releases/download/v1.6.238.16010/ScpToolkit_Setup.exe
    echo.
    echo   2. Lancez l'installateur et cochez :
    echo      [x] DS3 Controller
    echo      [x] ScpVBus
    echo.
    echo   3. Completez l'installation puis relancez ce script.
)
echo.

REM ============================================================
REM  HidHide - optionnel, recommande pour Steam
REM ============================================================
echo --- HidHide (optionnel - recommande pour Steam) ---
sc query HidHide >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Pilote HidHide installe.
    if exist "%ProgramFiles%\Nefarius Software Solutions\HidHide\x64\HidHideCLI.exe" (
        echo [OK] HidHideCLI detecte.
    ) else if exist "%ProgramFiles%\Nefarius Software Solutions\HidHide\HidHideCLI.exe" (
        echo [OK] HidHideCLI detecte.
    ) else (
        echo [NON] HidHideCLI.exe introuvable.
    )
) else (
    echo [NON] HidHide non installe.
    echo.
    echo Optionnel mais recommande pour empecher les conflits Steam Input.
    echo.
    echo Installation manuelle :
    echo   1. https://github.com/nefarius/HidHide/releases/latest
    echo   2. Installez le pilote
    echo   3. REDEMARREZ le PC
    echo   4. Configurez avec launch_nav2keys.bat (admin)
)
echo.

echo ============================================================
echo    Verification terminee !
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
set /p choice="Souhaitez-vous creer un raccourci sur le Bureau ? (O/N) : "
if /i "%choice%"=="O" (
    powershell -NoProfile -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut([Environment]::GetFolderPath('Desktop') + '\NavCon Keyboard Mapper.lnk'); $Shortcut.TargetPath = '%~dp0..\02-USAGE\launch_nav2keys.bat'; $Shortcut.WorkingDirectory = '%~dp0..\02-USAGE'; $Shortcut.Description = 'NavCon Keyboard Mapper v3.6.0'; $Shortcut.Save()"
    echo [OK] Raccourci cree sur le Bureau !
)
echo.
pause
