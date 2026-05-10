import customtkinter as ctk
import json
import os
import time
import threading
import sys

try:
    import pyautogui
    import pyperclip
    from pynput import keyboard as pynput_keyboard
    from pynput import mouse as pynput_mouse
except ImportError as e:
    print(f"Library belum terinstall: {e}")
    print("Jalankan: pip install customtkinter pyautogui pyperclip pynput")
    sys.exit(1)

# ══════════════════════════════════════════
#  KONFIGURASI TAMPILAN
# ══════════════════════════════════════════
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

CONFIG_FILE = "config.json"

FIELDS = [
    ("jenis_jalan",        "Kolom Jenis Jalan"),
    ("jenis_kerusakan",    "Kolom Jenis Kerusakan"),
    ("keparahan",          "Kolom Tingkat Keparahan"),
    ("lebar_lajur",        "Kolom Lebar Lajur"),
    ("tombol_simpan",      "Tombol Simpan"),
    ("koordinat_d",        "Tombol Navigasi D"),
    ("koordinat_f",        "Tombol Navigasi F"),
    ("koordinat_h",        "Tombol Navigasi H"),
    ("koordinat_backtick", "Tombol Simpan Alternatif (`)"),
]

JENIS_KERUSAKAN = [
    ("Pelapukan/Pelepasan Butir",   "Alt+1"),
    ("Kegemukan/Bleeding",          "Alt+2"),
    ("Tambalan",                    "Alt+3"),
    ("Retak Memanjang & Melintang", "Alt+4"),
    ("Lubang",                      "Alt+5"),
    ("Retak Kulit Buaya",           "Alt+6"),
    ("Keriting",                    "Alt+7"),
    ("Retak Blok",                  "Alt+8"),
    ("Depresi",                     "Alt+9"),
    ("Sungkur (Shoving)",           "Alt+0"),
    ("Retak Selip",                 "Alt+Q"),
]


# ══════════════════════════════════════════
#  LOAD / SAVE CONFIG
# ══════════════════════════════════════════
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}

def save_config(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=2)


# ══════════════════════════════════════════
#  LOGIKA OTOMATISASI
# ══════════════════════════════════════════
def format_lebar(nilai):
    return str(int(nilai)) if nilai == int(nilai) else str(nilai)

def isi_form_awal(jenis_kerusakan, config, log_fn):
    x, y = config["jenis_jalan"]
    pyautogui.click(x, y)
    pyperclip.copy("Perkerasan Beton Aspal")
    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.02)

    x, y = config["jenis_kerusakan"]
    pyautogui.click(x, y)
    pyperclip.copy(jenis_kerusakan)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.02)

    log_fn(f"✅ Diisi: {jenis_kerusakan} — gambar kotak secara manual")

def isi_lajur_dan_simpan(config, lebar_lajur_input, log_fn):
    x, y = config["lebar_lajur"]
    pyautogui.click(x, y)
    time.sleep(0.05)
    pyautogui.hotkey("ctrl", "a")
    pyautogui.hotkey("ctrl", "c")
    time.sleep(0.05)

    isi_lajur = pyperclip.paste().strip()
    lebar_str = format_lebar(lebar_lajur_input)

    if isi_lajur == "" or isi_lajur != lebar_str:
        pyautogui.hotkey("ctrl", "a")
        pyautogui.press("backspace")
        pyperclip.copy(lebar_str)
        pyautogui.hotkey("ctrl", "v")
        log_fn(f"✍️  Lebar lajur ditulis: {lebar_str} m")
    else:
        log_fn(f"🔁 Lebar lajur sudah benar: {lebar_str} m")

    x, y = config["tombol_simpan"]
    pyautogui.click(x, y)
    log_fn("💾 Disimpan!")

def isi_keparahan(teks, config, lebar_lajur_input, log_fn):
    x, y = config["keparahan"]
    pyautogui.click(x, y)
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("backspace")
    pyperclip.copy(teks)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.02)
    log_fn(f"🟡 Keparahan: {teks}")
    isi_lajur_dan_simpan(config, lebar_lajur_input, log_fn)


