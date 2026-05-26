import time, sys, json, os, subprocess
import pydirectinput

pydirectinput.FAILSAFE = False

# ── Configuration ──────────────────────────────────────────────────
CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.json')

DEFAULT_CONFIG = {
    "mapping": {
        "0x1000": "space", "0x2000": "c",
        "0x0100": "q", "0x0040": "shift", "0x0010": "esc",
        "0x0001": "3", "0x0002": "4", "0x0004": "1", "0x0008": "f",
    },
    "triggers": {"threshold": 80, "L2": "x"},
    "stick": {"deadzone": 7849, "up": "w", "down": "s", "left": "a", "right": "d"}
}

def load_config():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH) as f:
                cfg = json.load(f)
            # Migration : supprimer les entrées obsolètes
            obsolete_keys = {"0x4000", "0x8000", "0x0200", "0x0080", "0x0020"}
            for key in obsolete_keys:
                cfg.get("mapping", {}).pop(key, None)
            cfg.get("triggers", {}).pop("R2", None)
            # Compléter avec les défauts manquants
            for section in DEFAULT_CONFIG:
                if section not in cfg:
                    cfg[section] = DEFAULT_CONFIG[section]
            return cfg
        except Exception:
            pass
    return DEFAULT_CONFIG

config = load_config()
MAP = { int(k, 16): v for k, v in config["mapping"].items() }
DZ = config["stick"]["deadzone"]
TRIGGER_THRESHOLD = config["triggers"]["threshold"]
L2_KEY = config["triggers"]["L2"]
WASD_KEYS = [config["stick"]["up"], config["stick"]["left"],
             config["stick"]["down"], config["stick"]["right"]]

def _find_helper():
    h = os.path.join(os.path.dirname(__file__), 'xinput_helper.exe')
    if os.path.exists(h): return h
    s = os.path.join(os.path.dirname(__file__), 'xinput_helper.cs')
    if not os.path.exists(s): return None
    r = subprocess.run(['powershell', '-NoProfile', '-Command',
        'try { Add-Type -OutputAssembly "' + h + '" -TypeDefinition (Get-Content "' + s + '" -Raw) -Language CSharp -WarningAction SilentlyContinue; exit 0 } catch { exit 1 }'],
        capture_output=True, text=True, timeout=30)
    return h if r.returncode == 0 and os.path.exists(h) else None

_XH_PATH = _find_helper()

def _xh_run(*args):
    if not _XH_PATH: return None
    try:
        r = subprocess.run([_XH_PATH] + list(args), capture_output=True, text=True, timeout=5)
        return r.stdout.strip()
    except: return None

def get_connected_slot():
    out = _xh_run()
    if out: return int(out.split()[0])
    return -1

def xinput_get_state(slot):
    out = _xh_run('POLL', str(slot))
    if out and out != 'DISCONNECTED':
        parts = out.split()
        if len(parts) >= 9:
            return {
                'dwPacketNumber': int(parts[1]),
                'wButtons': int(parts[2]),
                'bLeftTrigger': int(parts[3]),
                'bRightTrigger': int(parts[4]),
                'sThumbLX': int(parts[5]),
                'sThumbLY': int(parts[6]),
                'sThumbRX': int(parts[7]),
                'sThumbRY': int(parts[8]),
            }
    return None

BTN_NAMES = {
    0x1000: 'A', 0x2000: 'B', 0x0100: 'LB', 0x0010: 'Start',
    0x0040: 'L3', 0x0001: 'D-U', 0x0002: 'D-D', 0x0004: 'D-L', 0x0008: 'D-R',
}

# ── State ─────────────────────────────────────────────────────────
pressed = set()
lt_pressed = False
last_wasd = [False]*4

def btn_change(mask, down):
    key = MAP.get(mask)
    if not key: return
    if down and mask not in pressed:
        pressed.add(mask); pydirectinput.keyDown(key)
    elif not down and mask in pressed:
        pressed.discard(mask); pydirectinput.keyUp(key)

