# NavCon Pack v3.0.0

## Navigation Controller → Clavier pour PC

Solution complète pour utiliser un **Sony Navigation Controller** (PS Move, VID 054C:PID 042F) sur PC Windows comme clavier, sans reWASD (banni par EAC).

## Fonctionnement

```
Navigation Controller → ScpService → ScpVBus (Xbox 360 virtuel) → nav2keys.py (XInput) → Touches clavier (pydirectinput) → BF6
```

BF6 ne voit **que le clavier**, jamais la manette.

## Installation

1. Installer Python 3.12+ depuis [python.org](https://www.python.org/downloads/) (cocher "Add Python to PATH")
2. Exécuter `INSTALL.bat` en tant qu'administrateur
3. Redémarrer le PC
4. Allumer le Navigation Controller
5. Double-cliquer sur `launch_nav2keys.bat`
6. Lancer le jeu

## Mapping par défaut

| Bouton Nav | Touche | Action |
|-----------|--------|--------|
| Stick Gauche | WASD | Déplacement |
| L3 | Shift | Sprint |
| Cross (X) | Espace | Saut |
| Circle (O) | C | S'accroupir |
| Square ([]) | R | Recharger |
| Triangle (A) | 2 | Arme secondaire |
| L1 | Q | Répéter/Commo |
| R1 | G | Grenade |
| L2 (trigger) | X | Plat ventre |
| R2 (trigger) | E | Interagir |
| Select | Tab | Scoreboard |
| Start | Échap | Menu |
| D-Pad Haut | 3 | Gadget |
| D-Pad Bas | 4 | Spécial |
| D-Pad Gauche | 1 | Arme principale |
| D-Pad Droite | F | Interagir |
| R3 | V | Mêlée |

## Contenu

| Fichier | Rôle |
|---------|------|
| `INSTALL.bat` | Installation complète (admin) |
| `launch_nav2keys.bat` | Lancement quotidien |
| `nav2keys.py` | Script de mapping v2.3 |
| `ScpToolkit_Setup.exe` | Installateur ScpToolkit |
| `README.txt` | Documentation complète |

## Prérequis

- Windows 10/11 (64-bit)
- Python 3.12+
- Navigation Controller Sony (VID 054C / PID 042F)

## Auteurs

Développé en collaboration entre [Votre Nom] et OpenCode (IA).

## Licence

Usage personnel uniquement. Ne pas redistribuer commercialement.