# ══════════════════════════════════════════
#  HALAMAN SETUP WIZARD
# ══════════════════════════════════════════
class SetupWizard(ctk.CTkFrame):
    def __init__(self, master, on_done):
        super().__init__(master, fg_color="transparent")
        self.on_done = on_done
        self.config_data = {}
        self.current_index = 0
        self.capturing = False

        ctk.CTkLabel(self, text="⚙️  Setup Koordinat",
                     font=ctk.CTkFont(size=22, weight="bold")).pack(pady=(20, 5))
        ctk.CTkLabel(self, text="Klik setiap kolom di form Bhineka satu per satu",
                     font=ctk.CTkFont(size=13), text_color="gray").pack(pady=(0, 20))

        self.progress_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=14))
        self.progress_label.pack(pady=5)

        self.progress_bar = ctk.CTkProgressBar(self, width=400)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=10)

        self.instruction_box = ctk.CTkLabel(
            self, text="", font=ctk.CTkFont(size=15, weight="bold"),
            wraplength=450, justify="center",
            fg_color=("gray85", "gray20"), corner_radius=10,
            padx=20, pady=15
        )
        self.instruction_box.pack(pady=20, padx=30, fill="x")

        self.countdown_label = ctk.CTkLabel(
            self, text="",
            font=ctk.CTkFont(size=40, weight="bold"),
            text_color="#3B8ED0"
        )
        self.countdown_label.pack(pady=5)

        self.btn_start = ctk.CTkButton(
            self, text="▶  Mulai Tangkap Koordinat",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=45, command=self.start_capture
        )
        self.btn_start.pack(pady=15)

        self.result_frame = ctk.CTkScrollableFrame(
            self, height=150, label_text="Koordinat yang sudah ditangkap")
        self.result_frame.pack(pady=10, padx=20, fill="x")

        self.update_ui()

    # ── helper: update UI dari thread secara aman ──
    def ui(self, fn):
        """Jadwalkan fn di main thread supaya tidak crash."""
        self.master.after(0, fn)

    def update_ui(self):
        idx = self.current_index
        self.progress_bar.set(idx / len(FIELDS))
        self.progress_label.configure(text=f"Langkah {idx + 1} dari {len(FIELDS)}")
        key, label = FIELDS[idx]
        self.instruction_box.configure(text=f"Klik pada:\n\n🎯  {label}")
        self.countdown_label.configure(text="")

    def start_capture(self):
        if self.capturing:
            return
        self.capturing = True
        self.btn_start.configure(state="disabled", text="Menunggu klik...")
        threading.Thread(target=self.capture_with_countdown, daemon=True).start()

    def capture_with_countdown(self):
        # Countdown — semua UI update pakai self.ui() agar aman dari thread
        for i in range(3, 0, -1):
            self.ui(lambda i=i: self.countdown_label.configure(text=str(i)))
            time.sleep(1)

        self.ui(lambda: self.countdown_label.configure(text="🖱️ Klik sekarang!"))

        # Sembunyikan window
        self.ui(lambda: self.master.withdraw())
        time.sleep(0.5)

        # Tangkap klik pakai pynput
        clicked = threading.Event()
        coords = [0, 0]

        def on_click(x, y, button, pressed):
            if pressed and button == pynput_mouse.Button.left:
                coords[0], coords[1] = x, y
                clicked.set()
                return False

        with pynput_mouse.Listener(on_click=on_click):
            clicked.wait()

        x, y = coords[0], coords[1]
        time.sleep(0.2)

        # Tampilkan window kembali
        self.ui(lambda: self.master.deiconify())
        time.sleep(0.2)

        # Simpan koordinat
        key, label = FIELDS[self.current_index]
        self.config_data[key] = [x, y]

        # Update UI secara aman
        self.ui(lambda: self.countdown_label.configure(text=f"✅  ({x}, {y})"))
        self.ui(lambda: self.update_result(label, x, y))

        self.capturing = False
        self.current_index += 1

        if self.current_index >= len(FIELDS):
            save_config(self.config_data)
            self.ui(lambda: self.countdown_label.configure(text="✅ Semua koordinat tersimpan!"))
            self.ui(lambda: self.btn_start.configure(state="disabled", text="Selesai!"))
            self.ui(lambda: self.progress_bar.set(1.0))
            self.ui(lambda: self.progress_label.configure(
                text=f"Selesai! {len(FIELDS)} koordinat tersimpan"))
            time.sleep(1.5)
            self.ui(lambda: self.on_done(self.config_data))
        else:
            self.ui(lambda: self.update_ui())
            self.ui(lambda: self.btn_start.configure(
                state="normal", text="▶  Tangkap Berikutnya"))

    def update_result(self, label, x, y):
        row = ctk.CTkFrame(self.result_frame, fg_color="transparent")
        row.pack(fill="x", pady=2)
        ctk.CTkLabel(row, text=f"✔  {label}",
                     font=ctk.CTkFont(size=12), anchor="w").pack(side="left", padx=5)
        ctk.CTkLabel(row, text=f"({x}, {y})",
                     font=ctk.CTkFont(size=12),
                     text_color="#3B8ED0").pack(side="right", padx=5)


