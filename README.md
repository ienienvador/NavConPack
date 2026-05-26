# NavCon Pack v3.6.0

## Navigation Controller → Clavier pour PC

Solution complète pour utiliser un **Sony Navigation Controller** (PS Move) sur PC Windows comme clavier. Compatible avec tous les jeux — aucune détection de manette parasite.

**Spécialisé Navigation Controller** : Cette version est optimisée exclusivement pour le Navigation Controller (demi-manette PS Move). Les boutons absents sur ce contrôleur (Square, Triangle, R1, R2, R3, Select) ont été retirés.

## Structure du Pack

```
NavConPack/
├── README.md                    ← Ce fichier
├── MANUEL.txt                   ← Documentation complète
├── 01-INSTALLATION/             ← Installation (une seule fois)
│   ├── INSTALL.bat
│   └── README_INSTALL.txt
└── 02-USAGE/                    ← Usage quotidien
    ├── launch_nav2keys.bat
    ├── configurator.bat
    ├── nav2keys.py
    ├── configurator.py
    ├── config.json
    └── presets/
```

## Installation (une seule fois)

1. **Installer ScpToolkit manuellement** (OBLIGATOIRE) :
   - Télécharger depuis : https://github.com/nefarius/ScpToolkit/releases/download/v1.6.238.16010/ScpToolkit_Setup.exe
   - Cocher **DS3 Controller** et **ScpVBus**
   - Redémarrer le PC
2. Ouvrir le dossier `01-INSTALLATION`
3. Clic droit sur `INSTALL.bat` → **Exécuter en tant qu'administrateur**
4. Le script vérifie Python, pydirectinput et ScpToolkit

Voir `01-INSTALLATION/README_INSTALL.txt` pour les instructions détaillées.

## Usage Quotidien

1. Ouvrir le dossier `02-USAGE`
2. Allumer le Navigation Controller (USB ou Bluetooth)
3. Double-cliquer sur `launch_nav2keys.bat`
4. La console affiche "Controller détecté sur slot X"
5. Lancer le jeu

## Configuration GUI

1. Ouvrir le dossier `02-USAGE`
2. Double-cliquer sur `configurator.bat`
3. Modifier le mapping visuellement
4. Sauvegarder → `config.json` mis à jour

## Mapping par défaut

| Bouton Nav | Touche | Action (exemple) |
|-----------|--------|------------------|
| Stick Gauche | WASD | Déplacement |
| L3 | Shift | Sprint |
| Cross (X) | Espace | Saut |
| Circle (O) | C | S'accroupir |
| L1 | Q | Action rapide |
| L2 (trigger) | X | Action alternative |
| PS Button | Échap | Pause / Menu |
| D-Pad Haut | 3 | Slot 3 |
| D-Pad Bas | 4 | Slot 4 |
| D-Pad Gauche | 1 | Slot 1 |
| D-Pad Droite | F | Interaction |

## Mise à jour

Pour mettre à jour vers une nouvelle version :

1. Télécharger le nouveau pack depuis GitHub
2. **Préserver votre configuration** : copier `config.json` de l'ancien `02-USAGE/` vers le nouveau
3. Remplacer le contenu de `02-USAGE/` par le nouveau
4. Remplacer `README.md` et `MANUEL.txt`
5. Relancer `01-INSTALLATION/INSTALL.bat` si la version ScpToolkit a changé

## Prérequis

- Windows 10/11 (64-bit)
- Python 3.12+ (https://www.python.org/downloads/)
- Navigation Controller Sony (PS Move)

## ⚠️ Jeux Steam — Masquer le contrôleur avec HidHide

Steam Input intercepte automatiquement les contrôleurs XInput (le contrôleur Xbox 360 virtuel créé par ScpVBus). Cela crée un conflit avec les touches clavier envoyées par `nav2keys.py`.

**Solution recommandée : HidHide** (pare-feu de périphériques par Nefarius)

HidHide masque le contrôleur virtuel de Steam tout en permettant à `nav2keys.py` d'y accéder.

Depuis v3.6.0, la configuration est **automatique** :
- `INSTALL.bat` (étape 5) détecte/installe/configure HidHide
- `launch_nav2keys.bat` configure HidHide à chaque lancement

Voir `MANUEL.txt` section "SOLUTION RECOMMANDEE : HidHide" pour le guide complet.

**Alternative** : Désactiver Steam Input par jeu (Propriétés → Contrôleur → Disable Steam Input)

## Auteurs

Développé en collaboration entre ienien et OpenCode (IA).

## Licence

Usage personnel uniquement. Ne pas redistribuer commercialement.