def do_wasd(lx, ly):
    global last_wasd
    lx = lx if abs(lx) > DZ else 0
    ly = ly if abs(ly) > DZ else 0
    cur = [ly < -DZ, lx < -DZ, ly > DZ, lx > DZ]
    for i in range(4):
        if cur[i] and not last_wasd[i]: pydirectinput.keyDown(WASD_KEYS[i])
        elif last_wasd[i] and not cur[i]: pydirectinput.keyUp(WASD_KEYS[i])
    last_wasd = cur

def do_triggers(lt, rt):
    global lt_pressed
    lt_down = lt > TRIGGER_THRESHOLD
    
    if lt_down and not lt_pressed:
        lt_pressed = True; pydirectinput.keyDown(L2_KEY)
    elif not lt_down and lt_pressed:
        lt_pressed = False; pydirectinput.keyUp(L2_KEY)

def release_all():
    global lt_pressed
    for m in list(pressed): btn_change(m, False)
    do_wasd(0, 0)
    if lt_pressed: lt_pressed = False; pydirectinput.keyUp(L2_KEY)



def print_status(s):
    active = []
    for mask, name in BTN_NAMES.items():
        if s['wButtons'] & mask:
            key = MAP.get(mask)
            if key: active.append(f'{name}->{key}')
    
    lt = s['bLeftTrigger']
    if lt > TRIGGER_THRESHOLD: active.append(f'L2->{L2_KEY}({lt})')
    
    lx, ly = s['sThumbLX'], s['sThumbLY']
    lx_norm = lx if abs(lx) > DZ else 0
    ly_norm = ly if abs(ly) > DZ else 0
    wasd_active = []
    if ly_norm < -DZ: wasd_active.append(WASD_KEYS[0].upper())
    if lx_norm < -DZ: wasd_active.append(WASD_KEYS[1].upper())
    if ly_norm > DZ: wasd_active.append(WASD_KEYS[2].upper())
    if lx_norm > DZ: wasd_active.append(WASD_KEYS[3].upper())
    if wasd_active: active.append(f'Stick={"".join(wasd_active)}')
    
    status = ', '.join(active) if active else 'idle'
    sys.stdout.write(f'\r  [{status}]' + ' ' * 60)
    sys.stdout.flush()

# ── Main ───────────────────────────────────────────────────────────
def main():
    print("NavCon -> Keyboard Mapper v3.5.0", flush=True)
    print("=" * 40, flush=True)
    
    slot = get_connected_slot()
    if slot < 0:
        print("Recherche du controller... (branchez ou appuyez sur un bouton)", flush=True)
        while True:
            slot = get_connected_slot()
            if slot >= 0:
                break
            time.sleep(0.5)
    
    print(f"Controller detecte sur slot {slot}", flush=True)
    print("Mapping actif - Ctrl+C pour arreter", flush=True)
    print("-" * 40, flush=True)
    
    global last_wasd, pressed, lt_pressed
    last_btn = 0
    lt_pressed = False
    reconnect_count = 0
    
    try:
        while True:
            s = xinput_get_state(slot)
            
            if not s:
                if reconnect_count == 0:
                    sys.stdout.write('\r  [DECONNECTE - reconnexion...]' + ' ' * 40)
                    sys.stdout.flush()
                reconnect_count += 1
                time.sleep(0.5)
                
                if reconnect_count > 20:
                    slot = get_connected_slot()
                    if slot >= 0:
                        reconnect_count = 0
                        sys.stdout.write('\r  [RECONNECTE sur slot ' + str(slot) + ']' + ' ' * 40)
                        sys.stdout.flush()
                continue
            
            reconnect_count = 0
            
            ch = s['wButtons'] ^ last_btn
            if ch:
                for bit in range(16):
                    m = 1 << bit
                    if ch & m: btn_change(m, bool(s['wButtons'] & m))
                last_btn = s['wButtons']
            
            do_wasd(s['sThumbLX'], s['sThumbLY'])
            do_triggers(s['bLeftTrigger'], s['bRightTrigger'])
            
            print_status(s)
            time.sleep(0.004)
    except KeyboardInterrupt:
        pass
    finally:
        release_all()
        print("\nTouches relachees. Exiting.", flush=True)

if __name__ == '__main__':
    main()
