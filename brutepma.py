import requests
from colorama import Fore, Style, init
import os
import pyfiglet
from concurrent.futures import ThreadPoolExecutor, as_completed

init(autoreset=True)

def clear_screen():

    os.system('cls' if os.name == 'nt' else 'clear')

def display_banner():
    # Authors jgn di ganti pler
    banner = pyfiglet.Figlet(font='banner3-D').renderText('Reyree')
    print(banner)

def check_folder(base_url, folder):
    url = f"{base_url}/{folder}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    try:
        response = requests.get(url, headers=headers, allow_redirects=True)
        if response.status_code == 200:
            print(f"{Fore.GREEN}{folder} - Valid")
            return url
        elif response.status_code == 403:
            print(f"{Fore.YELLOW}{folder} - Forbidden (403)")
        elif response.status_code == 404:
            print(f"{Fore.RED}{folder} - Tidak Valid (404)")
        else:
            print(f"{Fore.RED}{folder} - Error: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}{folder} - Error: {e}")
    return None

def main():
    clear_screen()
    display_banner()
    
    base_url = input("Masukkan URL website (contoh: http://example.com): ").strip()
    if not base_url.endswith('/'):
        base_url += '/'
    
    file_name = input("Masukkan nama file. Contoh : list.txt: ").strip()
    
    try:
        with open(file_name, "r") as file:
            folders = file.read().splitlines()

        valid_folders = []

        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_folder = {executor.submit(check_folder, base_url, folder): folder for folder in folders}
            for future in as_completed(future_to_folder):
                result = future.result()
                if result:
                    valid_folders.append(result)
        
        if valid_folders:
            print(f"\nURL Valid:")
            for valid_url in valid_folders:
                print(valid_url)
        else:
            print("\nGak ada yg valid.")
    except FileNotFoundError:
        print(f"{Fore.RED}File {file_name} tidak ditemukan.")

if __name__ == "__main__":
    main()
