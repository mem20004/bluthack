import os
import requests
import socket
import webbrowser

def clear():
os.system("clear")

def banner():
print("""
██████   ██████  ██ ███    ██ ████████ ████████  ██████   ██████  ██
██    ██ ██       ██ ████   ██    ██       ██    ██    ██ ██    ██ ██
██    ██ ███████  ██ ██ ██  ██    ██       ██    ██    ██ ██    ██ ██
██    ██      ██  ██ ██  ██ ██    ██       ██    ██    ██ ██    ██ ██
██████   ██████  ██ ██   ████    ██       ██     ██████   ██████  ███████

```
        >>> OsintTool PRO <<<
```

""")

# ===== SEARCH =====

def smart_search():
query = input("Что ищем: ")
site = input("Сайт (можно пусто): ")
filetype = input("Тип файла: ")

```
dork = ""

if query:
    dork += f'"{query}" '
if site:
    dork += f"site:{site} "
if filetype:
    dork += f"filetype:{filetype} "

print("\nDork:", dork)

webbrowser.open("https://www.google.com/search?q=" + dork.replace(" ", "+"))
```

# ===== USERNAME =====

def username_check():
username = input("Ник: ")

```
sites = [
    f"https://github.com/{username}",
    f"https://t.me/{username}",
    f"https://instagram.com/{username}",
    f"https://twitter.com/{username}",
    f"https://reddit.com/user/{username}"
]

print("\nРезультаты:\n")

for url in sites:
    try:
        r = requests.get(url)
        if r.status_code == 200:
            print("[+] Найден:", url)
        else:
            print("[-] Нет:", url)
    except:
        print("Ошибка:", url)
```

# ===== DOMAIN =====

def domain_info():
domain = input("Домен: ")

```
print("\nIP:")
try:
    ip = socket.gethostbyname(domain)
    print(ip)
except:
    print("Ошибка")

print("\nWhois:")
os.system(f"whois {domain}")
```

# ===== IP LOOKUP =====

def ip_lookup():
ip = input("IP: ")

```
try:
    data = requests.get(f"http://ip-api.com/json/{ip}").json()
    for k, v in data.items():
        print(k, ":", v)
except:
    print("Ошибка")
```

# ===== QUICK RECON =====

def quick_recon():
target = input("Цель (домен): ")

```
print("\n[+] IP:")
try:
    print(socket.gethostbyname(target))
except:
    pass

print("\n[+] Open in browser")
webbrowser.open(f"https://{target}")
```

# ===== MENU =====

def main():
while True:
clear()
banner()

```
    print("1. Smart Search")
    print("2. Username OSINT")
    print("3. Domain Info")
    print("4. IP Lookup")
    print("5. Quick Recon")
    print("99. Exit")

    choice = input("> ")

    if choice == "1":
        smart_search()
        input()
    elif choice == "2":
        username_check()
        input()
    elif choice == "3":
        domain_info()
        input()
    elif choice == "4":
        ip_lookup()
        input()
    elif choice == "5":
        quick_recon()
        input()
    elif choice == "99":
        break
```

if **name** == "**main**":
main()
