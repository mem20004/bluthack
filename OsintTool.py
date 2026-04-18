import os
import requests
import socket
import webbrowser
from colorama import init, Fore

init(autoreset=True)

def clear():
    os.system("clear")

def gradient(text):
    colors = [Fore.CYAN, Fore.BLUE, Fore.LIGHTBLUE_EX]
    return "".join(colors[i % len(colors)] + c for i, c in enumerate(text))

def banner():
    print(gradient("""
 ██████   ██████  ██ ███    ██ ████████ ████████  ██████   ██████  ██      
██    ██ ██       ██ ████   ██    ██       ██    ██    ██ ██    ██ ██      
██    ██ ███████  ██ ██ ██  ██    ██       ██    ██    ██ ██    ██ ██      
██    ██      ██  ██ ██  ██ ██    ██       ██    ██    ██ ██    ██ ██      
 ██████   ██████  ██ ██   ████    ██       ██     ██████   ██████  ███████ 
"""))
    print(gradient("          >>> OsintTool PRO MAX <<<\n"))

def menu():
    print(Fore.GREEN + "1. Smart Search".ljust(30) + "2. Username Check")
    print(Fore.GREEN + "3. Domain Info".ljust(30) + "4. IP Lookup")
    print(Fore.GREEN + "5. Quick Recon".ljust(30) + "6. Port Scan")
    print(Fore.GREEN + "7. HTTP Headers".ljust(30) + "8. DNS Lookup")
    print(Fore.GREEN + "9. Subdomain Finder".ljust(30) + "10. Email Finder")
    print(Fore.GREEN + "11. GeoIP".ljust(30) + "12. Open Links")
    print(Fore.RED + "99. Exit\n")

def smart_search():
    q = input("Query: ")
    webbrowser.open("https://www.google.com/search?q=" + q.replace(" ", "+"))

def username_check():
    u = input("Username: ")
    sites = [f"https://github.com/{u}", f"https://instagram.com/{u}", f"https://t.me/{u}"]
    for s in sites:
        try:
            r = requests.get(s)
            print("[+]" if r.status_code==200 else "[-]", s)
        except:
            print("[!]", s)

def domain_info():
    d = input("Domain: ")
    try:
        print("IP:", socket.gethostbyname(d))
    except:
        print("Error")
    os.system(f"whois {d}")

def ip_lookup():
    ip = input("IP: ")
    try:
        data = requests.get(f"http://ip-api.com/json/{ip}").json()
        for k,v in data.items():
            print(k,":",v)
    except:
        print("Error")

def quick_recon():
    t = input("Target: ")
    try:
        print("IP:", socket.gethostbyname(t))
    except:
        pass
    webbrowser.open(f"https://{t}")

def port_scan():
    host = input("Host: ")
    for p in range(20, 1025):
        s = socket.socket()
        s.settimeout(0.3)
        try:
            s.connect((host,p))
            print("Open:", p)
        except:
            pass
        s.close()

def headers():
    url = input("URL: ")
    try:
        r = requests.get(url)
        for k,v in r.headers.items():
            print(k,":",v)
    except:
        print("Error")

def dns_lookup():
    d = input("Domain: ")
    os.system(f"nslookup {d}")

def subdomain():
    d = input("Domain: ")
    subs = ["www","mail","ftp","test"]
    for s in subs:
        try:
            print(s+".",socket.gethostbyname(s+"."+d))
        except:
            pass

def email_finder():
    text = input("Text: ")
    import re
    emails = re.findall(r"[\w\.-]+@[\w\.-]+", text)
    for e in emails:
        print(e)

def geoip():
    ip = input("IP: ")
    try:
        print(requests.get(f"http://ip-api.com/json/{ip}").json())
    except:
        print("Error")

def open_links():
    q = input("Query: ")
    webbrowser.open("https://duckduckgo.com/?q=" + q.replace(" ", "+"))

def main():
    while True:
        clear()
        banner()
        menu()
        c = input("> ")

        if c == "1": smart_search()
        elif c == "2": username_check()
        elif c == "3": domain_info()
        elif c == "4": ip_lookup()
        elif c == "5": quick_recon()
        elif c == "6": port_scan()
        elif c == "7": headers()
        elif c == "8": dns_lookup()
        elif c == "9": subdomain()
        elif c == "10": email_finder()
        elif c == "11": geoip()
        elif c == "12": open_links()
        elif c == "99": break

        input("\nEnter...")

if __name__ == "__main__":
    main()