# ══════════════════════════════════════════
#  HALAMAN UTAMA
# ══════════════════════════════════════════
class MainPanel(ctk.CTkFrame):
    def __init__(self, master, config, on_reset_coords):
        super().__init__(master, fg_color="transparent")
        self.config = config
        self.on_reset_coords = on_reset_coords
        self.lebar_lajur = 3.5
        self.running = False
        self.hotkey_listener = None
        self._build_ui()

    # ── helper: update UI dari thread secara aman ──
    def ui(self, fn):
        self.master.after(0, fn)

    def _build_ui(self):
        # Header
        header = ctk.CTkFrame(self, fg_color=("gray90", "gray15"), corner_radius=12)
        header.pack(fill="x", padx=15, pady=(15, 5))

        ctk.CTkLabel(header, text="🛣️  Otomatisasi Survei Jalan",
                     font=ctk.CTkFont(size=20, weight="bold")).pack(side="left", padx=15, pady=10)

        ctk.CTkButton(header, text="⚙️ Ubah Koordinat", width=140,
                      fg_color="transparent", border_width=1,
                      command=self.on_reset_coords).pack(side="right", padx=10, pady=10)

        # Lebar Lajur
        lebar_frame = ctk.CTkFrame(self, fg_color=("gray90", "gray15"), corner_radius=12)
        lebar_frame.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(lebar_frame, text="📏 Lebar Lajur (m):",
                     font=ctk.CTkFont(size=14)).pack(side="left", padx=15, pady=10)

        self.lebar_entry = ctk.CTkEntry(lebar_frame, width=80, placeholder_text="3.5")
        self.lebar_entry.insert(0, "3.5")
        self.lebar_entry.pack(side="left", padx=5)

        ctk.CTkButton(lebar_frame, text="Simpan", width=80,
                      command=self.simpan_lebar).pack(side="left", padx=5)

        self.lebar_status = ctk.CTkLabel(
            lebar_frame, text="✅ 3.5 m",
            text_color="#3B8ED0", font=ctk.CTkFont(size=13))
        self.lebar_status.pack(side="left", padx=10)

        # Start/Stop
        self.btn_start = ctk.CTkButton(
            self, text="▶  Mulai Otomatisasi",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=45, fg_color="#2FA572", hover_color="#1F7A55",
            command=self.toggle_automation
        )
        self.btn_start.pack(fill="x", padx=15, pady=5)

        # Panel 2 kolom
        columns = ctk.CTkFrame(self, fg_color="transparent")
        columns.pack(fill="both", expand=True, padx=15, pady=5)
        columns.columnconfigure(0, weight=1)
        columns.columnconfigure(1, weight=1)

        # Kolom kiri: Jenis Kerusakan
        left = ctk.CTkFrame(columns, fg_color=("gray90", "gray15"), corner_radius=12)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 5), pady=5)

        ctk.CTkLabel(left, text="🔍 Jenis Kerusakan",
                     font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(10, 5))

        for nama, hk in JENIS_KERUSAKAN:
            row = ctk.CTkFrame(left, fg_color="transparent")
            row.pack(fill="x", padx=10, pady=2)
            ctk.CTkButton(
                row, text=nama, height=32,
                font=ctk.CTkFont(size=12),
                fg_color=("gray80", "gray25"),
                text_color=("gray10", "gray95"),
                hover_color=("gray70", "gray35"),
                anchor="w",
                command=lambda n=nama: self.klik_kerusakan(n)
            ).pack(side="left", fill="x", expand=True)
            ctk.CTkLabel(
                row, text=hk, width=55,
                font=ctk.CTkFont(size=11),
                text_color="#3B8ED0",
                fg_color=("gray75", "gray30"),
                corner_radius=5
            ).pack(side="right", padx=(3, 0))

        # Kolom kanan
        right = ctk.CTkFrame(columns, fg_color=("gray90", "gray15"), corner_radius=12)
        right.grid(row=0, column=1, sticky="nsew", padx=(5, 0), pady=5)

        # Keparahan
        ctk.CTkLabel(right, text="⚠️  Tingkat Keparahan",
                     font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(10, 5))

        kep_frame = ctk.CTkFrame(right, fg_color="transparent")
        kep_frame.pack(fill="x", padx=10)
        kep_frame.columnconfigure(0, weight=1)
        kep_frame.columnconfigure(1, weight=1)
        kep_frame.columnconfigure(2, weight=1)

        for i, (level, fg, hover, hk) in enumerate([
            ("Rendah", "#2FA572", "#1F7A55", "Alt+W"),
            ("Sedang", "#D4A017", "#A07810", "Alt+E"),
            ("Tinggi", "#C0392B", "#922B21", "Alt+R"),
        ]):
            ctk.CTkButton(
                kep_frame, text=f"{level}\n{hk}", height=45,
                font=ctk.CTkFont(size=12, weight="bold"),
                fg_color=fg, hover_color=hover,
                command=lambda l=level: self.klik_keparahan(l)
            ).grid(row=0, column=i, padx=3, pady=5, sticky="ew")

        # Navigasi
        ctk.CTkLabel(right, text="🖱️  Tombol Navigasi",
                     font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(15, 5))

        nav_frame = ctk.CTkFrame(right, fg_color="transparent")
        nav_frame.pack(fill="x", padx=10)

        for label, key in [
            ("D\nAlt+D", "koordinat_d"),
            ("F\nAlt+F", "koordinat_f"),
            ("H\nAlt+H", "koordinat_h"),
            ("S\nAlt+S", "koordinat_backtick")
        ]:
            ctk.CTkButton(
                nav_frame, text=label, width=65, height=45,
                font=ctk.CTkFont(size=11),
                command=lambda k=key: self.klik_navigasi(k)
            ).pack(side="left", padx=3)

        # Log
        ctk.CTkLabel(right, text="📋 Log Aktivitas",
                     font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(15, 5))

        self.log_box = ctk.CTkTextbox(right, height=180, font=ctk.CTkFont(size=11))
        self.log_box.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.log_box.configure(state="disabled")

        self.log("💻 Aplikasi siap digunakan.")
        self.log(f"📏 Lebar lajur: {self.lebar_lajur} m")
        self.log("ℹ️  Tekan ▶ Mulai untuk mengaktifkan hotkey.")

    def log(self, pesan):
        """Log aman dipanggil dari thread manapun."""
        def _do():
            self.log_box.configure(state="normal")
            self.log_box.insert("end", pesan + "\n")
            self.log_box.see("end")
            self.log_box.configure(state="disabled")
        self.master.after(0, _do)

    def simpan_lebar(self):
        try:
            nilai = float(self.lebar_entry.get())
            self.lebar_lajur = nilai
            self.lebar_status.configure(
                text=f"✅ {format_lebar(nilai)} m", text_color="#3B8ED0")
            self.log(f"📏 Lebar lajur diubah: {format_lebar(nilai)} m")
        except ValueError:
            self.lebar_status.configure(text="❌ Nilai tidak valid", text_color="red")

    def toggle_automation(self):
        if not self.running:
            self.start_automation()
        else:
            self.stop_automation()

    def start_automation(self):
        self.running = True
        self.btn_start.configure(
            text="⏹  Stop Otomatisasi",
            fg_color="#C0392B", hover_color="#922B21"
        )
        self.log("▶️  Otomatisasi dimulai! Hotkey aktif.")

        cfg = self.config

        def run(fn, *args):
            threading.Thread(target=fn, args=args, daemon=True).start()

        hotkey_map = {
            '<alt>+1': lambda: run(isi_form_awal, "Pelapukan/Pelepasan Butir", cfg, self.log),
            '<alt>+2': lambda: run(isi_form_awal, "Kegemukan/Bleeding", cfg, self.log),
            '<alt>+3': lambda: run(isi_form_awal, "Tambalan", cfg, self.log),
            '<alt>+4': lambda: run(isi_form_awal, "Retak Memanjang & Melintang", cfg, self.log),
            '<alt>+5': lambda: run(isi_form_awal, "Lubang", cfg, self.log),
            '<alt>+6': lambda: run(isi_form_awal, "Retak Kulit Buaya", cfg, self.log),
            '<alt>+7': lambda: run(isi_form_awal, "Keriting", cfg, self.log),
            '<alt>+8': lambda: run(isi_form_awal, "Retak Blok", cfg, self.log),
            '<alt>+9': lambda: run(isi_form_awal, "Depresi", cfg, self.log),
            '<alt>+0': lambda: run(isi_form_awal, "Sungkur (Shoving)", cfg, self.log),
            '<alt>+q': lambda: run(isi_form_awal, "Retak Selip", cfg, self.log),
            '<alt>+w': lambda: run(isi_keparahan, "Rendah", cfg, self.lebar_lajur, self.log),
            '<alt>+e': lambda: run(isi_keparahan, "Sedang", cfg, self.lebar_lajur, self.log),
            '<alt>+r': lambda: run(isi_keparahan, "Tinggi", cfg, self.lebar_lajur, self.log),
            '<alt>+d': lambda: run(self.klik_navigasi, "koordinat_d"),
            '<alt>+f': lambda: run(self.klik_navigasi, "koordinat_f"),
            '<alt>+h': lambda: run(self.klik_navigasi, "koordinat_h"),
            '<alt>+s': lambda: run(self.klik_navigasi, "koordinat_backtick"),
        }

        self.hotkey_listener = pynput_keyboard.GlobalHotKeys(hotkey_map)
        self.hotkey_listener.start()
        self.log("⌨️  Semua hotkey Alt siap dipakai.")

    def stop_automation(self):
        self.running = False
        if self.hotkey_listener:
            self.hotkey_listener.stop()
            self.hotkey_listener = None
        self.btn_start.configure(
            text="▶  Mulai Otomatisasi",
            fg_color="#2FA572", hover_color="#1F7A55"
        )
        self.log("⏹  Otomatisasi dihentikan.")

    def klik_kerusakan(self, nama):
        if not self.running:
            self.log("⚠️  Tekan ▶ Mulai dulu!")
            return
        threading.Thread(
            target=isi_form_awal,
            args=(nama, self.config, self.log),
            daemon=True
        ).start()

    def klik_keparahan(self, level):
        if not self.running:
            self.log("⚠️  Tekan ▶ Mulai dulu!")
            return
        threading.Thread(
            target=isi_keparahan,
            args=(level, self.config, self.lebar_lajur, self.log),
            daemon=True
        ).start()

    def klik_navigasi(self, key):
        if key in self.config:
            x, y = self.config[key]
            pyautogui.click(x, y)
            self.log(f"🖱️  Navigasi: {key} → ({x}, {y})")


# ══════════════════════════════════════════
#  APP UTAMA
# ══════════════════════════════════════════
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🛣️  AutoBhineka")
        self.geometry("900x680")
        self.minsize(800, 600)
        self.resizable(True, True)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.current_frame = None
        config = load_config()

        if config and all(k in config for k, _ in FIELDS):
            self.show_main(config)
        else:
            self.show_setup()

    def on_close(self):
        if isinstance(self.current_frame, MainPanel):
            self.current_frame.stop_automation()
        self.destroy()

    def clear(self):
        if self.current_frame:
            self.current_frame.destroy()

    def show_setup(self):
        self.clear()
        self.geometry("600x600")
        self.current_frame = SetupWizard(self, on_done=self.show_main)
        self.current_frame.pack(fill="both", expand=True)

    def show_main(self, config):
        self.clear()
        self.geometry("900x680")
        self.current_frame = MainPanel(
            self, config, on_reset_coords=self.show_setup)
        self.current_frame.pack(fill="both", expand=True)


# ══════════════════════════════════════════
#  JALANKAN
# ══════════════════════════════════════════
if __name__ == "__main__":
    app = App()
    app.mainloop()