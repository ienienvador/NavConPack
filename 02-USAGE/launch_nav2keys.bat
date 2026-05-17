@echo off
title NavCon Keyboard Mapper v3.4.0
cd /d "%~dp0"

echo ============================================================
echo    NavCon Keyboard Mapper v3.3.0
echo ============================================================
echo.
echo [ATTENTION] Si vous lancez un jeu via STEAM :
echo   Steam Input doit etre desactive pour ce jeu,
echo   sinon la manette et le clavier entreront en conflit.
echo.
echo   Steam -^> Bibliotheque -^> Proprietes du jeu -^> Controleur
echo   -^> "Disable Steam Input"
echo.
echo ============================================================
echo.

python nav2keys.py
pause
