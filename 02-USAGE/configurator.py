import tkinter as tk
from tkinter import ttk, messagebox
import json, os, ctypes, time, threading

CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.json')
PRESETS_DIR = os.path.join(os.path.dirname(__file__), 'presets')

DEFAULT_CONFIG = {
    "mapping": {
        "0x1000": "space", "0x2000": "c",
        "0x0100": "q", "0x0040": "shift", "0x0010": "esc",
        "0x0001": "3", "0x0002": "4", "0x0004": "1", "0x0008": "f",
    },
    "triggers": {"threshold": 80, "L2": "x"},
    "stick": {"deadzone": 7849, "up": "w", "down": "s", "left": "a", "right": "d"}
}

BTN_GROUPS = {
    "left": {
        "label": "Cote Gauche (Navigation Controller)",
        "buttons": {
            "0x0001": "D-Pad Haut",
            "0x0002": "D-Pad Bas",
            "0x0004": "D-Pad Gauche",
            "0x0008": "D-Pad Droite",
            "0x1000": "Cross (X)",
            "0x2000": "Circle (O)",
            "0x0100": "L1",
            "0x0040": "L3 (clic stick)",
            "0x0010": "PS Button (Start)",
        }
    }
}

BTN_LABELS_FLAT = {k: v for group in BTN_GROUPS.values() for k, v in group["buttons"].items()}

KEY_OPTIONS = [
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
    "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
    "space", "tab", "esc", "enter", "shift", "ctrl", "alt",
    "backspace", "delete", "insert", "home", "end",
    "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12",
    "left", "right", "up", "down",
    "pageup", "pagedown", "printscreen", "capslock", "numlock", "scrolllock",
    "pause", "multiply", "add", "subtract", "decimal", "divide",
]

class XINPUT_GAMEPAD(ctypes.Structure):
    _fields_ = [
        ('wButtons', ctypes.c_ushort),
        ('bLeftTrigger', ctypes.c_ubyte),
        ('bRightTrigger', ctypes.c_ubyte),
        ('sThumbLX', ctypes.c_short),
        ('sThumbLY', ctypes.c_short),
        ('sThumbRX', ctypes.c_short),
        ('sThumbRY', ctypes.c_short),
    ]

class XINPUT_STATE(ctypes.Structure):
    _fields_ = [('dwPacketNumber', ctypes.c_ulong), ('Gamepad', XINPUT_GAMEPAD)]

