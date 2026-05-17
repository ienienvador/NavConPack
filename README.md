# NavCon Pack v3.0.1

## Navigation Controller → Clavier pour PC

Solution complète pour utiliser un **Sony Navigation Controller** (PS Move) sur PC Windows comme clavier. Compatible avec tous les jeux — aucune détection de manette parasite.

## Fonctionnement

```
Navigation Controller → ScpService → ScpVBus (Xbox 360 virtuel) → nav2keys.py (XInput) → Touches clavier (pydirectinput) → Jeu
```

Le jeu ne voit **que le clavier**, jamais la manette.

## Installation

1. Installer Python 3.12+ depuis [python.org](https://www.python.org/downloads/) (cocher "Add Python to PATH")
2. Exécuter `INSTALL.bat` en tant qu'administrateur (ScpToolkit sera téléchargé automatiquement depuis [github.com/nefarius/ScpToolkit](https://github.com/nefarius/ScpToolkit/releases))
3. Redémarrer le PC
4. Allumer le Navigation Controller
5. Double-cliquer sur `launch_nav2keys.bat`
6. Lancer le jeu

## Mapping par défaut

| Bouton Nav | Touche | Action (exemple) |
|-----------|--------|------------------|
| Stick Gauche | WASD | Déplacement |
| L3 | Shift | Sprint |
| Cross (X) | Espace | Saut |
| Circle (O) | C | S'accroupir |
| Square ([]) | R | Recharger |
| Triangle (A) | 2 | Arme secondaire |
| L1 | Q | Action rapide |
| R1 | G | Grenade / Objet |
| L2 (trigger) | X | Action alternative |
| R2 (trigger) | E | Interagir |
| Select | Tab | Scoreboard / Menu |
| Start | Échap | Pause |
| D-Pad Haut | 3 | Slot 3 |
| D-Pad Bas | 4 | Slot 4 |
| D-Pad Gauche | 1 | Slot 1 |
| D-Pad Droite | F | Interaction |
| R3 | V | Mêlée / Action |

## Contenu

| Fichier | Rôle |
|---------|------|
| `INSTALL.bat` | Installation complète (admin) |
| `launch_nav2keys.bat` | Lancement quotidien |
| `nav2keys.py` | Script de mapping v3.0.1 |
| `README.txt` | Documentation complète |

## Prérequis

- Windows 10/11 (64-bit)
- Python 3.12+
- Navigation Controller Sony (PS Move)

## Auteurs

Développé en collaboration entre ienien et OpenCode (IA).

## Licence

Usage personnel uniquement. Ne pas redistribuer commercialement.
