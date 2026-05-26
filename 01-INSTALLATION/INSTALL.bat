@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

echo ============================================================
echo    NavCon Pack v3.6.0 - Installation Complete
echo    Navigation Controller -^> Clavier pour PC
echo ============================================================
echo.

REM === Verifier admin ===
echo [1/5] Verification des droits administrateur...
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

echo [2/5] Verification de Python...
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

echo [3/5] Installation de pydirectinput...
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

echo [4/5] Verification de ScpToolkit...
if not exist "C:\Program Files\Nefarius Software Solutions\ScpToolkit\ScpService.exe" goto SCP_NON
echo [OK] ScpToolkit detecte.

echo [4/5] Redemarrage du service ScpService...
sc query Ds3Service >nul 2>&1
if %errorlevel% neq 0 goto DSC_NON
echo [OK] Service Ds3Service present. Arret en cours...

REM Arreter le service et tuer les processus Scp
net stop Ds3Service >nul 2>&1
taskkill /f /im ScpTrayApp.exe >nul 2>&1
taskkill /f /im ScpServer.exe >nul 2>&1
taskkill /f /im ScpMonitor.exe >nul 2>&1

REM Nettoyer la base DBreeze (parfois verrouillee par ScpTrayApp)
set SCPDB=%ProgramFiles%\Nefarius Software Solutions\ScpToolkit\Db
if exist "%SCPDB%\_DBreezeSchema" (
    del /f /q "%SCPDB%\_DBreezeSchema" >nul 2>&1
    del /f /q "%SCPDB%\_DBreezeSchema.rhp" >nul 2>&1
    del /f /q "%SCPDB%\_DBreezeSchema.rol" >nul 2>&1
    del /f /q "%SCPDB%\_DBreezeTranJrnl" >nul 2>&1
    del /f /q "%SCPDB%\_DBreezeTranJrnl.rhp" >nul 2>&1
    del /f /q "%SCPDB%\_DBreezeTranJrnl.rol" >nul 2>&1
)
timeout /t 2 /nobreak >nul

REM Demarrer le service
net start Ds3Service >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Service Ds3Service demarre.
) else (
    echo [NON] Echec demarrage Ds3Service.
    echo       Utilisez ScpSettings.exe pour reconfigurer.
)
echo.
goto HID_START

:SCP_NON
echo [NON] ScpToolkit n'est pas installe.
echo.
echo ScpToolkit doit etre installe MANUELLEMENT avant de continuer.
echo.
echo 1. Telechargez ScpToolkit v1.6.238 :
echo    https://github.com/nefarius/ScpToolkit/releases/download/v1.6.238.16010/ScpToolkit_Setup.exe
echo.
echo 2. Lancez l'installateur et cochez :
echo    [x] DS3 Controller
echo    [x] ScpVBus
echo    [ ] DualShock 3
echo.
echo 3. Completez l'installation puis relancez ce script.
echo.
pause
exit /b 1

:DSC_NON
echo [NON] Service Ds3Service non trouve.
echo ScpToolkit n'est peut-etre pas installe correctement.
echo Relancez l'installateur ScpToolkit et cochez DS3 Controller.
pause
exit /b 1

REM ============================================================
REM  HidHide - optionnel, recommande pour Steam
REM ============================================================
:HID_START
echo [5/5] Installation et configuration de HidHide - optionnel, recommande pour Steam...
echo.
echo =================================================================
echo   Pourquoi HidHide ?
echo =================================================================
echo.
echo   Steam Input intercepte toutes les manettes XInput, y compris
echo   le controleur Xbox 360 virtuel cree par ScpVBus. Cela cree
echo   un conflit manette/clavier dans les jeux.
echo.
echo   HidHide est un pare-feu de peripheriques d'entree qui permet :
echo.
echo     1. MASQUER le controleur virtuel a Steam et aux jeux
echo     2. AUTORISER python.exe a voir le controleur
echo.
echo   Site officiel : https://github.com/nefarius/HidHide
echo   Notre version : traduction francaise depuis les sources
echo =================================================================
echo.

set HIDDIR=%ProgramFiles%\Nefarius Software Solutions\HidHide\x64
set HIDROOT=%ProgramFiles%\Nefarius Software Solutions\HidHide
set FRENCH_CLI=%~dp0..\HidHide\bin\Release\x64\HidHideCLI.exe
set FRENCH_CLIENT=%~dp0..\HidHide\bin\Release\x64\HidHideClient.exe

echo --- Etape 1 : Detection de HidHide ---
sc query HidHide >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Service pilote HidHide detecte.
    echo [OK] HidHide deja installe sur ce PC.
    echo.
    goto HID_INSTALLED
)

echo [NON] Service pilote HidHide non trouve.
echo.
goto HID_NOT_INSTALLED

:HID_INSTALLED

echo --- Etape 2 : Verification des fichiers ---
if exist "%HIDDIR%\HidHideCLI.exe" ( echo [OK] HidHideCLI.exe present dans %HIDDIR% ) else ( echo [NON] HidHideCLI.exe manquant )
if exist "%HIDDIR%\HidHideClient.exe" ( echo [OK] HidHideClient.exe present ) else ( echo [NON] HidHideClient.exe manquant )
if exist "%HIDROOT%\HidHide.sys" ( echo [OK] Pilote HidHide.sys present ) else ( echo [NON] Pilote HidHide.sys manquant )
echo.

