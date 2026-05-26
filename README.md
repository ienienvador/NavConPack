# NavCon Pack v3.6.0

Navigation Controller (PS Move) -> Clavier pour PC

## Nouveau : Application WPF

NavCon.exe est une application Windows (C# WPF) qui integre :
- Selection des presets au lancement
- Configuration avec 5 onglets (Boutons, Trigger L2, Stick, Presets, Test)
- Mapping en temps reel (boutons -> touches clavier)
- Configuration automatique de HidHide (anti Steam Input)

## Utilisation rapide

1. Installer Python 3.12+, .NET 9.0 SDK, ScpToolkit, HidHide (optionnel)
2. Lancer `01-INSTALLATION\INSTALL.bat` (admin) pour installer pydirectinput
3. Compiler avec `02-USAGE\compile.bat`
4. Lancer `02-USAGE\bin\NavCon.exe`
5. Choisir un preset -> Demarrer -> Jouer

## Pre-requis

- Windows 10/11 64-bit
- Python 3.12+ (Add Python to PATH)
- .NET 9.0 SDK
- [ScpToolkit](https://github.com/nefarius/ScpToolkit/releases) (DS3 Controller + ScpVBus)
- [HidHide](https://github.com/nefarius/HidHide/releases) (optionnel, recommandé Steam)
- pydirectinput (installe par INSTALL.bat)

## Mapping par defaut

| Bouton Nav | Touche | Action     |
|------------|--------|------------|
| Stick      | WASD   | Deplacement |
| L3         | Shift  | Sprint     |
| Cross (X)  | Space  | Saut       |
| Circle (O) | C      | S'accroupir |
| L1         | Q      | Action rapide |
| L2         | X      | Action alternative |
| PS Button  | Escape | Pause/Menu |

## Credits

- ienien : conception, tests en jeu
- OpenCode (IA) : developpement
