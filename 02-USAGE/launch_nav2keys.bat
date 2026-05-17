@echo off
title NavCon Keyboard Mapper v3.5.0
cd /d "%~dp0"

echo ============================================================
echo    NavCon Keyboard Mapper v3.5.0
echo ============================================================
echo.
echo [ATTENTION] Si vous lancez un jeu via STEAM :
echo   Le controleur virtuel est visible par Steam Input.
echo.
echo   Solution recommandee : HidHide
echo   1. Installer HidHide : https://github.com/nefarius/HidHide
echo   2. Whitelister python.exe dans HidHide
echo   3. Masquer le controleur Xbox 360 virtuel
echo.
echo   Alternative : Steam -^> Proprietes du jeu -^> Controleur
echo   -^> "Disable Steam Input"
echo.
echo ============================================================
echo.

python nav2keys.py
pause
