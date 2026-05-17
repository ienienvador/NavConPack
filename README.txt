================================================================
  NavCon Pack v3.0 - Navigation Controller -> Clavier
  Pack complet déployable
================================================================

AUTEURS & COLLABORATION
-----------------------
Ce projet a été développé en collaboration entre :
  - [Votre Nom] : conception, tests en jeu, validation du mapping
  - OpenCode (IA) : développement du script, debugging, optimisation

Recherche et développement effectués ensemble sur plusieurs sessions
de tests, incluant le diagnostic des drivers, la résolution des
conflits manette/clavier, et l'adaptation pour les jeux PC.

Ce pack est le résultat d'une recherche approfondie pour trouver
une solution fonctionnelle sans utiliser reWASD (banni par EAC).


PRÉREQUIS
---------
- Windows 10/11 (64-bit)
- Python 3.12+ (https://www.python.org/downloads/)
  -> COCHEZ "Add Python to PATH" lors de l'installation
- Navigation Controller Sony (PS Move)
- ScpToolkit (téléchargé automatiquement depuis github.com/nefarius/ScpToolkit)

INSTALLATION (une seule fois)
------------------------------
1. Copier le dossier NavConPack sur le nouveau PC
2. Clic droit sur INSTALL.bat -> "Exécuter en tant qu'administrateur"
3. Suivre les étapes (Python -> pydirectinput -> ScpToolkit -> Driver)
4. Redémarrer le PC

UTILISATION QUOTIDIENNE
-----------------------
1. Allumer le Navigation Controller (USB ou Bluetooth)
2. Double-cliquer sur launch_nav2keys.bat
3. La console affiche "Controller détecté sur slot X"
4. Lancer votre jeu - la manette agit comme un clavier

UTILISATION DU MAPPING
----------------------
Le script nav2keys.py traduit chaque bouton du Navigation Controller
en une touche clavier. Le jeu reçoit uniquement des frappes clavier,
jamais de signaux de manette.

Comment ça marche :
  1. ScpService détecte la manette et crée un contrôleur Xbox 360 virtuel
  2. nav2keys.py lit ce contrôleur virtuel via XInput
  3. Chaque appui sur un bouton est converti en touche clavier
  4. Le jeu reçoit la touche comme si vous tapiez au clavier

Important :
  - NE PAS utiliser AntiMicroX en même temps (conflit)
  - La console doit rester ouverte pendant le jeu
  - Pour arrêter : Ctrl+C dans la console ou fermer la fenêtre
  - Si une touche reste bloquée : Ctrl+C pour tout relâcher

MAPPING PAR DÉFAUT
------------------
  Bouton Nav        Touche    Action (exemple)
  ───────────────── ───────── ──────────────────────
  Stick Gauche      WASD      Déplacement
  L3 (clic stick)   Shift     Sprint
  Cross (X)         Espace    Saut
  Circle (O)        C         S'accroupir
  Square ([])       R         Recharger
  Triangle (A)      2         Arme secondaire
  L1                Q         Action rapide
  R1                G         Grenade / Objet
  L2 (trigger)      X         Action alternative
  R2 (trigger)      E         Interagir
  Select            Tab       Scoreboard / Menu
  Start             Échap     Pause
  D-Pad Haut        3         Slot 3
  D-Pad Bas         4         Slot 4
  D-Pad Gauche      1         Slot 1
  D-Pad Droite      F         Interaction
  R3 (clic stick)   V         Mêlée / Action

Notes sur les triggers :
  - L2 et R2 sont analogiques (pression progressive)
  - Le seuil de déclenchement est à 80/255 (30 %)
  - Appuyez à fond pour une réponse immédiate
  - Si le seuil ne vous convient pas, modifiez TRIGGER_THRESHOLD
    dans nav2keys.py (ligne 56)

Notes sur le stick :
  - La deadzone est à 7849 (sur 32767)
  - Si le stick est trop sensible ou pas assez, modifiez DZ
    dans nav2keys.py (ligne 55)

MODIFIER LE MAPPING
-------------------
Ouvrir nav2keys.py avec un éditeur de texte (Bloc-notes, VSCode, etc.)

Le dictionnaire MAP (ligne 29) définit les correspondances :
  MAP = {
      0x1000: 'space',    # Cross -> Espace
      0x2000: 'c',        # Circle -> C
      0x4000: 'r',        # Square -> R
      ...
  }

Format : 0xXXXX: 'nom_touche'
  - 0xXXXX = code du bouton XInput (ne pas modifier sauf si vous
    savez ce que vous faites)
  - 'nom_touche' = nom de la touche pydirectinput

Noms de touches valides :
  - Lettres : 'a' à 'z'
  - Chiffres : '1' à '9', '0'
  - Spéciales : 'space', 'tab', 'esc', 'enter', 'shift', 'ctrl',
    'alt', 'backspace', 'delete', 'insert', 'home', 'end'
  - F1 à F12 : 'f1' à 'f12'
  - Flèches : 'left', 'right', 'up', 'down'

Exemple - changer L1 de Q à E :
  Avant : 0x0100: 'q',
  Après : 0x0100: 'e',

Sauvegarder le fichier et relancer launch_nav2keys.bat.

DÉPANNAGE
---------
"Python n'est pas installé"
  -> Télécharger Python depuis python.org
  -> COCHER "Add Python to PATH"
  -> Relancer INSTALL.bat

"Controller not found"
  -> Vérifier que ScpService tourne (services.msc -> SCP DSx Service)
  -> Rebrancher le controller
  -> Redémarrer le PC

"Touches bloquées"
  -> Ctrl+C dans la console pour tout relâcher

"L2 ne répond pas"
  -> Seuil à 80, appuyer à fond sur le trigger
  -> Modifier TRIGGER_THRESHOLD dans nav2keys.py si besoin

"Le jeu voit encore la manette"
  -> Fermer AntiMicroX complètement (clic droit -> Quitter)
  -> nav2keys.py remplace AntiMicroX, ne pas utiliser les deux

CONTENU DU PACK
---------------
  NavConPack/
  ├── INSTALL.bat              Installation complète (admin)
  ├── launch_nav2keys.bat      Lancement quotidien
  ├── nav2keys.py              Script de mapping v2.3
  └── README.txt               Ce fichier
