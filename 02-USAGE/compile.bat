@echo off
title NavCon - Compilation
cd /d "%~dp0"
echo Compilation de NavCon...
dotnet build NavCon\NavCon.csproj -c Release >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Compilation reussie !
    copy /y "NavCon\bin\Release\net9.0-windows\NavCon.exe" "NavCon.exe" >nul 2>&1
    if exist "NavCon.exe" echo [OK] Copie vers NavCon.exe
) else (
    echo [NON] Echec de la compilation.
    echo Verifiez que .NET 9.0 SDK est installe : dotnet --version
)
pause