echo --- Etape 3 : Mise a jour vers la version francaise ---
if not exist "%FRENCH_CLI%" goto FR_NON
copy /y "%FRENCH_CLI%" "%HIDDIR%\HidHideCLI.exe" >nul 2>&1
if %errorlevel% equ 0 ( echo [OK] HidHideCLI.exe mis a jour - version francaise ) else ( echo [NON] Echec copie HidHideCLI.exe )
copy /y "%FRENCH_CLIENT%" "%HIDDIR%\HidHideClient.exe" >nul 2>&1
if %errorlevel% equ 0 ( echo [OK] HidHideClient.exe mis a jour - version francaise ) else ( echo [NON] Echec copie HidHideClient.exe )
goto FR_FIN

:FR_NON
echo [NON] Version francaise compilee introuvable
echo [OK] Utilisation de la version anglaise officielle

:FR_FIN
echo.

echo --- Etape 4 : Configuration de HidHide ---
if not exist "%HIDDIR%\HidHideCLI.exe" goto CLI_MANQUANT
"%HIDDIR%\HidHideCLI.exe" --inv-on >nul 2>&1
if %errorlevel% equ 0 ( echo [OK] Mode inverse active ) else ( echo [NON] Echec activation mode inverse )

for /f "tokens=*" %%p in ('where python 2^>nul') do (
    "%HIDDIR%\HidHideCLI.exe" --app-reg "%%p" >nul 2>&1
    if %errorlevel% equ 0 ( echo [OK] %%p autorise ) else ( echo [NON] Echec whitelist %%p )
)

"%HIDDIR%\HidHideCLI.exe" --cloak-on >nul 2>&1
if %errorlevel% equ 0 ( echo [OK] Masquage active ) else ( echo [NON] Echec activation masquage )
goto CLI_OK

:CLI_MANQUANT
echo [NON] HidHideCLI.exe introuvable dans %HIDDIR%
echo Configurez manuellement via : Demarrer -^> HidHide Configuration Client

:CLI_OK
echo.

echo --- Etape 5 : Verification de la configuration ---
if exist "%HIDDIR%\HidHideCLI.exe" (
    "%HIDDIR%\HidHideCLI.exe" --cloak-state
    "%HIDDIR%\HidHideCLI.exe" --inv-state
    "%HIDDIR%\HidHideCLI.exe" --app-list
)
echo [OK] Configuration HidHide terminee.
echo.
goto HID_FIN

:HID_NOT_INSTALLED
echo --- Optionnel : Installation de HidHide ---
echo.
set /p choice="Souhaitez-vous installer HidHide ? (O/N) : "
if /i "!choice!"=="O" goto HID_INSTALL_OUI
echo [NON] Installation ignoree
echo.
echo Alternatives si conflit Steam Input :
echo   - Relancez ce script pour installer HidHide
echo   - Desactiver Steam Input par jeu : Proprietes -^> Controleur
goto HID_FIN

:HID_INSTALL_OUI
echo.
echo --- Etape 1 : Telechargement de HidHide ---
echo Source : https://github.com/nefarius/HidHide/releases
echo.
powershell -NoProfile -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://github.com/nefarius/HidHide/releases/latest/download/HidHide_Setup.exe' -OutFile '%TEMP%\HidHide_Setup.exe'"
if not exist "%TEMP%\HidHide_Setup.exe" goto DL_NON
echo [OK] Installateur telecharge
echo.
echo --- Etape 2 : Installation du pilote ---
echo IMPORTANT : Suivez les instructions a l'ecran.
echo            REDEMARREZ le PC apres l'installation.
echo.
"%TEMP%\HidHide_Setup.exe"
echo.
echo --- Etape 3 : Installation de l'interface francaise ---
if not exist "%FRENCH_CLI%" goto FR_NON2
if not exist "%HIDDIR%\" goto DIR_NON
copy /y "%FRENCH_CLI%" "%HIDDIR%\HidHideCLI.exe" >nul 2>&1
if %errorlevel% equ 0 ( echo [OK] HidHideCLI.exe francais installe ) else ( echo [NON] Echec copie )
copy /y "%FRENCH_CLIENT%" "%HIDDIR%\HidHideClient.exe" >nul 2>&1
if %errorlevel% equ 0 ( echo [OK] HidHideClient.exe francais installe ) else ( echo [NON] Echec copie )
goto INSTALL_FIN

:DIR_NON
echo [NON] %HIDDIR% introuvable - l'installateur a-t-il echoue ?
goto INSTALL_FIN

:FR_NON2
if not exist "%FRENCH_CLI%" echo [NON] Version francaise non disponible - interface anglaise utilisee
goto INSTALL_FIN

:DL_NON
echo [NON] Echec du telechargement
echo.
echo Telechargez manuellement depuis :
echo   https://github.com/nefarius/HidHide/releases

:INSTALL_FIN
echo.
echo ================================================================
echo   INSTALLATION DE HIDHIDE TERMINEE
echo ================================================================
echo.
echo   ETAPES SUIVANTES :
echo     1. REDEMARREZ votre PC obligatoire
echo     2. Relancez INSTALL.bat en administrateur
echo     3. La configuration se fera automatiquement
echo.

:HID_FIN
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
set /p choice="Souhaitez-vous creer un raccourci sur le Bureau ? (O/N) : "
if /i "%choice%"=="O" (
    powershell -NoProfile -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut([Environment]::GetFolderPath('Desktop') + '\NavCon Keyboard Mapper.lnk'); $Shortcut.TargetPath = '%~dp0..\02-USAGE\launch_nav2keys.bat'; $Shortcut.WorkingDirectory = '%~dp0..\02-USAGE'; $Shortcut.Description = 'NavCon Keyboard Mapper v3.6.0'; $Shortcut.Save()"
    echo [OK] Raccourci cree sur le Bureau !
)
echo.
pause
