# python
import os
import subprocess
import time
from colorama import init, Fore, Style

init(autoreset=True)

# ===== БАННЕР =====
def draw_banner():
    banner = f"""
{Fore.RED}██████╗ ██╗     ██╗   ██╗████████╗██╗  ██╗ █████╗  ██████╗██╗  ██╗
{Fore.RED}██╔══██╗██║     ██║   ██║╚══██╔══╝██║  ██║██╔══██╗██╔════╝██║ ██╔╝
{Fore.CYAN}██████╔╝██║     ██║   ██║   ██║   ███████║███████║██║     █████╔╝ 
{Fore.CYAN}██╔══██╗██║     ██║   ██║   ██║   ██╔══██║██╔══██║██║     ██╔═██╗ 
{Fore.GREEN}██████╔╝███████╗╚██████╔╝   ██║   ██║  ██║██║  ██║╚██████╗██║  ██╗
{Fore.GREEN}╚═════╝ ╚══════╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝

{Fore.MAGENTA}           >>>   BlutHack Bluetooth Tool   <<<
{Style.RESET_ALL}
"""
    print(banner)

# ===== КОМАНДЫ =====
def run_cmd(cmd):
    return subprocess.getoutput(cmd)

# ===== СКАН =====
def scan_devices():
    print(Fore.YELLOW + "[*] Включаем Bluetooth...")
    run_cmd("bluetoothctl power on")
    run_cmd("bluetoothctl agent on")
    run_cmd("bluetoothctl default-agent")

    print(Fore.YELLOW + "[*] Сканирование (10 сек)...")
    run_cmd("bluetoothctl scan on")
    time.sleep(10)
    run_cmd("bluetoothctl scan off")

    devices = run_cmd("bluetoothctl devices")

    print(Fore.CYAN + "\nНайденные устройства:")
    print("-" * 50)
    print(Fore.GREEN + devices)
    print("-" * 50)

# ===== ПОДКЛЮЧЕНИЕ =====
def connect_device():
    mac = input(Fore.WHITE + "Введи MAC устройства: ")

    if not mac:
        return

    print(Fore.YELLOW + f"[*] Подключение к {mac}...")
    run_cmd(f"bluetoothctl pair {mac}")
    run_cmd(f"bluetoothctl trust {mac}")
    result = run_cmd(f"bluetoothctl connect {mac}")

    print(Fore.GREEN + result)
    input("\nНажми Enter...")

# ===== МЕНЮ =====
def main():
    while True:
        os.system("clear")
        draw_banner()

        print(Fore.GREEN + "1. Сканировать Bluetooth")
        print(Fore.CYAN + "2. Подключиться к устройству")
        print(Fore.RED + "99. Выход")

        choice = input(Fore.WHITE + "\nBlutHack > ")

        if choice == "1":
            scan_devices()
            input("\nEnter...")
        elif choice == "2":
            connect_device()
        elif choice == "99":
            print(Fore.RED + "Выход...")
            break
        else:
            print("Неверный выбор")
            time.sleep(1)

# ===== ЗАПУСК =====
if __name__ == "__main__":
    main()

