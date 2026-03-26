import tkinter as tk
from tkinter import Label, Canvas, ttk, messagebox, Scale, Text, Scrollbar
from PIL import ImageTk, Image, ImageSequence, ImageOps, ImageEnhance
import pygame
import catyy
import threading
import requests
import webbrowser
import random
import io
import os
import json
import time
import sys

if sys.platform == "win32":
    import winreg

class ProjectHub:
    def __init__(self, root):
        self.root = root
        self.root.title("Paw Session 🐾")
        
        pygame.mixer.pre_init(44100, -16, 2, 4096)
        pygame.mixer.init()
        
        screen_h = self.root.winfo_screenheight()
        self.win_w = 600
        self.win_h = int(screen_h * 0.85)
        self.root.geometry(f"{self.win_w}x{self.win_h}")
        self.root.resizable(False, False)
        
        self.config_file = "settings.json"
        self.settings = self.load_settings()
        
        self.api_key = self.settings.get("api_key", "")
        self.dark_mode = self.settings.get("dark_mode", False)
        self.search_algo = self.settings.get("search_algo", "Popular")
        self.blacklist = self.settings.get("blacklist", [])
        self.lang = self.settings.get("lang", "EN")
        self.nyan_speed = self.settings.get("nyan_speed", 40)
        self.nyan_opacity = self.settings.get("nyan_opacity", 1.0)
        self.auto_start = self.settings.get("auto_start", False)
        self.search_term = self.settings.get("search_term", "")
        self.selected_ascii = self.settings.get("selected_ascii", "Classic")
        
        self.ascii_library = {
            "Classic": "         _._     _,-'\"\"`-._\n        (,-.`._,'(       |\\`-/|\n            `-.-' \\ )-`( , o o)\n                  `-    \\`_`\"'-",
            "Grumpy": "      |\\      _,,,---,,_\nZZZzz /,`.-'`'    -.  ;-;;,_\n     |,4-  ) )-,_. ,\\ (  `'-'\n    '---''(_/--'  `-'\\_)",
            "Minimal": "   |\\__/,|   (`\\\n |_ _  |.--.) )\n ( T   )     /\n(((^_(((/(((_/"
        }
        
        self.translations = {
            "EN": {
                "title": "Paw Session",
                "settings": "Settings",
                "dark": "Dark Mode",
                "lang": "Language:",
                "algo": "Search Algorithm:",
                "bl": "Blacklist (comma separated):",
                "save": "Save Settings",
                "help": "How to get Youtube API key",
                "summon": "Summon Video",
                "dose": "Daily Goofy Dose",
                "wait": "Waiting for units...",
                "catching": "Catching the cat...",
                "speed": "Nyan Speed",
                "opacity": "Nyan Opacity",
                "ascii": "ASCII Style:",
                "startup": "Run on Startup",
                "sterm": "Search Term (Mandatory #cat):",
                "logs": "System Logs:",
                "api_setup": "YouTube API Setup",
                "api_guide": "YouTube Data API v3 Setup Guide:\n\n1. Visit Google Cloud Console (console.cloud.google.com) and sign in.\n2. Create a new project named 'PawSession-App'.\n3. In Library, Enable 'YouTube Data API v3'.\n4. Go to Credentials -> Create Credentials -> API key.\n5. Copy the AIza... key and paste it below.\n\n*Security Tip: Restrict your key to YouTube Data API v3 only.",
                "api_label": "Enter your YouTube API Key:",
                "api_confirm": "Activate & Launch"
            },
            "TR": {
                "title": "Pati Oturumu",
                "settings": "Ayarlar",
                "dark": "Karanlık Mod",
                "lang": "Dil Seçimi:",
                "algo": "Arama Algoritması:",
                "bl": "Kara Liste (virgülle ayır):",
                "save": "Ayarları Kaydet",
                "help": "API Anahtarı nasıl alınır",
                "summon": "Video Getir",
                "dose": "Günlük Şapşallık Dozu",
                "wait": "Şapşallık bekleniyor...",
                "catching": "Şapşal kedi yakalanıyor...",
                "speed": "Nyan Hızı",
                "opacity": "Nyan Şeffaflığı",
                "ascii": "ASCII Tarzı:",
                "startup": "Başlangıçta Çalıştır",
                "sterm": "Arama Metni (Zorunlu #cat):",
                "logs": "Sistem Günlükleri:",
                "api_setup": "YouTube API Kurulumu",
                "api_guide": "YouTube Data API v3 Kurulum Rehberi:\n\n1. console.cloud.google.com adresine gidin ve giriş yapın.\n2. 'PawSession-App' adında yeni proje oluşturun.\n3. Kütüphaneden 'YouTube Data API v3'ü etkinleştirin.\n4. Kimlik Bilgileri -> API anahtarı oluştur'a tıklayın.\n5. AIza... kodunu kopyalayıp aşağıya yapıştırın.\n\n*İpucu: Güvenlik için anahtarınızı kısıtlamayı unutmayın.",
                "api_label": "YouTube API Anahtarınızı Girin:",
                "api_confirm": "Onayla ve Başlat"
            },
            "DE": {
                "title": "Pfoten Sitzung",
                "settings": "Einstellungen",
                "dark": "Dunkelmodus",
                "lang": "Sprache:",
                "algo": "Suchalgorithmus:",
                "bl": "Blacklist:",
                "save": "Speichern",
                "help": "API-Schlüssel Hilfe",
                "summon": "Video Aufrufen",
                "dose": "Tägliche Dosis",
                "wait": "Warten...",
                "speed": "Nyan Geschwindigkeit",
                "opacity": "Nyan Deckkraft",
                "ascii": "ASCII Stil:",
                "startup": "Autostart",
                "sterm": "Suchbegriff (#cat Pflicht):",
                "logs": "Systemprotokolle:",
                "api_setup": "YouTube API Einrichtung",
                "api_guide": "Anleitung für API-Schlüssel:\n\n1. Gehen Sie zu console.cloud.google.com.\n2. Projekt 'PawSession' erstellen.\n3. 'YouTube Data API v3' aktivieren.\n4. Anmeldedaten -> API-Schlüssel erstellen.\n5. Schlüssel hier einfügen.",
                "api_label": "API-Schlüssel:",
                "api_confirm": "Bestätigen"
            }
        }
        
        self.themes = {
            "light": {"bg": "#FFF5F7", "card": "#FFFFFF", "text": "#4A4A4A", "accent": "#FF85A2", "p_bg": "white", "log": "#FDF2F4"},
            "dark": {"bg": "#1A1A1B", "card": "#2D2D2E", "text": "#E4E6EB", "accent": "#FFACBF", "p_bg": "#2D2D2E", "log": "#252526"}
        }
        
        self.rgb_colors = ["#FF0000", "#FF4500", "#FFD700", "#00FF00", "#00FFFF", "#0000FF", "#8A2BE2", "#FF00FF"]
        self.rgb_index = 0
        
        if not self.api_key:
            self.show_api_wizard()
        else:
            self.start_main_app()

    def load_settings(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f:
                    return json.load(f)
            except: 
                pass
        return {
            "api_key": "",
            "dark_mode": False,
            "lang": "EN",
            "nyan_speed": 40,
            "nyan_opacity": 1.0,
            "auto_start": False,
            "search_algo": "Popular",
            "blacklist": [],
            "search_term": "",
            "selected_ascii": "Classic"
        }

    def save_settings(self):
        s = {
            "api_key": self.api_key,
            "dark_mode": self.dark_mode,
            "search_algo": self.search_algo,
            "blacklist": self.blacklist,
            "lang": self.lang,
            "nyan_speed": self.nyan_speed,
            "nyan_opacity": self.nyan_opacity,
            "auto_start": self.auto_start,
            "search_term": self.search_term,
            "selected_ascii": self.selected_ascii
        }
        with open(self.config_file, "w") as f:
            json.dump(s, f)
        self.toggle_startup_registry()

    def show_api_wizard(self):
        self.wizard_frame = tk.Frame(self.root, padx=30, pady=30, bg="#FFFFFF")
        self.wizard_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        tr = self.translations[self.lang]
        
        wizard_title = tk.Label(self.wizard_frame, text=tr["api_setup"], font=("Segoe UI", 18, "bold"), bg="#FFFFFF", fg="#FF85A2")
        wizard_title.pack(pady=10)
        
        guide_text = tk.Text(self.wizard_frame, height=10, width=50, font=("Segoe UI", 10), wrap="word", bd=0, bg="#FDF2F4")
        guide_text.insert("1.0", tr["api_guide"])
        guide_text.config(state="disabled")
        guide_text.pack(pady=10)
        
        api_label = tk.Label(self.wizard_frame, text=tr["api_label"], font=("Segoe UI", 10, "bold"), bg="#FFFFFF")
        api_label.pack(pady=(10, 0))
        
        self.api_entry = tk.Entry(self.wizard_frame, width=45, font=("Consolas", 11), bd=1, relief="solid")
        self.api_entry.pack(pady=10)
        
        def confirm():
            val = self.api_entry.get().strip()
            if val:
                self.api_key = val
                self.save_settings()
                self.wizard_frame.destroy()
                self.start_main_app()
            else:
                messagebox.showwarning("API Required", "Please provide your YouTube API key to continue.")
        
        confirm_btn = tk.Button(self.wizard_frame, text=tr["api_confirm"], command=confirm, bg="#FF85A2", fg="white", font=("Segoe UI", 11, "bold"), relief="flat", padx=20, pady=5)
        confirm_btn.pack(pady=15)

    def start_main_app(self):
        if os.path.exists("cat.ico"):
            self.root.iconbitmap("cat.ico")
            
        self.setup_ui()
        self.update_ui_language()
        self.set_theme()
        
        threading.Thread(target=self.animate_nyan_rotating, daemon=True).start()
        threading.Thread(target=self.animate_title_rgb, daemon=True).start()

    def toggle_startup_registry(self):
        if sys.platform != "win32": return
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        app_name = "PatiOturumu"
        app_path = os.path.realpath(sys.argv[0])
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
            if self.auto_start:
                winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, f'"{app_path}"')
            else:
                try: 
                    winreg.DeleteValue(key, app_name)
                except: 
                    pass
            winreg.CloseKey(key)
        except: 
            pass

    def log_event(self, msg):
        timestamp = time.strftime("[%H:%M:%S] ")
        if hasattr(self, 'log_text'):
            self.log_text.config(state="normal")
            self.log_text.insert("end", timestamp + msg + "\n")
            self.log_text.see("end")
            self.log_text.config(state="disabled")

    def set_theme(self):
        t = self.themes["dark"] if self.dark_mode else self.themes["light"]
        self.root.configure(bg=t["bg"])
        self.main_card.configure(bg=t["card"])
        self.title_label.configure(bg=t["card"])
        self.ascii_label.configure(bg=t["card"], fg=t["text"])
        self.img_label.configure(bg=t["card"], fg=t["text"])
        self.nyan_canvas.configure(bg=t["bg"], highlightbackground=t["bg"])
        self.settings_btn.configure(bg=t["accent"])
        self.log_frame.configure(bg=t["card"])
        self.log_text.configure(bg=t["log"], fg=t["text"])
        self.log_label.configure(bg=t["card"], fg=t["accent"])

    def update_ui_language(self):
        tr = self.translations[self.lang]
        self.title_label.config(text=tr["title"])
        self.settings_btn.config(text=f"⚙️ {tr['settings']}")
        self.summon_btn.config(text=tr["summon"])
        self.dose_btn.config(text=tr["dose"])
        self.log_label.config(text=tr["logs"])
        self.ascii_label.config(text=self.ascii_library[self.selected_ascii])
        if not hasattr(self.img_label, 'image'):
            self.img_label.config(text=tr["wait"])

    def show_api_help(self):
        tr = self.translations[self.lang]
        h_win = tk.Toplevel(self.root)
        h_win.title(tr["help"])
        h_win.geometry("480x450")
        t = self.themes["dark"] if self.dark_mode else self.themes["light"]
        h_win.configure(bg=t["bg"])
        
        help_title = tk.Label(h_win, text=tr["help"], font=("Segoe UI", 16, "bold"), bg=t["bg"], fg=t["accent"])
        help_title.pack(pady=15)
        
        txt = tk.Text(h_win, height=12, width=50, font=("Segoe UI", 10), wrap="word", bg=t["log"], fg=t["text"], bd=0, padx=10, pady=10)
        txt.insert("1.0", tr["api_guide"])
        txt.config(state="disabled")
        txt.pack(pady=10)
        
        ok_btn = tk.Button(h_win, text="OK", command=h_win.destroy, bg=t["accent"], fg="white", font=("Segoe UI", 10, "bold"), relief="flat", width=15)
        ok_btn.pack(pady=10)

    def open_settings(self):
        tr = self.translations[self.lang]
        s_win = tk.Toplevel(self.root)
        s_win.title(tr["settings"])
        s_win.geometry("540x980")
        t = self.themes["dark"] if self.dark_mode else self.themes["light"]
        s_win.configure(bg=t["bg"])

        settings_title = tk.Label(s_win, text=tr["settings"], font=("Segoe UI", 22, "bold"), bg=t["bg"], fg=t["accent"])
        settings_title.pack(pady=15)
        
        help_btn = tk.Button(s_win, text=f"❓ {tr['help']}", command=self.show_api_help, bg="#98D8D8", fg="white", font=("Segoe UI", 10, "bold"), relief="flat")
        help_btn.pack(pady=5)
        
        api_label = tk.Label(s_win, text="YouTube API Key:", bg=t["bg"], fg=t["text"], font=("Segoe UI", 10, "bold"))
        api_label.pack()
        
        api_e = tk.Entry(s_win, width=40, font=("Consolas", 10))
        api_e.insert(0, self.api_key)
        api_e.pack(pady=5)
        
        dark_v = tk.BooleanVar(value=self.dark_mode)
        tk.Checkbutton(s_win, text=tr["dark"], variable=dark_v, bg=t["bg"], fg=t["text"], selectcolor=t["p_bg"]).pack()
        
        start_v = tk.BooleanVar(value=self.auto_start)
        tk.Checkbutton(s_win, text=tr["startup"], variable=start_v, bg=t["bg"], fg=t["text"], selectcolor=t["p_bg"]).pack()
        
        ascii_l_node = tk.Label(s_win, text=tr["ascii"], bg=t["bg"], fg=t["text"], font=("Segoe UI", 10, "bold"))
        ascii_l_node.pack(pady=5)
        
        ascii_cb = ttk.Combobox(s_win, values=list(self.ascii_library.keys()), state="readonly")
        ascii_cb.set(self.selected_ascii)
        ascii_cb.pack()
        
        speed_slider = tk.Scale(s_win, from_=10, to=100, orient="horizontal", label=tr["speed"], bg=t["bg"], fg=t["text"], length=280)
        speed_slider.set(self.nyan_speed)
        speed_slider.pack()
        
        opacity_slider = tk.Scale(s_win, from_=10, to=100, orient="horizontal", label=tr["opacity"], bg=t["bg"], fg=t["text"], length=280)
        opacity_slider.set(int(self.nyan_opacity * 100))
        opacity_slider.pack()
        
        lang_cb = ttk.Combobox(s_win, values=["EN", "TR", "DE"], state="readonly")
        lang_cb.set(self.lang)
        lang_cb.pack(pady=15)
        
        algo_cb = ttk.Combobox(s_win, values=["Popular", "Recent", "Random"], state="readonly")
        algo_cb.set(self.search_algo)
        algo_cb.pack()
        
        term_label = tk.Label(s_win, text=tr["sterm"], bg=t["bg"], fg=t["text"])
        term_label.pack()
        
        term_entry = tk.Entry(s_win, width=40)
        term_entry.insert(0, self.search_term)
        term_entry.pack()
        
        bl_label = tk.Label(s_win, text=tr["bl"], bg=t["bg"], fg=t["text"])
        bl_label.pack()
        
        bl_entry = tk.Entry(s_win, width=40)
        bl_entry.insert(0, ", ".join(self.blacklist))
        bl_entry.pack()
        
        def save_and_close():
            self.api_key = api_e.get().strip()
            self.dark_mode = dark_v.get()
            self.auto_start = start_v.get()
            self.lang = lang_cb.get()
            self.search_algo = algo_cb.get()
            self.selected_ascii = ascii_cb.get()
            self.nyan_speed = speed_slider.get()
            self.nyan_opacity = opacity_slider.get() / 100.0
            self.search_term = term_entry.get()
            self.blacklist = [x.strip().lower() for x in bl_entry.get().split(",") if x.strip()]
            self.save_settings()
            self.update_ui_language()
            self.set_theme()
            s_win.destroy()
            
        save_btn = tk.Button(s_win, text=tr["save"], command=save_and_close, bg=t["accent"], fg="white", width=35, height=2, relief="flat", font=("Segoe UI", 11, "bold"))
        save_btn.pack(pady=25)

    def play_meow(self):
        def stream():
            try:
                r = requests.get("https://www.soundjay.com/nature/sounds/cat-meow-01.mp3", timeout=5)
                pygame.mixer.Sound(io.BytesIO(r.content)).play()
            except: 
                pass
        threading.Thread(target=stream).start()

    def fetch_filtered_video(self):
        full_query = f"#cat {self.search_term}".strip()
        self.log_event(f"Searching YouTube with API for: {full_query}")
        while True:
            video = catyy.fetch_popular_cat_video(api_key=self.api_key, query=full_query, algo=self.search_algo)
            title = video['title'].lower()
            if any(word in title for word in self.blacklist):
                self.log_event(f"Filtered (Blacklisted): {video['title']}")
                continue
            self.log_event(f"Summoned Success: {video['title']}")
            catyy.open_video_in_browser(video['id'])
            break

    def load_cat_image(self):
        img = catyy.fetch_cat_image()
        if img:
            fixed_img = ImageOps.fit(img, (400, 300), Image.Resampling.LANCZOS)
            tk_img = ImageTk.PhotoImage(fixed_img)
            self.img_label.config(image=tk_img, text="")
            self.img_label.image = tk_img
            self.log_event("New goofy dose delivered successfully.")

    def animate_nyan_rotating(self):
        gif_path = "nyan-cat.gif"
        if not os.path.exists(gif_path): return
        gif_data = Image.open(gif_path)
        self.all_frames = {"RIGHT": [], "DOWN": [], "LEFT": [], "UP": []}
        for frame in ImageSequence.Iterator(gif_data):
            base = frame.convert("RGBA").resize((85, 55))
            if self.nyan_opacity < 1.0:
                alpha = base.getchannel('A').point(lambda i: i * self.nyan_opacity)
                base.putalpha(alpha)
            self.all_frames["RIGHT"].append(ImageTk.PhotoImage(base))
            self.all_frames["DOWN"].append(ImageTk.PhotoImage(base.rotate(-90, expand=True)))
            self.all_frames["LEFT"].append(ImageTk.PhotoImage(base.transpose(Image.FLIP_LEFT_RIGHT)))
            self.all_frames["UP"].append(ImageTk.PhotoImage(base.rotate(90, expand=True)))
        
        curr, x, y, f_idx = "RIGHT", 10, 10, 0
        cat_id = self.nyan_canvas.create_image(x, y, image=self.all_frames[curr][0], anchor="nw")
        
        while self.root.winfo_exists():
            if curr == "RIGHT": 
                x += 8
                if x >= self.win_w - 95: curr = "DOWN"
            elif curr == "DOWN": 
                y += 8
                if y >= self.win_h - 95: curr = "LEFT"
            elif curr == "LEFT": 
                x -= 8
                if x <= 10: curr = "UP"
            elif curr == "UP": 
                y -= 8
                if y <= 10: curr = "RIGHT"
            
            self.nyan_canvas.itemconfig(cat_id, image=self.all_frames[curr][f_idx % len(self.all_frames[curr])])
            self.nyan_canvas.coords(cat_id, x, y)
            f_idx += 1
            time.sleep(self.nyan_speed / 1000.0)

    def animate_title_rgb(self):
        while self.root.winfo_exists():
            try:
                self.title_label.config(fg=self.rgb_colors[self.rgb_index])
                self.rgb_index = (self.rgb_index + 1) % len(self.rgb_colors)
                time.sleep(0.05)
            except: 
                pass

    def setup_ui(self):
        self.nyan_canvas = Canvas(self.root, width=self.win_w, height=self.win_h, highlightthickness=0)
        self.nyan_canvas.place(x=0, y=0)
        
        self.main_card = tk.Frame(self.root, padx=30, pady=20)
        self.main_card.place(relx=0.5, rely=0.45, anchor="center")
        
        self.ascii_label = tk.Label(self.main_card, font=("Consolas", 10))
        self.ascii_label.pack()
        
        self.title_label = tk.Label(self.main_card, text="", font=("Segoe UI", 26, "bold"))
        self.title_label.pack(pady=10)
        
        self.settings_btn = tk.Button(self.main_card, command=self.open_settings, relief="flat", font=("Segoe UI", 10, "bold"), fg="white", width=35)
        self.settings_btn.pack(pady=5)
        
        btn_container = tk.Frame(self.main_card, bg=self.main_card["bg"])
        btn_container.pack(pady=10)
        
        self.summon_btn = tk.Button(btn_container, command=lambda: threading.Thread(target=self.fetch_filtered_video).start(), width=30, height=2, bg="#FF85A2", fg="white", font=("Segoe UI", 11, "bold"), borderwidth=0)
        self.summon_btn.pack(pady=5)
        
        self.dose_btn = tk.Button(btn_container, command=lambda: threading.Thread(target=self.load_cat_image).start(), width=30, height=2, bg="#98D8D8", fg="white", font=("Segoe UI", 11, "bold"), borderwidth=0)
        self.dose_btn.pack(pady=5)
        
        self.img_label = Label(self.main_card, font=("Segoe UI", 11), pady=12)
        self.img_label.pack()
        
        self.log_frame = tk.Frame(self.main_card, pady=10)
        self.log_frame.pack(fill="x")
        
        self.log_label = tk.Label(self.log_frame, font=("Segoe UI", 9, "bold"))
        self.log_label.pack(anchor="w")
        
        self.log_text = Text(self.log_frame, height=5, width=45, font=("Consolas", 8), state="disabled", relief="flat")
        self.log_text.pack(side="left", fill="both")
        
        scrollbar = Scrollbar(self.log_frame, command=self.log_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.log_text.config(yscrollcommand=scrollbar.set)

if __name__ == "__main__":
    root = tk.Tk()
    app = ProjectHub(root)
    root.mainloop()