from pystyle import Center, Colorate, Colors, Anime
import colorama
import requests
from bs4 import BeautifulSoup
import re
import time
import os

os.system('cls')
print(Colorate.Horizontal(Colors.blue_to_cyan,"""
▄▄▄▄  ▄▄▄  ▄▄▄▄                                 
▀███  ███  ███▀                                 
 ███  ███  ███ ██ ██ ███▄███▄ ████▄ ██ ██ ▄█▀▀▀ 
 ███▄▄███▄▄███ ██ ██ ██ ██ ██ ██ ██ ██ ██ ▀███▄ 
  ▀████▀████▀  ▀██▀█ ██ ██ ██ ████▀ ▀██▀█ ▄▄▄█▀ 
                              ██                
                              ▀▀                

                ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
                ┃ Author : Wumpus             ┃
                ┃ Discord: .gg/datas          ┃
                ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
"""))

colorama.init(autoreset=True)

sites = {
    "TikTok": "https://www.tiktok.com/@{}",
    "Instagram": "https://www.instagram.com/{}",
    "GitHub": "https://github.com/{}",
    "Pinterest": "https://www.pinterest.com/{}",
    "Snapchat": "https://www.snapchat.com/add/{}",
    "Telegram": "https://t.me/{}",
    "Steam": "https://steamcommunity.com/id/{}",
    "SoundCloud": "https://soundcloud.com/{}",
    "DeviantArt": "https://www.deviantart.com/{}",
    "Quora": "https://www.quora.com/profile/{}",
    "Patreon": "https://www.patreon.com/{}",
    "LinkedIn": "https://www.linkedin.com/in/{}",
    "Discord": "https://discord.com/users/{}",
    "Twitch": "https://www.twitch.tv/{}",
    "StackOverflow": "https://stackoverflow.com/users/{}",
    "Fiverr": "https://www.fiverr.com/{}",
    "Twitter": "https://twitter.com/{}",
    "Facebook": "https://www.facebook.com/{}",
    "YouTube": "https://www.youtube.com/{}",
}

def check_username(username):
    session = requests.Session()
    found = []

    print(colorama.Fore.YELLOW + "Scanning...")

    for site, url_template in sites.items():
        url = url_template.format(username)
        try:
            response = session.get(url, timeout=3)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                page_text = soup.get_text().lower()
                found.append(f"{site}: {url}")
                print(colorama.Fore.GREEN + f"Found: {site} -> {url}")
            else:
                print(colorama.Fore.RED + f"Not Found: {site}")

        except Exception:
            print(colorama.Fore.RED + f"Error checking {site}")

    print("\n" + colorama.Fore.CYAN + f"Total Found: {len(found)}")
    for entry in found:
        print(colorama.Fore.GREEN + entry)

if __name__ == "__main__":
    username = input(colorama.Fore.BLUE + "Enter the username to track: ").strip()
    check_username(username)
