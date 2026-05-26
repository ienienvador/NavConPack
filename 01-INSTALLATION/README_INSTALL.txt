===============================================================
  NavCon Pack v3.6.0 - Instructions d'Installation
===============================================================

PREREQUIS
---------
- Windows 10/11 (64-bit)
- Python 3.12+ (https://www.python.org/downloads/)
  -> COCHEZ "Add Python to PATH" lors de l'installation
- .NET 9.0 SDK (https://dotnet.microsoft.com/fr-fr/download/dotnet/9.0)
- ScpToolkit installe MANUELLEMENT (voir ci-dessous)
- Navigation Controller Sony (PS Move)

INSTALLATION DE SCPToolkit (A FAIRE AVANT INSTALL.BAT)
------------------------------------------------------
1. Telechargez ScpToolkit v1.6.238 :
   https://github.com/nefarius/ScpToolkit/releases/download/v1.6.238.16010/ScpToolkit_Setup.exe

2. Lancez ScpToolkit_Setup.exe

3. Lors de la selection des composants, cochez UNIQUEMENT :
   [x] DS3 Controller          <-- OBLIGATOIRE (inclut Navigation Controller)
   [x] ScpVBus                 <-- OBLIGATOIRE (bus virtuel Xbox 360)
   [ ] DualShock 3             <-- OPTIONNEL
   [ ] Xbox 360 Controller     <-- NE PAS COCHER

4. Completez l'installation

5. IMPORTANT : Apres l'installation, redemarrez votre PC

HidHide (optionnel, recommande pour les jeux Steam)
---------------------------------------------------
Lien : https://github.com/nefarius/HidHide/releases/latest
- Installez, redemarrez
- NavCon.exe configure automatiquement HidHide au lancement

INSTALLATION DU PACK
--------------------
1. Clic droit sur INSTALL.bat -> "Executer en tant qu'administrateur"
2. Le script verifie :
   - Python
   - pydirectinput (pip install)
   - ScpToolkit installe
   - HidHide installe
3. Aucune installation automatique de ScpToolkit/HidHide
   -> Ils doivent etre installes manuellement avant

COMPILATION ET LANCEMENT
-------------------------
1. Ouvrir 02-USAGE
2. Lancer compile.bat (compile NavCon.exe avec .NET 9.0)
3. Lancer bin\NavCon.exe (administrateur)
4. Choisir un preset, cliquer Demarrer

CONFIGURATION
-------------
Cliquer "Configurer" dans NavCon.exe pour modifier le mapping :
  - 5 onglets : Boutons, Trigger L2, Stick, Presets, Test
  - Sauvegarder dans config.json

MISE A JOUR
-----------
1. Telecharger le nouveau pack depuis GitHub
2. Remplacer le contenu de 02-USAGE (conservez config.json si besoin)
3. Recompiler avec compile.bat

Auteurs : ienien et OpenCode (IA)
