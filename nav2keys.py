import ctypes, time, sys
from ctypes import wintypes
import pydirectinput

pydirectinput.FAILSAFE = False

# ── XInput API ─────────────────────────────────────────────────────
class XINPUT_GAMEPAD(ctypes.Structure):
    _fields_ = [
        ('wButtons', wintypes.WORD),
        ('bLeftTrigger', wintypes.BYTE),
        ('bRightTrigger', wintypes.BYTE),
        ('sThumbLX', wintypes.SHORT),
        ('sThumbLY', wintypes.SHORT),
        ('sThumbRX', wintypes.SHORT),
        ('sThumbRY', wintypes.SHORT),
    ]

class XINPUT_STATE(ctypes.Structure):
    _fields_ = [('dwPacketNumber', wintypes.DWORD), ('Gamepad', XINPUT_GAMEPAD)]

xinput = ctypes.windll.xinput1_4
if not xinput:
    xinput = ctypes.windll.xinput1_3
if not xinput:
    xinput = ctypes.windll.xinput9_1_0

# ── Mapping (button_mask -> key_name for pydirectinput) ────────────
MAP = {
    0x1000: 'space',
    0x2000: 'c',
    0x4000: 'r',
    0x8000: '2',
    0x0100: 'q',
    0x0200: 'g',
    0x0020: 'tab',
    0x0010: 'esc',
    0x0040: 'shift',
    0x0080: 'v',
    0x0001: '3',
    0x0002: '4',
    0x0004: '1',
    0x0008: 'f',
}

BTN_NAMES = {
    0x1000: 'A', 0x2000: 'B', 0x4000: 'X', 0x8000: 'Y',
    0x0100: 'LB', 0x0200: 'RB', 0x0020: 'Back', 0x0010: 'Start',
    0x0040: 'L3', 0x0080: 'R3',
    0x0001: 'D-U', 0x0002: 'D-D', 0x0004: 'D-L', 0x0008: 'D-R',
}

# ── State ──────────────────────────────────────────────────────────
pressed = set()
DZ = 7849
TRIGGER_THRESHOLD = 80
lt_pressed = False
rt_pressed = False
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
    keys = ['w', 'a', 's', 'd']
    for i in range(4):
        if cur[i] and not last_wasd[i]: pydirectinput.keyDown(keys[i])
        elif last_wasd[i] and not cur[i]: pydirectinput.keyUp(keys[i])
    last_wasd = cur

def do_triggers(lt, rt):
    global lt_pressed, rt_pressed
    lt_down = lt > TRIGGER_THRESHOLD
    rt_down = rt > TRIGGER_THRESHOLD
    
    if lt_down and not lt_pressed:
        lt_pressed = True; pydirectinput.keyDown('x')
    elif not lt_down and lt_pressed:
        lt_pressed = False; pydirectinput.keyUp('x')
    
    if rt_down and not rt_pressed:
        rt_pressed = True; pydirectinput.keyDown('e')
    elif not rt_down and rt_pressed:
        rt_pressed = False; pydirectinput.keyUp('e')

def release_all():
    global lt_pressed, rt_pressed
    for m in list(pressed): btn_change(m, False)
    do_wasd(0, 0)
    if lt_pressed: lt_pressed = False; pydirectinput.keyUp('x')
    if rt_pressed: rt_pressed = False; pydirectinput.keyUp('e')

def get_connected_slot():
    state = XINPUT_STATE()
    for slot in range(4):
        r = xinput.XInputGetState(slot, ctypes.byref(state))
        if r == 0:
            return slot
    return -1

def print_status(g):
    active = []
    for mask, name in BTN_NAMES.items():
        if g.wButtons & mask:
            key = MAP.get(mask)
            if key: active.append(f'{name}->{key}')
    
    lt = g.bLeftTrigger
    rt = g.bRightTrigger
    if lt > TRIGGER_THRESHOLD: active.append(f'L2->x({lt})')
    if rt > TRIGGER_THRESHOLD: active.append(f'R2->e({rt})')
    
    lx, ly = g.sThumbLX, g.sThumbLY
    lx_norm = lx if abs(lx) > DZ else 0
    ly_norm = ly if abs(ly) > DZ else 0
    wasd_active = []
    if ly_norm < -DZ: wasd_active.append('W')
    if lx_norm < -DZ: wasd_active.append('A')
    if ly_norm > DZ: wasd_active.append('S')
    if lx_norm > DZ: wasd_active.append('D')
    if wasd_active: active.append(f'Stick={"".join(wasd_active)}')
    
    status = ', '.join(active) if active else 'idle'
    sys.stdout.write(f'\r  [{status}]' + ' ' * 60)
    sys.stdout.flush()

# ── Main ───────────────────────────────────────────────────────────
def main():
    print("NavCon -> Keyboard Mapper v3.0.1", flush=True)
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
    
    global last_wasd, pressed, lt_pressed, rt_pressed
    last_btn = 0
    lt_pressed = False
    rt_pressed = False
    reconnect_count = 0
    
    try:
        while True:
            s = XINPUT_STATE()
            r = xinput.XInputGetState(slot, ctypes.byref(s))
            
            if r != 0:
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
            g = s.Gamepad
            
            ch = g.wButtons ^ last_btn
            if ch:
                for bit in range(16):
                    m = 1 << bit
                    if ch & m: btn_change(m, bool(g.wButtons & m))
                last_btn = g.wButtons
            
            do_wasd(g.sThumbLX, g.sThumbLY)
            do_triggers(g.bLeftTrigger, g.bRightTrigger)
            
            print_status(g)
            time.sleep(0.004)
    except KeyboardInterrupt:
        pass
    finally:
        release_all()
        print("\nTouches relachees. Exiting.", flush=True)

if __name__ == '__main__':
    main()
