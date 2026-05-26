@echo off
setlocal enabledelayedexpansion
title NavCon Keyboard Mapper v3.6.0
cd /d "%~dp0"

echo ============================================================
echo    NavCon Keyboard Mapper v3.6.0
echo ============================================================
echo.

REM === Detection de l'emplacement de HidHideCLI ===
set HIDCLI=
if exist "%ProgramFiles%\Nefarius Software Solutions\HidHide\x64\HidHideCLI.exe" set HIDCLI=%ProgramFiles%\Nefarius Software Solutions\HidHide\x64\HidHideCLI.exe
if exist "%ProgramFiles%\Nefarius Software Solutions\HidHide\HidHideCLI.exe" set HIDCLI=%ProgramFiles%\Nefarius Software Solutions\HidHide\HidHideCLI.exe

if not defined HIDCLI goto NO_HIDHIDE

echo [HidHide] Detection en cours...
net session >nul 2>&1
if !errorlevel! neq 0 goto NO_ADMIN

echo [HidHide] Droits admin detectes. Configuration en cours...

"!HIDCLI!" --inv-on >nul 2>&1
if !errorlevel! equ 0 ( echo [OK] Mode inverse active ) else ( echo [NON] Activation mode inverse echouee )

for /f "tokens=*" %%p in ('where python 2^>nul') do (
    "!HIDCLI!" --app-reg "%%p" >nul 2>&1
    if !errorlevel! equ 0 ( echo [OK] %%p autorise ) else ( echo [NON] Echec whitelist %%p )
)

"!HIDCLI!" --cloak-on >nul 2>&1
if !errorlevel! equ 0 ( echo [OK] Masquage active ) else ( echo [NON] Activation masquage echouee )

echo [HidHide] Configuration terminee - Steam ne verra pas le controleur.
echo.
goto RUN_NAV2KEYS

:NO_ADMIN
echo [HidHide] Droits admin manquants - configuration deja appliquee par INSTALL.bat.
echo.
goto RUN_NAV2KEYS

:NO_HIDHIDE
echo [ATTENTION] HidHide non installe - le controleur sera visible par Steam Input.
echo.
echo   Solution : installer HidHide via 01-INSTALLATION\INSTALL.bat (admin)
echo   Alternative : Steam -^> Proprietes du jeu -^> Controleur -^> "Disable Steam Input"
echo.

:RUN_NAV2KEYS
echo ============================================================
echo.

REM === Menu de sélection du preset ===
set PRESET_COUNT=0
for %%f in ("%~dp0presets\*.json") do (
    set /a PRESET_COUNT+=1
    set "PRESET_!PRESET_COUNT!=%%~nf"
)

if !PRESET_COUNT! gtr 0 (
    echo Presets disponibles :
    echo.
    for /l %%i in (1,1,!PRESET_COUNT!) do (
        echo   %%i. !PRESET_%%i!
    )
    echo.
    set CHOICE=
    set /p CHOICE="Choisissez un numero (1-!PRESET_COUNT!) ou Entree pour le config actuel : "
    echo.
    if defined CHOICE (
        for %%i in (!CHOICE!) do set "PRESET_NAME=!PRESET_%%i!"
        if defined PRESET_NAME (
            echo [Preset] Lancement avec le preset : !PRESET_NAME!
            echo.
            python nav2keys.py "!PRESET_NAME!"
        ) else (
            echo [Preset] Choix invalide. Utilisation de config.json actuel.
            echo.
            python nav2keys.py
        )
    ) else (
        echo [Preset] Utilisation de config.json actuel
        echo.
        python nav2keys.py
    )
) else (
    echo [Preset] Aucun preset trouve. Utilisation de config.json actuel.
    echo.
    python nav2keys.py
)
pause
