import os
import sys
import subprocess
import json
import time

def setup_termux():
    """Автоматическая настройка окружения Termux"""
    print("[*] Проверка системных зависимостей...")
    
    # 1. Проверка и установка пакета termux-api в консоли
    check_api = subprocess.run(['command', '-v', 'termux-bluetooth-scan'], shell=True, capture_output=True)
    if check_api.returncode != 0:
        print("[!] Пакет termux-api не найден. Устанавливаю...")
        os.system('pkg update -y && pkg install termux-api -y')
    
    # 2. Проверка библиотек Python
    try:
        import colorama
    except ImportError:
        print("[!] Библиотека colorama не найдена. Устанавливаю...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "colorama"])

setup_termux()

from colorama import init, Fore
init(autoreset=True)

def draw_interface():
    os.system('clear')
    banner = f"""
{Fore.RED}###############################################################
{Fore.RED}#                                                             #
{Fore.CYAN}  @@@@@@@   @@@       @@@  @@@  @@@@@@@@  @@@  @@@   @@@@@@  
  @@@@@@@@  @@@       @@@  @@@  @@@@@@@@  @@@  @@@  @@@@@@@@ 
  @@!  @@@  @@!       @@!  @@@     @@!    @@!  @@@  @@!  @@@ 
  !@   @!@  !@!       !@!  @!@     @!!    !@!  @!@  !@!  @!@ 
  @!@!@!@   @!!       @!@  !@!     @!!    @!@!@!@!  @!@!@!@! 
  !!!@!!!!  !!!       !@!  !!!     !!!    !!!@!!!!  !!!@!!!! 
  !!:  !!!  !!:       !!:  !!!     !!:    !!:  !!!  !!:  !!! 
  :!:  !:!   :!:      :!:  !:!     :!:    :!:  !:!  :!:  !:! 
   :: ::::   :: ::::  ::::: ::      ::    ::   :::  ::   ::: 
  :: : ::   : :: : :   : :  :       :      :   : :   :   : :  
{Fore.RED}#                                                             #
{Fore.GREEN}#            [ AUTO-INSTALL & SCAN MODE: TERMUX ]             #
{Fore.RED}###############################################################
    """
    print(banner)
    print(f"{Fore.GREEN} 1. Сканировать эфир (Bluetooth)")
    print(f"{Fore.RED} 99. Выход")
    print(f"{Fore.MAGENTA}" + "-" * 63)

def scan_android():
    print(f"{Fore.YELLOW}[*] Запуск termux-bluetooth-scan...")
    print(f"{Fore.YELLOW}[*] Убедись, что GPS включен, иначе Android ничего не найдет!")
    
    try:
        # Запуск сканирования
        scan_proc = subprocess.run(['termux-bluetooth-scan'], capture_output=True, text=True, timeout=30)
        
        if scan_proc.returncode != 0:
            print(f"{Fore.RED}[!] Ошибка API! Убедись, что ПРИЛОЖЕНИЕ Termux:API установлено из стора.")
            input("\nНажми Enter...")
            return

        devices = json.loads(scan_proc.stdout)

        if not devices:
            print(f"{Fore.RED}[-] Устройства не найдены. Попробуй поднести их ближе.")
        else:
            print(f"\n{Fore.CYAN}{'Name':<25} | {'MAC-Address':<20} | {'RSSI'}")
            print("-" * 63)
            for dev in devices:
                name = dev.get('name', 'N/A')
                addr = dev.get('address', '??:??:??')
                rssi = dev.get('rssi', '0')
                print(f"{Fore.GREEN}{name:<25} {Fore.WHITE}| {addr:<20} | {rssi} dBm")
                
    except subprocess.TimeoutExpired:
        print(f"{Fore.RED}[!] Превышено время ожидания сканирования.")
    except Exception as e:
        print(f"{Fore.RED}[!] Сбой: {e}")
    
    input(f"\n{Fore.YELLOW}Готово. Жми Enter...")

def main():
    while True:
        draw_interface()
        choice = input(f"{Fore.WHITE}BlutHack > ")
        if choice == "1":
            scan_android()
        elif choice == "99":
            print(f"{Fore.RED}Выход...")
            sys.exit()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
