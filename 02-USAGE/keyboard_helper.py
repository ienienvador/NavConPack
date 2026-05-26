import sys, json, pydirectinput

pydirectinput.FAILSAFE = False

KEYS = ["space","tab","esc","enter","shift","ctrl","alt","backspace","delete","insert","home","end",
        "left","right","up","down","pageup","pagedown","printscreen","capslock","numlock","scrolllock",
        "pause","multiply","add","subtract","decimal","divide",
        "a","b","c","d","e","f","g","h","i","j","k","l","m",
        "n","o","p","q","r","s","t","u","v","w","x","y","z",
        "0","1","2","3","4","5","6","7","8","9",
        "f1","f2","f3","f4","f5","f6","f7","f8","f9","f10","f11","f12"]

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    try:
        cmd = json.loads(line)
        action = cmd.get("action")
        key = cmd.get("key")
        if action == "keyDown":
            pydirectinput.keyDown(key)
        elif action == "keyUp":
            pydirectinput.keyUp(key)
        elif action == "press":
            pydirectinput.press(key)
        elif action == "releaseAll":
            for k in KEYS:
                try: pydirectinput.keyUp(k)
                except: pass
        elif action == "exit":
            break
    except Exception:
        pass
