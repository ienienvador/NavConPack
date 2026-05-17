# NavCon Pack v3.3.0

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

1. Ouvrir le dossier `01-INSTALLATION`
2. Clic droit sur `INSTALL.bat` → **Exécuter en tant qu'administrateur**
3. Suivre les étapes (Python → pydirectinput → ScpToolkit → Driver)
4. Redémarrer le PC

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

## ⚠️ Jeux Steam — Important

Steam Input intercepte automatiquement les contrôleurs XInput (le contrôleur Xbox 360 virtuel créé par ScpVBus). Cela crée un conflit avec les touches clavier envoyées par `nav2keys.py`.

**Solution rapide (par jeu) :**
1. Steam → Bibliothèque → Clic droit sur le jeu → **Propriétés**
2. Onglet **Contrôleur** → "Override for [jeu]" → **Disable Steam Input**

**Solution globale :**
Steam → Paramètres → Contrôleur → Désactiver "Activer Steam Input pour les manettes Xbox"

Voir `MANUEL.txt` section "JEUX STEAM" pour plus de détails.

## Auteurs

Développé en collaboration entre ienien et OpenCode (IA).

## Licence

Usage personnel uniquement. Ne pas redistribuer commercialement.
