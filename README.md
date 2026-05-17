# NavCon Pack v3.1.0

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

## Configuration GUI (nouveau en v3.1.0)

Lancer `configurator.bat` pour ouvrir l'interface de configuration graphique :

- **Boutons** : Cliquer sur chaque bouton pour choisir sa touche dans un menu déroulant
- **Triggers** : Ajuster le seuil de déclenchement (slider) et la touche associée
- **Stick** : Ajuster la deadzone et les touches WASD
- **Presets** : Charger un profil préconfiguré (BF6, COD, ARC, The Division)
- **Test** : Tester en temps réel avec le controller connecté (vraies touches envoyées)

La configuration est sauvegardée dans `config.json` et lue automatiquement par `nav2keys.py`.

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
| `configurator.bat` | Interface de configuration GUI |
| `nav2keys.py` | Script de mapping v3.1.0 |
| `configurator.py` | Interface GUI (Tkinter) |
| `config.json` | Configuration utilisateur |
| `presets/` | Profils préconfigurés (BF6, COD, ARC, Division) |
| `MANUEL.txt` | Documentation complète |

## Prérequis

- Windows 10/11 (64-bit)
- Python 3.12+
- Navigation Controller Sony (PS Move)

## Auteurs

Développé en collaboration entre ienien et OpenCode (IA).

## Licence

Usage personnel uniquement. Ne pas redistribuer commercialement.
