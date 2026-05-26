@echo off
title NavCon - Compilation
cd /d "%~dp0"
echo Compilation de NavCon...

REM Publie l'application dans le dossier bin/ (exe + dll + config)
dotnet publish NavCon\NavCon.csproj -c Release -o "bin" >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Compilation reussie !
    echo L executable se trouve dans : bin\NavCon.exe
    echo.
    echo Pour lancer : bin\NavCon.exe
) else (
    echo [NON] Echec de la compilation.
    echo Verifiez que .NET 9.0 SDK est installe : dotnet --version
)
pause
