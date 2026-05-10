import pyautogui
import mouse  # pip install mouse
import time

print("🖱️ Silakan klik kiri 6 kali di posisi yang kamu inginkan.")
print("📍 Setiap klik akan menyimpan koordinat ke terminal.\n")

koordinat = []

def on_click():
    if mouse.is_pressed(button='left'):
        x, y = pyautogui.position()
        koordinat.append((x, y))
        print(f"📌 Klik {len(koordinat)}: ({x}, {y})")

        # Hentikan setelah 6 klik
        if len(koordinat) >= 6:
            print("\n✅ Koordinat lengkap:")
            for i, (x, y) in enumerate(koordinat, 1):
                print(f"{i}. ({x}, {y})")
            exit()

# Jalankan listener
while True:
    on_click()
    time.sleep(0.1)
