================================================================
  NavCon Pack v3.6.0 - Instructions d'Installation
================================================================

PREREQUIS
---------
- Windows 10/11 (64-bit)
- Python 3.12+ (https://www.python.org/downloads/)
  -> COCHEZ "Add Python to PATH" lors de l'installation
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
   [ ] DualShock 3             <-- OPTIONNEL (pas necessaire pour Nav Controller)
   [ ] Xbox 360 Controller     <-- NE PAS COCHER (inutile)

4. Completez l'installation

5. IMPORTANT : Apres l'installation, redemarrez votre PC

INSTALLATION DU PACK
-------------------
1. Clic droit sur INSTALL.bat -> "Executer en tant qu'administrateur"
2. Le script va :
   - Verifier Python
   - Installer pydirectinput
   - Verifier que ScpToolkit est installe
   - Redemarrer le service Ds3Service
   - (Optionnel) Installer/Configurer HidHide pour les jeux Steam
3. Si ScpToolkit n'est pas detecte, le script s'arrete avec instructions

APRES INSTALLATION
------------------
1. Aller dans le dossier 02-USAGE
2. Allumer le Navigation Controller
3. Double-cliquer sur launch_nav2keys.bat
4. Lancer votre jeu

CONFIGURATION
-------------
Pour modifier le mapping des touches :
1. Aller dans 02-USAGE
2. Double-cliquer sur configurator.bat
3. Modifier les touches et sauvegarder

MISE A JOUR
-----------
Pour mettre a jour vers une nouvelle version :
1. Telecharger le nouveau pack depuis GitHub
2. Remplacer le contenu de 02-USAGE (conservez config.json si vous voulez garder vos parametres)
3. Remplacer README.md et MANUEL.txt
4. Relancer INSTALL.bat uniquement pour verifier pydirectinput

HidHide (pour les jeux Steam)
-----------------------------
Depuis v3.6.0, HidHide est configure automatiquement :
  - INSTALL.bat etape 5 : Detecte si HidHide est installe.
    Si oui, configure python.exe en whitelist et active le masquage.
    Si non, propose de telecharger et d'installer HidHide.
  - launch_nav2keys.bat : Reconfigure HidHide a chaque lancement.

Aucune configuration manuelle necessaire.

Voir MANUEL.txt section "SOLUTION RECOMMANDEE : HidHide"
pour les details et la configuration manuelle si besoin.

Auteurs : ienien et OpenCode (IA)
