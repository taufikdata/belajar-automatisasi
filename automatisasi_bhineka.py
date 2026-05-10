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
# FUNGSI FORMAT DAN INPUT LEBAR LAJUR
# =============================

def format_lebar(nilai):
    return str(int(nilai)) if nilai == int(nilai) else str(nilai)

def input_lebar_lajur():
    root = tk.Tk()
    root.withdraw()
    while True:
        try:
            nilai = simpledialog.askstring("Input", "🫼 Masukkan lebar lajur (m):")
            if nilai is None:
                continue
            return float(nilai)
        except ValueError:
            continue

# Nilai awal
lebar_lajur_input = input_lebar_lajur()

# =============================
# FUNGSI OTOMATISASI FORM
# =============================

def isi_jenis_jalan():
    pyautogui.click(1258, 193)
    pyperclip.copy("Perkerasan Beton Aspal")
    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.02)

def isi_jenis_kerusakan(teks):
    pyautogui.click(1258, 212)
    pyperclip.copy(teks)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.02)

def isi_form_awal(jenis_kerusakan):
    print(f"🟢 Isi Jenis Jalan & Kerusakan: {jenis_kerusakan}")
    isi_jenis_jalan()
    isi_jenis_kerusakan(jenis_kerusakan)
    print("⏸️ Gambar kotaknya secara manual.")
    pyautogui.moveTo(lebar_layar / 2, tinggi_layar / 2)

def isi_lajur_dan_simpan():
    pyautogui.click(1275, 272)
    time.sleep(0.05)

    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.05)

    isi_lajur = pyperclip.paste().strip()
    lebar_str = format_lebar(lebar_lajur_input)

    if isi_lajur == "" or isi_lajur != lebar_str:
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('backspace')
        pyperclip.copy(lebar_str)
        pyautogui.hotkey("ctrl", "v")
        print(f"✍️ Lebar {lebar_str} ditulis.")
    else:
        print(f"🔁 Lebar lajur sudah benar: {lebar_str}")

    pyautogui.click(1309, 385)
    print("✅ Disimpan.")

def isi_form_lanjutan():
    print("🔵 Keparahan: Rendah + Lajur")
    pyautogui.click(1268, 256)
    pyperclip.copy("Rendah")
    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.02)
    isi_lajur_dan_simpan()

def isi_keparahan_dan_lajur(teks_keparahan):
    print(f"🟡 Keparahan: {teks_keparahan} + Lajur")
    pyautogui.click(1268, 256)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('backspace')
    pyperclip.copy(teks_keparahan)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.02)
    isi_lajur_dan_simpan()

def ubah_lebar_lajur():
    global lebar_lajur_input
    lebar_lajur_input = input_lebar_lajur()
    print(f"🔁 Lebar lajur baru: {format_lebar(lebar_lajur_input)} meter")

# =============================
# KOORDINAT MANUAL
# =============================

def klik_koordinat(x, y):
    pyautogui.click(x, y)

# =============================
# INFORMASI
# =============================

print("💻 Otomatisasi Bhineka SIAP.")
print("🫼 Lebar lajur:", format_lebar(lebar_lajur_input))
print("\n--- HOTKEY ---")
print("Ctrl+Z = Pelapukan")
print("Ctrl+K = Kegemukan")
print("Ctrl+T = Tambalan")
print("Ctrl+M = Retak Memanjang")
print("Ctrl+L = Lubang")
print("Ctrl+B = Retak Kulit Buaya")
print("Ctrl+1 = Keriting")
print("Ctrl+2 = Retak Blok")
print("Ctrl+3 = Depresi")
print("Ctrl+4 = Sungkur")
print("Ctrl+5 = Retak Selip")
print("Ctrl+W = Rendah + Lajur")
print("Ctrl+E = Sedang + Lajur + Simpan")
print("Ctrl+R = Tinggi + Lajur + Simpan")
print("Ctrl+U = Ubah Lebar Lajur")
print("D = Klik (688, 84)")
print("F = Klik (719, 86)")
print("Ctrl+H = Klik (1179, 412)")
print("` = Klik (1312, 382)")
print("Ctrl+Q = STOP")

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
            isi_keparahan_dan_lajur("Sedang")
            while keyboard.is_pressed('ctrl+e'): pass

        elif keyboard.is_pressed('ctrl+r'):
            isi_keparahan_dan_lajur("Tinggi")
            while keyboard.is_pressed('ctrl+r'): pass

        elif keyboard.is_pressed('ctrl+u'):
            ubah_lebar_lajur()
            while keyboard.is_pressed('ctrl+u'): pass

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
            print("⛔ Dihentikan.")
            sys.exit()

        time.sleep(0.01)

except KeyboardInterrupt:
    print("❌ Dihentikan manual.")
