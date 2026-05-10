import pyautogui
import keyboard
import time

print("🖱️ Arahkan mouse ke area yang ingin kamu tandai.")
print("📍 Koordinat akan tampil setiap 0.5 detik.")
print("📌 Tekan tombol 'y' untuk menyimpan titik.")
print("❌ Tekan Ctrl+C untuk keluar.\n")
time.sleep(2)

try:
    while True:
        x, y = pyautogui.position()
        print(f"Koordinat mouse: ({x}, {y})", end="\r")

        if keyboard.is_pressed('y'):
            print(f"\n📌 Koordinat disimpan: ({x}, {y})")
            while keyboard.is_pressed('y'):  # tunggu sampai dilepas
                time.sleep(0.1)

        time.sleep(0.5)

except KeyboardInterrupt:
    print("\n⛔ Selesai. Tutup skrip.")
