import pyautogui
import keyboard
import pyperclip
import time
import sys
import tkinter as tk
from tkinter import simpledialog

# Ambil ukuran layar
lebar_layar, tinggi_layar = pyautogui.size()

# =============================
# FUNGSI FORM INPUT UTAMA
# =============================

def isi_jenis_jalan():
    pyautogui.moveTo(1258, 193, duration=0.05)
    pyautogui.click()
    pyperclip.copy("Perkerasan Beton Aspal")
    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.01)

def isi_jenis_kerusakan(teks):
    pyautogui.moveTo(1258, 212, duration=0.05)
    pyautogui.click()
    pyperclip.copy(teks)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.01)

def isi_form_awal(jenis_kerusakan):
    print(f"🟢 Mengisi Jenis Jalan dan Jenis Kerusakan ({jenis_kerusakan})...")
    time.sleep(0.1)
    isi_jenis_jalan()
    isi_jenis_kerusakan(jenis_kerusakan)
    print("⏸️ Silakan gambar kotaknya secara manual.")
    pyautogui.moveTo(lebar_layar / 2, tinggi_layar / 2, duration=0.2)

# =============================
# FUNGSI TINGKAT KEPARAHAN + SIMPAN
# =============================

def klik_simpan():
    pyautogui.moveTo(1309, 385, duration=0.05)
    pyautogui.click()
    print("✅ Data disimpan.")

def isi_form_lanjutan():
    print("🔵 Mengisi Tingkat Keparahan: Rendah...")
    time.sleep(0.1)
    pyautogui.moveTo(1268, 256, duration=0.05)
    pyautogui.click()
    pyperclip.copy("Rendah")
    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.01)
    klik_simpan()

def isi_keparahan(teks_keparahan):
    print(f"🟡 Mengisi Tingkat Keparahan: {teks_keparahan}...")
    pyautogui.moveTo(1268, 256, duration=0.05)
    pyautogui.click()
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('backspace')
    pyperclip.copy(teks_keparahan)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.01)
    klik_simpan()

# =============================
# KOORDINAT MANUAL
# =============================

def klik_koordinat(x, y):
    pyautogui.moveTo(x, y, duration=0.05)
    pyautogui.click()

# =============================
# INFORMASI
# =============================

print("💻 Otomatisasi Bhineka SIAP.")
print("\n--- HOTKEY ---")
print("Ctrl+Z = Pelapukan/Pelepasan Butir")
print("Ctrl+K = Kegemukan/Bleeding")
print("Ctrl+T = Tambalan")
print("Ctrl+M = Retak Memanjang & Melintang")
print("Ctrl+L = Lubang")
print("Ctrl+B = Retak Kulit Buaya")
print("Ctrl+1 = Keriting")
print("Ctrl+2 = Retak Blok")
print("Ctrl+3 = Depresi")
print("Ctrl+4 = Sungkur (Shoving)")
print("Ctrl+5 = Retak Selip")
print("Ctrl+W = Rendah + Simpan")
print("Ctrl+E = Sedang + Simpan")
print("Ctrl+R = Tinggi + Simpan")
print("`       = Klik koordinat (1312, 382)")
print("D       = Klik koordinat ke-6 (688, 84)")
print("F       = Klik koordinat ke-7 (719, 86)")
print("Ctrl+H  = Klik koordinat ke-8 (1179, 412)")
print("Ctrl+Q  = STOP")

# =============================
# LOOP UTAMA
# =============================

try:
    while True:
        if keyboard.is_pressed('ctrl+z'):
            isi_form_awal("Pelapukan/Pelepasan Butir")
            while keyboard.is_pressed('ctrl+z'): pass

        elif keyboard.is_pressed('ctrl+k'):
            isi_form_awal("Kegemukan/Bleeding")
            while keyboard.is_pressed('ctrl+k'): pass

        elif keyboard.is_pressed('ctrl+t'):
            isi_form_awal("Tambalan")
            while keyboard.is_pressed('ctrl+t'): pass

        elif keyboard.is_pressed('ctrl+m'):
            isi_form_awal("Retak Memanjang & Melintang")
            while keyboard.is_pressed('ctrl+m'): pass

        elif keyboard.is_pressed('ctrl+l'):
            isi_form_awal("Lubang")
            while keyboard.is_pressed('ctrl+l'): pass

        elif keyboard.is_pressed('ctrl+b'):
            isi_form_awal("Retak Kulit Buaya")
            while keyboard.is_pressed('ctrl+b'): pass

        elif keyboard.is_pressed('ctrl+1'):
            isi_form_awal("Keriting")
            while keyboard.is_pressed('ctrl+1'): pass

        elif keyboard.is_pressed('ctrl+2'):
            isi_form_awal("Retak Blok")
            while keyboard.is_pressed('ctrl+2'): pass

        elif keyboard.is_pressed('ctrl+3'):
            isi_form_awal("Depresi")
            while keyboard.is_pressed('ctrl+3'): pass

        elif keyboard.is_pressed('ctrl+4'):
            isi_form_awal("Sungkur (Shoving)")
            while keyboard.is_pressed('ctrl+4'): pass

        elif keyboard.is_pressed('ctrl+5'):
            isi_form_awal("Retak Selip")
            while keyboard.is_pressed('ctrl+5'): pass

        elif keyboard.is_pressed('ctrl+w'):
            isi_form_lanjutan()
            while keyboard.is_pressed('ctrl+w'): pass

        elif keyboard.is_pressed('ctrl+e'):
            isi_keparahan("Sedang")
            while keyboard.is_pressed('ctrl+e'): pass

        elif keyboard.is_pressed('ctrl+r'):
            isi_keparahan("Tinggi")
            while keyboard.is_pressed('ctrl+r'): pass

        elif keyboard.is_pressed('d'):
            klik_koordinat(688, 84)
            while keyboard.is_pressed('d'): pass

        elif keyboard.is_pressed('f'):
            klik_koordinat(719, 86)
            while keyboard.is_pressed('f'): pass

        elif keyboard.is_pressed('ctrl+h'):
            klik_koordinat(1179, 412)
            while keyboard.is_pressed('ctrl+h'): pass

        elif keyboard.is_pressed('`'):
            klik_koordinat(1312, 382)
            while keyboard.is_pressed('`'): pass

        elif keyboard.is_pressed('ctrl+q'):
            print("⛔ Otomatisasi dihentikan.")
            sys.exit()

        time.sleep(0.03)

except KeyboardInterrupt:
    print("❌ Dihentikan manual.")
