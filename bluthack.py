import os
import subprocess
import time
import json
import webbrowser
from colorama import init, Fore

init(autoreset=True)

DATA_FILE = "devices.json"

def gradient_text(text):
    colors = [Fore.CYAN, Fore.BLUE]
    return "".join(colors[i % len(colors)] + c for i, c in enumerate(text))

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
    print(gradient_text(">>> BlutHack <<<\n"))

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
    print("[*] scanning...")
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

    return devices

def main():
    while True:
        draw_banner()
        print("1. scan")
        print("99. exit")

        c = input("> ")

        if c == "1":
            scan_devices()
            input()
        elif c == "99":
            break

if __name__ == "__main__":
    main()
