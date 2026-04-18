import os
import subprocess
import time
import json
import webbrowser
from urllib.parse import quote_plus
from colorama import init, Fore, Style

init(autoreset=True)

DATA_FILE = "devices.json"


def gradient_text(text):
    colors = [Fore.CYAN, Fore.BLUE]
    return "".join(colors[i % len(colors)] + ch for i, ch in enumerate(text))


def draw_banner():
    os.system("clear")
    banner = """
 ██████   ██████  ██ ███    ██ ████████ ████████  ██████   ██████  ██      
██    ██ ██       ██ ████   ██    ██       ██    ██    ██ ██    ██ ██      
██    ██ ███████  ██ ██ ██  ██    ██       ██    ██    ██ ██    ██ ██      
██    ██      ██  ██ ██  ██ ██    ██       ██    ██    ██ ██    ██ ██      
 ██████   ██████  ██ ██   ████    ██       ██     ██████   ██████  ███████ 
"""
    print(gradient_text(banner))
    print(gradient_text("              >>> OsintTool (Bluetooth + Search Builder) <<<"))
    print()


def run_btctl(commands):
    process = subprocess.Popen(
        ["bluetoothctl"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    for cmd in commands:
        process.stdin.write(cmd + "\n")
    process.stdin.flush()
    return process


def bluetooth_available():
    try:
        result = subprocess.run(
            ["bluetoothctl", "list"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except Exception:
        return False


def scan_devices(duration=12):
    print(Fore.CYAN + f"[*] Сканирование Bluetooth {duration} сек...")
    print(Fore.CYAN + "[*] Если ничего не найдёт, проверь адаптер, rfkill и запуск с sudo.\n")

    process = run_btctl(["power on", "agent on", "default-agent", "scan on"])
    devices = {}
    start = time.time()

    try:
        while time.time() - start < duration:
            line = process.stdout.readline()
            if not line:
                continue

            line = line.strip()

            if "Device " in line:
                parts = line.split("Device ", 1)[1]
                pieces = parts.split(" ", 1)
                if len(pieces) == 2:
                    mac = pieces[0].strip()
                    name = pieces[1].strip()
                    if mac not in devices:
                        devices[mac] = name
                        print(Fore.BLUE + f"[+] {mac} - {name}")
    finally:
        try:
            process.stdin.write("scan off\n")
            process.stdin.flush()
        except Exception:
            pass
        process.terminate()

    if not devices:
        print(Fore.RED + "[-] Ничего не найдено.")
    return devices


def connect_device(mac):
    if not mac:
        print(Fore.RED + "[!] MAC пустой")
        return

    print(Fore.CYAN + f"[*] Подключение к {mac}...")
    os.system(f"bluetoothctl pair {mac}")
    os.system(f"bluetoothctl trust {mac}")
    os.system(f"bluetoothctl connect {mac}")
    input("\nНажми Enter...")


def save_devices(devices):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(devices, f, ensure_ascii=False, indent=2)
        print(Fore.GREEN + f"[+] Сохранено в {DATA_FILE}")
    except Exception as e:
        print(Fore.RED + f"[!] Ошибка сохранения: {e}")


def load_devices():
    if not os.path.exists(DATA_FILE):
        print(Fore.YELLOW + "[!] Нет сохранённых устройств")
        return {}

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(Fore.GREEN + f"[+] Загружено {len(data)} устройств:")
        for mac, name in data.items():
            print(Fore.CYAN + f"    {mac} - {name}")
        return data
    except Exception as e:
        print(Fore.RED + f"[!] Ошибка чтения: {e}")
        return {}


def ask_optional(prompt):
    return input(prompt).strip()


def build_dorks():
    print(Fore.CYAN + "\n=== Search Builder ===")
    query = ask_optional("Что ищешь (можно пусто): ")
    site = ask_optional("На каком сайте (можно пусто): ")
    filetype = ask_optional("Тип файла (pdf, docx, xlsx...) (можно пусто): ")
    intext = ask_optional("Слово в тексте (можно пусто): ")
    inurl = ask_optional("Слово в URL (можно пусто): ")
    intitle = ask_optional("Слово в заголовке (можно пусто): ")
    exclude = ask_optional("Что исключить через минус (можно пусто): ")
    exact = ask_optional("Точная фраза в кавычках (можно пусто): ")

    tokens = []

    if query:
        tokens.append(query)
    if exact:
        tokens.append(f'"{exact}"')
    if site:
        tokens.append(f"site:{site}")
    if filetype:
        tokens.append(f"filetype:{filetype}")
    if intext:
        tokens.append(f"intext:{intext}")
    if inurl:
        tokens.append(f"inurl:{inurl}")
    if intitle:
        tokens.append(f'intitle:"{intitle}"')
    if exclude:
        tokens.append(f"-{exclude}")

    base = " ".join(tokens).strip()
    dorks = []

    if base:
        dorks.append(base)

        if site and query:
            dorks.append(f'site:{site} "{query}"')
        if filetype and query:
            dorks.append(f'"{query}" filetype:{filetype}')
        if inurl and site:
            dorks.append(f"site:{site} inurl:{inurl}")
        if intext and site:
            dorks.append(f"site:{site} intext:{intext}")
        if intitle and query:
            dorks.append(f'intitle:"{intitle}" "{query}"')
        if query and site and filetype:
            dorks.append(f'site:{site} filetype:{filetype} "{query}"')

    unique = []
    seen = set()
    for item in dorks:
        if item and item not in seen:
            unique.append(item)
            seen.add(item)

    return unique


def open_queries(engine, queries):
    if engine == "google":
        base = "https://www.google.com/search?q="
    else:
        base = "https://www.bing.com/search?q="

    for q in queries:
        webbrowser.open_new_tab(base + quote_plus(q))


def osint_menu():
    queries = build_dorks()

    if not queries:
        print(Fore.YELLOW + "\n[!] Пустой запрос. Нечего генерировать.")
        input("\nНажми Enter...")
        return

    print(Fore.GREEN + "\nСгенерированные запросы:\n")
    for i, q in enumerate(queries, 1):
        print(Fore.CYAN + f"{i}. {q}")

    print("\n1. Открыть в Google")
    print("2. Открыть в Bing")
    print("0. Назад")

    choice = input("> ").strip()
    if choice == "1":
        open_queries("google", queries)
    elif choice == "2":
        open_queries("bing", queries)


def print_bt_help():
    print(Fore.CYAN + "\nПроверка Bluetooth:")
    print("1) lsusb")
    print("2) rfkill list")
    print("3) bluetoothctl list")
    print("4) hciconfig")
    print("5) Запускай скан лучше так: sudo python3 OsintTool.py")
    input("\nНажми Enter...")


def main():
    last_scan = {}

    while True:
        draw_banner()
        print(gradient_text("1. Сканировать Bluetooth"))
        print(gradient_text("2. Подключиться по MAC"))
        print(gradient_text("3. Сохранить последний скан"))
        print(gradient_text("4. Загрузить сохранённые устройства"))
        print(gradient_text("5. Search Builder"))
        print(gradient_text("6. Проверка Bluetooth / Help"))
        print(Fore.RED + "99. Выход\n")

        choice = input("OsintTool > ").strip()

        if choice == "1":
            if not bluetooth_available():
                print(Fore.RED + "[!] bluetoothctl не найден или адаптер не определяется.")
                input("\nНажми Enter...")
                continue
            last_scan = scan_devices(12)
            input("\nНажми Enter...")
        elif choice == "2":
            mac = input("MAC: ").strip()
            connect_device(mac)
        elif choice == "3":
            if last_scan:
                save_devices(last_scan)
            else:
                print(Fore.YELLOW + "[!] Сначала сделай скан.")
                time.sleep(1.5)
        elif choice == "4":
            load_devices()
            input("\nНажми Enter...")
        elif choice == "5":
            osint_menu()
        elif choice == "6":
            print_bt_help()
        elif choice == "99":
            break
        else:
            print(Fore.RED + "Неверный выбор")
            time.sleep(1)


if __name__ == "__main__":
    main()