class NavConConfigurator:
    def __init__(self, root):
        self.root = root
        self.root.title("NavCon Configurator v3.3.0 - By ienien")
        self.root.geometry("850x700")
        self.root.resizable(False, False)
        
        self.config = self.load_config()
        self.test_running = False
        self.test_thread = None
        self.stick_vars = {}
        
        self.xinput = ctypes.windll.xinput1_4
        if not self.xinput:
            self.xinput = ctypes.windll.xinput1_3
        if not self.xinput:
            self.xinput = ctypes.windll.xinput9_1_0
        
        self.build_ui()
        self.load_values()
    
    def load_config(self):
        if os.path.exists(CONFIG_PATH):
            try:
                with open(CONFIG_PATH) as f:
                    cfg = json.load(f)
                for section in DEFAULT_CONFIG:
                    if section not in cfg:
                        cfg[section] = DEFAULT_CONFIG[section]
                return cfg
            except Exception:
                pass
        return json.loads(json.dumps(DEFAULT_CONFIG))
    
    def save_config(self):
        with open(CONFIG_PATH, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def build_ui(self):
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title = ttk.Label(main_frame, text="NavCon Configurator v3.3.0 - By ienien",
                         font=('Segoe UI', 16, 'bold'))
        title.pack(pady=(0, 10))
        
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        self.build_buttons_tab(notebook)
        self.build_triggers_tab(notebook)
        self.build_stick_tab(notebook)
        self.build_presets_tab(notebook)
        self.build_test_tab(notebook)
        
        self.build_action_bar(main_frame)
    
    def build_buttons_tab(self, notebook):
        frame = ttk.Frame(notebook, padding=10)
        notebook.add(frame, text="Boutons")
        
        info_label = ttk.Label(frame, text="Spécialisé Navigation Controller — boutons côté droit non disponibles",
                              foreground='darkred', font=('Segoe UI', 10, 'bold'))
        info_label.pack(pady=(0, 10))
        
        canvas = tk.Canvas(frame, width=780, height=400)
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
        scroll_frame = ttk.Frame(canvas)
        
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor=tk.NW)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        for group_key, group_data in BTN_GROUPS.items():
            group_frame = ttk.LabelFrame(scroll_frame, text=group_data["label"], padding=10)
            group_frame.pack(fill=tk.X, pady=10, padx=5)
            
            btn_keys = list(group_data["buttons"].keys())
            for i in range(0, len(btn_keys), 2):
                row_frame = ttk.Frame(group_frame)
                row_frame.pack(fill=tk.X, pady=2)
                
                self._make_btn_row(row_frame, btn_keys[i], 0)
                if i + 1 < len(btn_keys):
                    self._make_btn_row(row_frame, btn_keys[i+1], 1)
    
    def _make_btn_row(self, parent, key, col):
        row = ttk.Frame(parent)
        row.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        ttk.Label(row, text=BTN_LABELS_FLAT.get(key, key), width=20, anchor=tk.W).pack(side=tk.LEFT)
        
        var = tk.StringVar(value=self.config["mapping"].get(key, ""))
        combo = ttk.Combobox(row, textvariable=var, values=KEY_OPTIONS, width=12, state="readonly")
        combo.pack(side=tk.LEFT, padx=5)
        
        def on_change(v=var, k=key):
            self.config["mapping"][k] = v.get()
        var.trace_add("write", lambda *args: on_change())
        
        self.config["_combos"] = self.config.get("_combos", {})
        self.config["_combos"][key] = var
    
    def build_triggers_tab(self, notebook):
        frame = ttk.Frame(notebook, padding=10)
        notebook.add(frame, text="Trigger L2")
        
        ttk.Label(frame, text="Seuil de declenchement du trigger analogique L2",
                 font=('Segoe UI', 11, 'bold')).pack(anchor=tk.W, pady=(0, 10))
        
        thresh_frame = ttk.Frame(frame)
        thresh_frame.pack(fill=tk.X, pady=5)
        ttk.Label(thresh_frame, text="Seuil (0-255) :").pack(side=tk.LEFT)
        
        self.thresh_var = tk.IntVar(value=self.config["triggers"]["threshold"])
        thresh_scale = ttk.Scale(thresh_frame, from_=0, to=255, variable=self.thresh_var,
                                 orient=tk.HORIZONTAL, length=300)
        thresh_scale.pack(side=tk.LEFT, padx=10)
        
        self.thresh_label = ttk.Label(thresh_frame, text=str(self.thresh_var.get()), width=4)
        self.thresh_label.pack(side=tk.LEFT)
        self.thresh_var.trace_add("write", lambda *args: self.thresh_label.config(text=str(self.thresh_var.get())))
        
        ttk.Separator(frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=15)
        
        ttk.Label(frame, text="Touche assignee au trigger L2",
                 font=('Segoe UI', 11, 'bold')).pack(anchor=tk.W, pady=(0, 10))
        
        row = ttk.Frame(frame)
        row.pack(fill=tk.X, pady=5)
        ttk.Label(row, text="L2 (Trigger gauche)", width=22, anchor=tk.W).pack(side=tk.LEFT)
        
        self.l2_var = tk.StringVar(value=self.config["triggers"].get("L2", ""))
        combo = ttk.Combobox(row, textvariable=self.l2_var, values=KEY_OPTIONS, width=12, state="readonly")
        combo.pack(side=tk.LEFT, padx=5)
        
        def on_change(*args):
            self.config["triggers"]["L2"] = self.l2_var.get()
        self.l2_var.trace_add("write", on_change)

    def build_stick_tab(self, notebook):
        frame = ttk.Frame(notebook, padding=10)
        notebook.add(frame, text="Stick Analogique")
        
        ttk.Label(frame, text="Deadzone du stick (mouvements ignores en dessous)",
                 font=('Segoe UI', 11, 'bold')).pack(anchor=tk.W, pady=(0, 10))
        
        dz_frame = ttk.Frame(frame)
        dz_frame.pack(fill=tk.X, pady=5)
        ttk.Label(dz_frame, text="Deadzone (0-32767) :").pack(side=tk.LEFT)
        
        self.dz_var = tk.IntVar(value=self.config["stick"]["deadzone"])
        dz_scale = ttk.Scale(dz_frame, from_=0, to=32767, variable=self.dz_var,
                             orient=tk.HORIZONTAL, length=300)
        dz_scale.pack(side=tk.LEFT, padx=10)
        
        self.dz_label = ttk.Label(dz_frame, text=str(self.dz_var.get()), width=6)
        self.dz_label.pack(side=tk.LEFT)
        self.dz_var.trace_add("write", lambda *args: self.dz_label.config(text=str(self.dz_var.get())))
        
        ttk.Separator(frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=15)
        
        ttk.Label(frame, text="Touches du stick (WASD par defaut)",
                 font=('Segoe UI', 11, 'bold')).pack(anchor=tk.W, pady=(0, 10))
        
        directions = [("up", "Haut (W)"), ("down", "Bas (S)"), ("left", "Gauche (A)"), ("right", "Droite (D)")]
        for dir_key, label in directions:
            row = ttk.Frame(frame)
            row.pack(fill=tk.X, pady=5)
            ttk.Label(row, text=label, width=18, anchor=tk.W).pack(side=tk.LEFT)
            
            var = tk.StringVar(value=self.config["stick"].get(dir_key, ""))
            self.stick_vars[dir_key] = var
            combo = ttk.Combobox(row, textvariable=var, values=KEY_OPTIONS, width=12, state="readonly")
            combo.pack(side=tk.LEFT, padx=5)
            
            def on_change(v=var, k=dir_key):
                self.config["stick"][k] = v.get()
            var.trace_add("write", lambda *args: on_change())
    
    def build_presets_tab(self, notebook):
        frame = ttk.Frame(notebook, padding=10)
        notebook.add(frame, text="Presets")
        
        ttk.Label(frame, text="Charger un profil preconfigure",
                 font=('Segoe UI', 11, 'bold')).pack(anchor=tk.W, pady=(0, 10))
        
        preset_frame = ttk.Frame(frame)
        preset_frame.pack(fill=tk.X, pady=10)
        
        self.preset_var = tk.StringVar()
        presets = self._get_presets()
        preset_combo = ttk.Combobox(preset_frame, textvariable=self.preset_var,
                                    values=presets, width=30, state="readonly")
        preset_combo.pack(side=tk.LEFT, padx=5)
        if presets:
            preset_combo.current(0)
        
        ttk.Button(preset_frame, text="Charger", command=self.load_preset).pack(side=tk.LEFT, padx=5)
        
        info_frame = ttk.LabelFrame(frame, text="Presets disponibles", padding=10)
        info_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        for preset_file in presets:
            try:
                with open(os.path.join(PRESETS_DIR, preset_file)) as f:
                    p = json.load(f)
                desc = p.get("description", "")
            except Exception:
                desc = ""
            ttk.Label(info_frame, text=f"  {preset_file.replace('.json','')} : {desc}").pack(anchor=tk.W, pady=2)
    
    def _get_presets(self):
        if not os.path.exists(PRESETS_DIR):
            return []
        return sorted([f for f in os.listdir(PRESETS_DIR) if f.endswith('.json')])
    
    def load_preset(self):
        preset_name = self.preset_var.get()
        if not preset_name:
            return
        preset_path = os.path.join(PRESETS_DIR, preset_name)
        if not os.path.exists(preset_path):
            messagebox.showerror("Erreur", f"Preset introuvable : {preset_name}")
            return
        try:
            with open(preset_path) as f:
                preset = json.load(f)
            self.config["mapping"] = preset.get("mapping", self.config["mapping"])
            self.config["triggers"] = preset.get("triggers", self.config["triggers"])
            self.config["stick"] = preset.get("stick", self.config["stick"])
            self.load_values()
            messagebox.showinfo("Succes", f"Preset '{preset_name}' charge avec succes !")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger le preset : {e}")
    
    def build_test_tab(self, notebook):
        frame = ttk.Frame(notebook, padding=10)
        notebook.add(frame, text="Test en direct")
        
        ttk.Label(frame, text="Appuyez sur les boutons du controller pour voir les touches envoyees",
                 font=('Segoe UI', 11, 'bold')).pack(anchor=tk.W, pady=(0, 10))
        
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=10)
        
        self.test_btn = ttk.Button(btn_frame, text="Demarrer le test", command=self.toggle_test)
        self.test_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(frame, text="Touches envoyees :", font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W, pady=(10, 5))
        
        self.test_output = tk.Text(frame, height=15, width=80, font=('Consolas', 10))
        self.test_output.pack(fill=tk.BOTH, expand=True)
        
        self.test_status = ttk.Label(frame, text="En attente...", foreground='gray')
        self.test_status.pack(pady=5)
    
    def toggle_test(self):
        if self.test_running:
            self.test_running = False
            self.test_btn.config(text="Demarrer le test")
            self.test_status.config(text="Test arrete", foreground='gray')
        else:
            self.test_running = True
            self.test_btn.config(text="Arreter le test")
            self.test_status.config(text="Test en cours - appuyez sur les boutons...", foreground='green')
            self.test_output.delete(1.0, tk.END)
            self.test_thread = threading.Thread(target=self._test_loop, daemon=True)
            self.test_thread.start()
    
    def _test_loop(self):
        import pydirectinput
        last_buttons = 0
        last_lt = -1
        threshold = self.config["triggers"]["threshold"]
        l2_key = self.config["triggers"]["L2"]
        lt_active = False
        
        while self.test_running:
            state = XINPUT_STATE()
            r = self.xinput.XInputGetState(0, ctypes.byref(state))
            if r == 0:
                g = state.Gamepad
                changed = g.wButtons ^ last_buttons
                if changed:
                    for bit in range(16):
                        m = 1 << bit
                        if changed & m:
                            hex_key = hex(m)
                            key = self.config["mapping"].get(hex_key, "?")
                            label = BTN_LABELS_FLAT.get(hex_key, hex_key)
                            state_str = "PRESSE" if (g.wButtons & m) else "RELACHE"
                            action = "keyDown" if state_str == "PRESSE" else "keyUp"
                            line = f"  {label} -> {action}('{key}')\n"
                            self.root.after(0, lambda l=line: self.test_output.insert(tk.END, l))
                            self.root.after(0, lambda: self.test_output.see(tk.END))
                            if state_str == "PRESSE":
                                try: pydirectinput.keyDown(key)
                                except: pass
                            else:
                                try: pydirectinput.keyUp(key)
                                except: pass
                    last_buttons = g.wButtons
                
                if g.bLeftTrigger != last_lt:
                    lt_down = g.bLeftTrigger > threshold
                    if lt_down and not lt_active:
                        lt_active = True
                        line = f"  L2 (trigger={g.bLeftTrigger}) -> keyDown('{l2_key}')\n"
                        self.root.after(0, lambda l=line: self.test_output.insert(tk.END, l))
                        try: pydirectinput.keyDown(l2_key)
                        except: pass
                    elif not lt_down and lt_active:
                        lt_active = False
                        line = f"  L2 relache -> keyUp('{l2_key}')\n"
                        self.root.after(0, lambda l=line: self.test_output.insert(tk.END, l))
                        try: pydirectinput.keyUp(l2_key)
                        except: pass
                    last_lt = g.bLeftTrigger
            time.sleep(0.01)
    
    def load_values(self):
        if "_combos" in self.config:
            for key, var in self.config["_combos"].items():
                val = self.config["mapping"].get(key, "")
                var.set(val)
        self.thresh_var.set(self.config["triggers"]["threshold"])
        self.dz_var.set(self.config["stick"]["deadzone"])
        self.l2_var.set(self.config["triggers"]["L2"])
        for dir_key, var in self.stick_vars.items():
            var.set(self.config["stick"][dir_key])
    
    def build_action_bar(self, parent):
        bar = ttk.Frame(parent)
        bar.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(bar, text="Sauvegarder", command=self.save_and_notify).pack(side=tk.LEFT, padx=5)
        ttk.Button(bar, text="Reinitialiser", command=self.reset_config).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(bar, text="Config sauvegardee dans config.json", foreground='gray').pack(side=tk.RIGHT, padx=5)
    
    def save_and_notify(self):
        self.config["triggers"]["threshold"] = self.thresh_var.get()
        self.config["stick"]["deadzone"] = self.dz_var.get()
        self.config.pop("_combos", None)
        self.save_config()
        messagebox.showinfo("Succes", "Configuration sauvegardee dans config.json !\n\nRelancez nav2keys.py pour appliquer les changements.")
    
    def reset_config(self):
        if messagebox.askyesno("Confirmation", "Reinitialiser tous les parametres aux valeurs par defaut ?"):
            self.config = json.loads(json.dumps(DEFAULT_CONFIG))
            self.thresh_var.set(DEFAULT_CONFIG["triggers"]["threshold"])
            self.dz_var.set(DEFAULT_CONFIG["stick"]["deadzone"])
            self.load_values()
            self.save_config()
            messagebox.showinfo("Succes", "Configuration reinitialisee !")

if __name__ == '__main__':
    root = tk.Tk()
    app = NavConConfigurator(root)
    root.mainloop()
