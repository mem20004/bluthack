python
import os
import subprocess
import time
from colorama import init, Fore, Style

init(autoreset=True)

# ===== ГРАДИЕНТ =====
def gradient_text(text):
    colors = [Fore.CYAN, Fore.BLUE]
    result = ""
    for i, char in enumerate(text):
        result += colors[i % len(colors)] + char
    return result

# ===== БАННЕР =====
def draw_banner():
    os.system("clear")
    banner = """
██████╗ ██╗     ██╗   ██╗████████╗██╗  ██╗ █████╗  ██████╗██╗  ██╗
██╔══██╗██║     ██║   ██║╚══██╔══╝██║  ██║██╔══██╗██╔════╝██║ ██╔╝
██████╔╝██║     ██║   ██║   ██║   ███████║███████║██║     █████╔╝ 
██╔══██╗██║     ██║   ██║   ██║   ██╔══██║██╔══██║██║     ██╔═██╗ 
██████╔╝███████╗╚██████╔╝   ██║   ██║  ██║██║  ██║╚██████╗██║  ██╗
╚═════╝ ╚══════╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
"""
    print(gradient_text(banner))
    print(gradient_text("        >>> BlutHack Bluetooth Scanner <<<\n"))

# ===== СКАН (РАБОЧИЙ) =====
def scan_devices():
    print(Fore.CYAN + "[*] Запуск сканирования... (10 сек)")

    process = subprocess.Popen(
        ["bluetoothctl"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    process.stdin.write("power on\n")
    process.stdin.write("scan on\n")
    process.stdin.flush()

    start_time = time.time()
    devices = set()

    while time.time() - start_time < 10:
        line = process.stdout.readline()
        if "Device" in line:
            parts = line.strip().split(" ", 2)
            if len(parts) >= 3:
                mac = parts[1]
                name = parts[2]
                devices.add((mac, name))
                print(Fore.BLUE + f"[+] {mac} - {name}")

    process.stdin.write("scan off\n")
    process.stdin.flush()
    process.terminate()

    if not devices:
        print(Fore.RED + "[-] Ничего не найдено")

# ===== ПОДКЛЮЧЕНИЕ =====
def connect_device():
    mac = input(Fore.WHITE + "MAC устройства: ")

    if not mac:
        return

    print(Fore.CYAN + f"[*] Подключение к {mac}...")

    os.system(f"bluetoothctl pair {mac}")
    os.system(f"bluetoothctl trust {mac}")
    os.system(f"bluetoothctl connect {mac}")

    input("\nEnter...")

# ===== МЕНЮ =====
def main():
    while True:
        draw_banner()

        print(gradient_text("1. Сканировать Bluetooth"))
        print(gradient_text("2. Подключиться"))
        print(Fore.RED + "99. Выход\n")

        choice = input("BlutHack > ")

        if choice == "1":
            scan_devices()
            input("\nEnter...")
        elif choice == "2":
            connect_device()
        elif choice == "99":
            break
        else:
            print("Ошибка")
            time.sleep(1)

if __name__ == "__main__":
    main()
