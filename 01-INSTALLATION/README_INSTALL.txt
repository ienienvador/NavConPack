================================================================
  NavCon Pack v3.3.0 - Instructions d'Installation
================================================================

PREREQUIS
---------
- Windows 10/11 (64-bit)
- Python 3.12+ (https://www.python.org/downloads/)
  -> COCHEZ "Add Python to PATH" lors de l'installation
- Navigation Controller Sony (PS Move)

INSTALLATION
------------
1. Clic droit sur INSTALL.bat -> "Executer en tant qu'administrateur"
2. Le script va :
   - Verifier Python
   - Installer pydirectinput
   - Telecharger et installer ScpToolkit
   - Configurer le driver Navigation Controller
   - Redemarrer le service ScpService
3. Redemarrer le PC (recommande)

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
4. Relancer INSTALL.bat si la version ScpToolkit a change

Auteurs : ienien et OpenCode (IA)
