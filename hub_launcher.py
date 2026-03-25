import tkinter as tk
from tkinter import Label, Canvas
from PIL import ImageTk, Image, ImageSequence, ImageOps
import pygame
import catyy
import threading
import requests
import io
import os
import json
import time

class ProjectHub:
    def __init__(self, root):
        self.root = root
        self.root.title("Paw Session 🐾")
        
        screen_h = self.root.winfo_screenheight()
        self.win_w = 600
        self.win_h = int(screen_h * 0.85)
        self.root.geometry(f"{self.win_w}x{self.win_h}")
        self.root.resizable(False, False)
        
        self.config_file = "settings.json"
        self.settings = self.load_settings()
        self.dark_mode = self.settings.get("dark_mode", False)
        
        self.themes = {
            "light": {"bg": "#FFF5F7", "card": "#FFFFFF", "text": "#4A4A4A", "accent": "#FF85A2"},
            "dark": {"bg": "#1A1A1B", "card": "#2D2D2E", "text": "#E4E6EB", "accent": "#FFACBF"}
        }
        
        self.rgb_colors = ["#FF0000", "#FF4500", "#FFD700", "#00FF00", "#00FFFF", "#0000FF", "#8A2BE2", "#FF00FF"]
        self.rgb_index = 0
        
        if os.path.exists("cat.ico"):
            self.root.iconbitmap("cat.ico")
            
        pygame.mixer.init()
        self.root.config(cursor="heart")
        
        self.setup_ui()
        self.set_theme()
        
        threading.Thread(target=self.animate_nyan_rotating, daemon=True).start()
        threading.Thread(target=self.animate_title_rgb, daemon=True).start()

    def load_settings(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f:
                    return json.load(f)
            except: pass
        return {}

    def save_settings(self):
        with open(self.config_file, "w") as f:
            json.dump({"dark_mode": self.dark_mode}, f)

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.save_settings()
        self.set_theme()

    def set_theme(self):
        t = self.themes["dark"] if self.dark_mode else self.themes["light"]
        self.root.configure(bg=t["bg"])
        self.main_card.configure(bg=t["card"])
        self.title_label.configure(bg=t["card"])
        self.ascii_label.configure(bg=t["card"], fg=t["text"])
        self.theme_btn.configure(text="🌙 Night Mode" if not self.dark_mode else "☀️ Day Mode", bg=t["accent"])
        self.img_label.configure(bg=t["card"], fg=t["text"])
        self.nyan_canvas.configure(bg=t["bg"], highlightbackground=t["bg"])

    def play_meow(self):
        def stream():
            try:
                r = requests.get("https://www.soundjay.com/nature/sounds/cat-meow-01.mp3", timeout=5)
                pygame.mixer.music.load(io.BytesIO(r.content))
                pygame.mixer.music.play()
            except: pass
        threading.Thread(target=stream).start()

    def load_cat_image(self):
        self.play_meow()
        self.img_label.config(text="Catching the goofy cat...", image="")
        img = catyy.fetch_cat_image()
        if img:
            # Sabit çözünürlük: 400x300 (Orantılı kesme ve boyutlandırma)
            fixed_img = ImageOps.fit(img, (400, 300), Image.Resampling.LANCZOS)
            tk_img = ImageTk.PhotoImage(fixed_img)
            self.img_label.config(image=tk_img, text="")
            self.img_label.image = tk_img
        else:
            self.img_label.config(text="Cat escaped! Try again.")

    def animate_nyan_rotating(self):
        gif_path = "nyan-cat.gif"
        if not os.path.exists(gif_path): return
        try:
            gif_data = Image.open(gif_path)
            self.all_frames = {"RIGHT": [], "DOWN": [], "LEFT": [], "UP": []}
            w, h = 85, 55
            for frame in ImageSequence.Iterator(gif_data):
                base = frame.convert("RGBA").resize((w, h))
                self.all_frames["RIGHT"].append(ImageTk.PhotoImage(base))
                self.all_frames["DOWN"].append(ImageTk.PhotoImage(base.rotate(-90, expand=True)))
                self.all_frames["LEFT"].append(ImageTk.PhotoImage(base.transpose(Image.FLIP_LEFT_RIGHT)))
                self.all_frames["UP"].append(ImageTk.PhotoImage(base.rotate(90, expand=True)))
            curr = "RIGHT"
            cat_id = self.nyan_canvas.create_image(10, 10, image=self.all_frames[curr][0], anchor="nw")
            x, y, f_idx = 10, 10, 0
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
                f_idx += 1
                self.nyan_canvas.itemconfig(cat_id, image=self.all_frames[curr][f_idx % len(self.all_frames[curr])])
                self.nyan_canvas.coords(cat_id, x, y)
                time.sleep(0.04)
        except: pass

    def animate_title_rgb(self):
        while self.root.winfo_exists():
            try:
                self.title_label.config(fg=self.rgb_colors[self.rgb_index])
                self.rgb_index = (self.rgb_index + 1) % len(self.rgb_colors)
                time.sleep(0.05)
            except: pass

    def on_hover(self, e, widget, color): widget['bg'] = color

    def setup_ui(self):
        self.nyan_canvas = Canvas(self.root, width=self.win_w, height=self.win_h, highlightthickness=0)
        self.nyan_canvas.place(x=0, y=0)
        self.main_card = tk.Frame(self.root, padx=30, pady=20)
        self.main_card.place(relx=0.5, rely=0.5, anchor="center")
        
        ascii_art = "         _._     _,-'\"\"`-._\n        (,-.`._,'(       |\\`-/|\n            `-.-' \\ )-`( , o o)\n                  `-    \\`_`\"'-"
        self.ascii_label = tk.Label(self.main_card, text=ascii_art, font=("Consolas", 10))
        self.ascii_label.pack()
        
        self.title_label = tk.Label(self.main_card, text="Paw Session", font=("Segoe UI", 26, "bold"))
        self.title_label.pack(pady=10)
        
        self.theme_btn = tk.Button(self.main_card, command=self.toggle_theme, relief="flat", font=("Segoe UI", 10), fg="white")
        self.theme_btn.pack(pady=5)
        
        btn_c = tk.Frame(self.main_card, bg=self.main_card["bg"])
        btn_c.pack(pady=10)
        
        for text, cmd, clr, hov in [("Summon Video", lambda: catyy.open_video_in_browser(catyy.fetch_popular_cat_video()['id']), "#FF85A2", "#FF507A"),
                                    ("Daily Goofy Dose", lambda: threading.Thread(target=self.load_cat_image).start(), "#98D8D8", "#7AC9C9")]:
            btn = tk.Button(btn_c, text=text, command=cmd, width=20, height=2, bg=clr, fg="white", font=("Segoe UI", 11, "bold"), borderwidth=0)
            btn.pack(pady=5)
            btn.bind("<Enter>", lambda e, b=btn, c=hov: self.on_hover(e, b, c))
            btn.bind("<Leave>", lambda e, b=btn, c=clr: self.on_hover(e, b, c))
            
        self.img_label = Label(self.main_card, text="Waiting for goofiness...", font=("Segoe UI", 10), pady=10)
        self.img_label.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = ProjectHub(root)
    root.mainloop()