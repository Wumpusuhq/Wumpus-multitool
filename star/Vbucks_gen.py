import random
import string
import aiohttp
import asyncio
from colorama import Fore
from pystyle import Colors, Colorate

from pystyle import Center, Colorate, Colors, Anime
from colorama import Fore
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
                          
                     0 = infinity

                          """))

CODES_TO_GENERATE = int(input(Colorate.Horizontal(Colors.blue_to_cyan, "Code to generate ➜  ")))
VALIDATION_URL = "https://www.fortnite.com/vbuckscard?sessionvalidated=true"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def generate_code():
    return "-".join(
        "".join(random.choices(string.ascii_uppercase + string.digits, k=4)) for _ in range(4)
    )

async def validate_code(session, code, results, index):
    try:
        async with session.post(VALIDATION_URL, headers=HEADERS, data={"code": code}) as response:
            if response.status == 200:
                result = (Colorate.Horizontal(Colors.blue_to_green, f"Code Valid {index + 1}: {code}, Status: Valid, HTTP Status Code: {response.status}"))
                results.append(result)
                print(f"\r{result}", end="", flush=True)
                return True 
            else:
                result = (Colorate.Horizontal(Colors.blue_to_red, f"Code invalid: {code}"))
                print(f"\r{result}", end="", flush=True)  
                return False
    except Exception as e:
        result = f"Code {index + 1}: {code}, Status: Error, {str(e)}"
        print(f"\r{result}", end="", flush=True)  
        return False

async def write_results_to_file(results):
    with open("Valid Riskow.txt", "w") as file:
        for result in results:
            file.write(result + "\n")

async def main():
    results = []
    conn = aiohttp.TCPConnector(limit_per_host=10)  
    async with aiohttp.ClientSession(connector=conn) as session:
        tasks = []
        index = 0
        if CODES_TO_GENERATE == 0:
            while True:
                code = generate_code()
                valid = await validate_code(session, code, results, index)
                if valid:
                    break
                index += 1
        else:
            for i in range(CODES_TO_GENERATE):
                code = generate_code()
                task = asyncio.create_task(validate_code(session, code, results, i))
                tasks.append(task)

            await asyncio.gather(*tasks)

    if results:
        await write_results_to_file(results)

if __name__ == "__main__":
    asyncio.run(main())
    input(Colorate.Horizontal(Colors.red_to_yellow, "\nPRESS ENTER TO EXIT..."))
