import os
import subprocess
import time
import json
import webbrowser
from colorama import init, Fore

init(autoreset=True)

DATA_FILE = "devices.json"

# ===== ГРАДИЕНТ =====

def gradient_text(text):
colors = [Fore.CYAN, Fore.BLUE]
return "".join(colors[i % len(colors)] + c for i, c in enumerate(text))

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
print(gradient_text("        >>> BlutHack (Bluetooth + OSINT) <<<\n"))

# ===== BLUETOOTH =====

def run_btctl(cmds):
p = subprocess.Popen(
["bluetoothctl"],
stdin=subprocess.PIPE,
stdout=subprocess.PIPE,
text=True
)
for c in cmds:
p.stdin.write(c + "\n")
p.stdin.flush()
return p

def scan_devices(duration=10):
print("[*] Сканирование...")
p = run_btctl(["power on", "scan on"])


devices = {}
start = time.time()

while time.time() - start < duration:
    line = p.stdout.readline()
    if "Device" in line:
        parts = line.strip().split(" ", 2)
        if len(parts) >= 3:
            mac = parts[1]
            name = parts[2]
            if mac not in devices:
                devices[mac] = name
                print(f"[+] {mac} - {name}")

p.stdin.write("scan off\n")
p.stdin.flush()
p.terminate()

if not devices:
    print("[-] Ничего не найдено")

return devices


def connect_device(mac):
print(f"[*] Подключение к {mac}")
os.system(f"bluetoothctl pair {mac}")
os.system(f"bluetoothctl trust {mac}")
os.system(f"bluetoothctl connect {mac}")
input("Enter...")

# ===== SAVE / LOAD =====

def save_devices(devs):
with open(DATA_FILE, "w") as f:
json.dump(devs, f)

def load_devices():
if not os.path.exists(DATA_FILE):
print("Нет сохранённых")
return
with open(DATA_FILE) as f:
data = json.load(f)
for m, n in data.items():
print(m, "-", n)

# ===== GOOGLE DORK =====

def build_dorks():
print("\n=== Dork Generator ===")


query = input("Что ищешь: ").strip()
site = input("Сайт: ").strip()
filetype = input("Тип файла: ").strip()
intext = input("Текст внутри: ").strip()
inurl = input("В URL: ").strip()
intitle = input("В заголовке: ").strip()

base = ""

if query:
    base += f'"{query}" '
if site:
    base += f"site:{site} "
if filetype:
    base += f"filetype:{filetype} "
if intext:
    base += f"intext:{intext} "
if inurl:
    base += f"inurl:{inurl} "
if intitle:
    base += f'intitle:"{intitle}" '

base = base.strip()

dorks = []

if base:
    dorks.append(base)
    dorks.append(base + " password")
    dorks.append(base + " admin")
    dorks.append(base + " login")
    dorks.append(base + ' "index of"')

if filetype:
    dorks.append(f'filetype:{filetype} "password"')

if site:
    dorks.append(f"site:{site} inurl:admin")

return dorks
```

def osint_menu():
dorks = build_dorks()

```
for i, d in enumerate(dorks, 1):
    print(f"{i}. {d}")

choice = input("Открыть? (y/n): ")

if choice == "y":
    for d in dorks:
        webbrowser.open("https://google.com/search?q=" + d.replace(" ", "+"))


# ===== MAIN =====

def main():
last = {}


while True:
    draw_banner()
    print("1. Скан Bluetooth")
    print("2. Подключиться")
    print("3. Сохранить")
    print("4. Загрузить")
    print("5. Google Dork")
    print("99. Выход")

    c = input("> ")

    if c == "1":
        last = scan_devices()
        input()
    elif c == "2":
        mac = input("MAC: ")
        connect_device(mac)
    elif c == "3":
        save_devices(last)
    elif c == "4":
        load_devices()
        input()
    elif c == "5":
        osint_menu()
        input()
    elif c == "99":
        break


if **name** == "**main**":
main()
