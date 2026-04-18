
import os
import subprocess
import time
import json
import webbrowser
from colorama import init, Fore, Style

init(autoreset=True)

DATA_FILE = "devices.json"

# ===== ГРАДИЕНТ (океан) =====
def gradient_text(text):
    palette = [Fore.CYAN, Fore.BLUE]  # можно расширить списком
    out = []
    for i, ch in enumerate(text):
        out.append(palette[i % len(palette)] + ch)
    return "".join(out)

# ===== БАННЕР =====
def draw_banner():
    os.system("clear")
    banner = r"""
██████╗ ██╗     ██╗   ██╗████████╗██╗  ██╗ █████╗  ██████╗██╗  ██╗
██╔══██╗██║     ██║   ██║╚══██╔══╝██║  ██║██╔══██╗██╔════╝██║ ██╔╝
██████╔╝██║     ██║   ██║   ██║   ███████║███████║██║     █████╔╝ 
██╔══██╗██║     ██║   ██║   ██║   ██╔══██║██╔══██║██║     ██╔═██╗ 
██████╔╝███████╗╚██████╔╝   ██║   ██║  ██║██║  ██║╚██████╗██║  ██╗
╚═════╝ ╚══════╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
"""
    print(gradient_text(banner))
    print(gradient_text("        >>> BlutHack (Bluetooth + OSINT) <<<\n"))

# ===== УТИЛИТЫ =====
def run_btctl(cmds, timeout=0):
    """
    cmds: список строк-команд для bluetoothctl
    """
    p = subprocess.Popen(
        ["bluetoothctl"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    for c in cmds:
        p.stdin.write(c + "\n")
    p.stdin.flush()
    if timeout:
        time.sleep(timeout)
    return p

def rssi_bucket(rssi):
    # bluetoothctl не всегда даёт RSSI; если есть — грубо классифицируем
    try:
        r = int(rssi)
        if r >= -60:
            return "Near"
        elif r >= -80:
            return "Medium"
        else:
            return "Far"
    except:
        return "N/A"

# ===== СКАН (живой) =====
def scan_devices(duration=12):
    print(Fore.CYAN + f"[*] Сканирование {duration} сек... (запускай с sudo)")
    p = run_btctl(["power on", "agent on", "default-agent", "scan on"])

    start = time.time()
    seen = {}  # mac -> name
    try:
        while time.time() - start < duration:
            line = p.stdout.readline()
            if not line:
                continue
            line = line.strip()
            # строки вида: [NEW] Device AA:BB:CC:DD:EE:FF Name
            if "Device" in line:
                parts = line.split(" ", 2)
                if len(parts) >= 3:
                    mac = parts[1]
                    name = parts[2]
                    if mac not in seen:
                        seen[mac] = name
                        print(Fore.BLUE + f"[+] {mac} - {name}")
    finally:
        try:
            p.stdin.write("scan off\n")
            p.stdin.flush()
        except:
            pass
        p.terminate()

    if not seen:
        print(Fore.RED + "[-] Ничего не найдено")
    return seen

# ===== ПОДКЛЮЧЕНИЕ =====
def connect_device(mac):
    if not mac:
        return
    print(Fore.CYAN + f"[*] Pair/Trust/Connect -> {mac}")
    os.system(f"bluetoothctl pair {mac}")
    os.system(f"bluetoothctl trust {mac}")
    os.system(f"bluetoothctl connect {mac}")
    input("\nEnter...")

# ===== СОХРАНЕНИЕ =====
def save_devices(devs: dict):
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(devs, f, indent=2)
        print(Fore.GREEN + f"[+] Сохранено в {DATA_FILE}")
    except Exception as e:
        print(Fore.RED + f"[!] Ошибка сохранения: {e}")

def load_devices():
    if not os.path.exists(DATA_FILE):
        print(Fore.YELLOW + "[!] Файл не найден")
        return {}
    try:
        with open(DATA_FILE) as f:
            data = json.load(f)
        print(Fore.GREEN + f"[+] Загружено {len(data)} устройств")
        for m, n in data.items():
            print(Fore.CYAN + f"{m} - {n}")
        return data
    except Exception as e:
        print(Fore.RED + f"[!] Ошибка чтения: {e}")
        return {}

# ===== OSINT: генератор поисковых запросов (без обхода ограничений) =====
def build_queries(target):
    """
    Возвращает набор легитимных поисковых запросов для OSINT.
    Никаких попыток обхода приватности — только формирование запросов.
    """
    t = target.strip()
    queries = [
        f'"{t}"',
        f'"{t}" site:linkedin.com',
        f'"{t}" site:twitter.com OR site:x.com',
        f'"{t}" site:github.com',
        f'"{t}" filetype:pdf',
        f'"{t}" site:docs.google.com',  # просто фильтр по домену
        f'"{t}" site:drive.google.com',
    ]
    return queries

def osint_menu():
    target = input(Fore.WHITE + "Цель (имя/ник/домен): ").strip()
    if not target:
        return
    qs = build_queries(target)
    print(Fore.CYAN + "\nСформированные запросы:")
    for i, q in enumerate(qs, 1):
        print(f"{i}. {q}")

    print("\nОткрыть в браузере?")
    print("1. Открыть все (Google)")
    print("2. Открыть все (Bing)")
    print("0. Назад")
    ch = input("> ")

    if ch == "1":
        for q in qs:
            url = "https://www.google.com/search?q=" + q.replace(" ", "+")
            webbrowser.open_new_tab(url)
    elif ch == "2":
        for q in qs:
            url = "https://www.bing.com/search?q=" + q.replace(" ", "+")
            webbrowser.open_new_tab(url)

# ===== МЕНЮ =====
def main():
    last_scan = {}

    while True:
        draw_banner()
        print(gradient_text("1. Сканировать Bluetooth"))
        print(gradient_text("2. Подключиться (ввести MAC)"))
        print(gradient_text("3. Сохранить последний скан"))
        print(gradient_text("4. Загрузить сохранённые"))
        print(gradient_text("5. OSINT (генератор запросов)"))
        print(Fore.RED + "99. Выход\n")

        ch = input("BlutHack > ").strip()

        if ch == "1":
            last_scan = scan_devices(12)
            input("\nEnter...")
        elif ch == "2":
            mac = input("MAC: ").strip()
            connect_device(mac)
        elif ch == "3":
            if last_scan:
                save_devices(last_scan)
            else:
                print(Fore.YELLOW + "[!] Сначала сделай скан")
                time.sleep(1.2)
        elif ch == "4":
            load_devices()
            input("\nEnter...")
        elif ch == "5":
            osint_menu()
            input("\nEnter...")
        elif ch == "99":
            break
        else:
            print("Неверный выбор")
            time.sleep(1)

if __name__ == "__main__":
    main()

