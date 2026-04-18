import os
import subprocess
import time
import json
import webbrowser
from urllib.parse import quote_plus
from colorama import init, Fore

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


def run_command(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)


def bluetooth_available():
    result = run_command("bluetoothctl list")
    return result.returncode == 0


def scan_devices(duration=12):
    print(Fore.CYAN + f"[*] Сканирование Bluetooth {duration} сек...")
    print(Fore.CYAN + "[*] Используется тот же способ, что и в терминале: timeout + bluetoothctl scan on")
    print()

    cmd = f"timeout {duration}s bluetoothctl scan on"
    result = run_command(cmd)

    devices = {}
    output = (result.stdout or "") + "\n" + (result.stderr or "")

    for raw_line in output.splitlines():
        line = raw_line.strip()
        if "Device " in line:
            try:
                part = line.split("Device ", 1)[1]
                mac, rest = part.split(" ", 1)
                name = rest.strip()
                if mac not in devices:
                    devices[mac] = name
            except ValueError:
                continue

    if devices:
        print(Fore.GREEN + "[+] Найденные устройства:")
        print("-" * 60)
        for mac, name in devices.items():
            print(Fore.BLUE + f"{mac} - {name}")
        print("-" * 60)
    else:
        print(Fore.RED + "[-] Ничего не найдено.")
        print(Fore.YELLOW + "[!] Если в терминале scan on видит устройства, но тут пусто — покажи вывод:")
        print(Fore.YELLOW + f"    {cmd}")

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


def unique_list(items):
    out = []
    seen = set()
    for item in items:
        if item and item not in seen:
            out.append(item)
            seen.add(item)
    return out


def build_queries():
    print(Fore.CYAN + "\n=== Search Builder ===")
    print("Поля можно оставлять пустыми.")
    print()

    query = ask_optional("Что ищешь (можно пусто): ")
    site = ask_optional("На каком сайте (можно пусто): ")
    intext = ask_optional("Текст на странице / intext (можно пусто): ")
    inurl = ask_optional("Слово в URL / inurl (можно пусто): ")
    intitle = ask_optional("Слово в title / intitle (можно пусто): ")
    filetype = ask_optional("Тип файла (pdf, docx, xlsx...) (можно пусто): ")
    exact = ask_optional("Точная фраза в кавычках (можно пусто): ")
    exclude = ask_optional("Что исключить через -term (можно пусто): ")

    base_tokens = []

    if query:
        base_tokens.append(query)
    if exact:
        base_tokens.append(f'"{exact}"')
    if site:
        base_tokens.append(f"site:{site}")
    if intext:
        base_tokens.append(f'intext:"{intext}"')
    if inurl:
        base_tokens.append(f'inurl:"{inurl}"')
    if intitle:
        base_tokens.append(f'intitle:"{intitle}"')
    if filetype:
        base_tokens.append(f"filetype:{filetype}")
    if exclude:
        base_tokens.append(f"-{exclude}")

    base = " ".join(base_tokens).strip()
    queries = []

    if base:
        queries.append(base)

    if query and site:
        queries.append(f'site:{site} "{query}"')

    if query and intext:
        if site:
            queries.append(f'site:{site} "{query}" intext:"{intext}"')
        else:
            queries.append(f'"{query}" intext:"{intext}"')

    if query and inurl:
        if site:
            queries.append(f'site:{site} "{query}" inurl:"{inurl}"')
        else:
            queries.append(f'"{query}" inurl:"{inurl}"')

    if query and intitle:
        if site:
            queries.append(f'site:{site} intitle:"{intitle}" "{query}"')
        else:
            queries.append(f'intitle:"{intitle}" "{query}"')

    if query and filetype:
        if site:
            queries.append(f'site:{site} filetype:{filetype} "{query}"')
        else:
            queries.append(f'filetype:{filetype} "{query}"')

    if site and intext and filetype:
        queries.append(f'site:{site} filetype:{filetype} intext:"{intext}"')

    if site and inurl and filetype:
        queries.append(f'site:{site} filetype:{filetype} inurl:"{inurl}"')

    if site and intitle:
        queries.append(f'site:{site} intitle:"{intitle}"')

    if site and inurl:
        queries.append(f'site:{site} inurl:"{inurl}"')

    if site and intext:
        queries.append(f'site:{site} intext:"{intext}"')

    if filetype and intext:
        queries.append(f'filetype:{filetype} intext:"{intext}"')

    if filetype and intitle:
        queries.append(f'filetype:{filetype} intitle:"{intitle}"')

    if exact and site:
        queries.append(f'site:{site} "{exact}"')

    if exact and filetype:
        queries.append(f'filetype:{filetype} "{exact}"')

    return unique_list(queries)


def open_queries(engine, queries):
    if engine == "google":
        base = "https://www.google.com/search?q="
    else:
        base = "https://www.bing.com/search?q="

    for q in queries:
        webbrowser.open_new_tab(base + quote_plus(q))


def search_builder_menu():
    queries = build_queries()

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


def browsers_menu():
    print(Fore.CYAN + "\nЛёгкие браузеры для старого antiX / Debian:\n")
    print(Fore.GREEN + "1. links2      - очень лёгкий, есть графический режим")
    print(Fore.GREEN + "2. w3m         - текстовый, очень быстрый")
    print(Fore.GREEN + "3. lynx        - текстовый, минимальный")
    print(Fore.GREEN + "4. dillo       - сверхлёгкий GUI-браузер")
    print(Fore.GREEN + "5. netsurf-gtk - лёгкий GUI-браузер")
    print()
    print(Fore.CYAN + "Команды установки:")
    print("sudo apt update")
    print("sudo apt install links2 w3m lynx dillo netsurf-gtk")
    print()
    print(Fore.CYAN + "Запуск:")
    print("links2 -g")
    print("w3m https://example.org")
    print("lynx https://example.org")
    print("dillo")
    print("netsurf-gtk")
    input("\nНажми Enter...")


def print_bt_help():
    print(Fore.CYAN + "\nПроверка Bluetooth:")
    print("1) lsusb")
    print("2) rfkill list")
    print("3) bluetoothctl list")
    print("4) hciconfig")
    print("5) Прямой тест скана:")
    print("   timeout 12s bluetoothctl scan on")
    print("6) Запуск скрипта:")
    print("   sudo python3 OsintTool.py")
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
        print(gradient_text("6. Лёгкие браузеры"))
        print(gradient_text("7. Проверка Bluetooth / Help"))
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
            search_builder_menu()
        elif choice == "6":
            browsers_menu()
        elif choice == "7":
            print_bt_help()
        elif choice == "99":
            break
        else:
            print(Fore.RED + "Неверный выбор")
            time.sleep(1)


if __name__ == "__main__":
    main()
