import requests
import json
import os
import pyfiglet
import sys
import time
from colorama import Fore, Style, init

init(autoreset=True)

def load_data():
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except:
        return {"api_key": "", "model": "deepseek/deepseek-chat-v3", "owner": "Diki", "lang": "Indonesian"}

def save_data(conf):
    with open('config.json', 'w') as f:
        json.dump(conf, f, indent=4)

def get_system_prompt():
    try:
        with open('prompt.txt', 'r') as s:
            return s.read()
    except:
        return "Kamu adalah OXYLUS-AI, asisten frontal."

def typewriter(teks):
    for char in teks:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.01)
    print()

def banner():
    os.system('clear')
    logo = pyfiglet.figlet_format("OXYLUS-AI", font="slant")
    print(Fore.CYAN + logo)
    print(Fore.WHITE + " Made With Chaos | Interface: CLI")
    print(Fore.CYAN + "==============================================\n")

def chat_engine(pesan, history, conf):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {conf['api_key']}",
        "Content-Type": "application/json"
    }
    messages = [{"role": "system", "content": get_system_prompt()}]
    messages.extend(history)
    messages.append({"role": "user", "content": pesan})
    
    try:
        response = requests.post(url, headers=headers, json={"model": conf['model'], "messages": messages})
        return response.json()['choices'][0]['message']['content']
    except:
        return "Gagal konek! Pastikan API Key lo bener."

def start_chat(conf):
    banner()
    print(Fore.YELLOW + "[ Chat Session Active ]")
    print(Fore.WHITE + "Ketik 'menu' untuk balik ke menu atau 'exit' untuk keluar\n")
    history = []
    while True:
        user_input = input(Fore.CYAN + f"[{conf['owner']}@oxylus]~# " + Style.RESET_ALL)
        if user_input.lower() == 'menu': break
        if user_input.lower() == 'exit': exit()
        
        print(Fore.YELLOW + "Oxylus is thinking...")
        result = chat_engine(user_input, history, conf)
        
        print(Fore.WHITE + "\n[OXYLUS-AI]: ", end="")
        typewriter(result)
        print()
        
        history.append({"role": "user", "content": user_input})
        history.append({"role": "assistant", "content": result})

def main_menu():
    while True:
        conf = load_data()
        banner()
        print(Fore.YELLOW + "[ Main Menu ]")
        print(f"1. Language: {Fore.GREEN}{conf.get('lang', 'Indonesian')}")
        print(f"2. Model: {Fore.GREEN}{conf['model']}")
        print(f"3. Set API Key")
        print("4. Start Chat")
        print("5. Exit")
        
        pilih = input(Fore.CYAN + "\n[>] Select (1-5): " + Style.RESET_ALL)
        
        if pilih == '1':
            conf['lang'] = input("Masukkan Bahasa: ")
            save_data(conf)
        elif pilih == '2':
            conf['model'] = input("Masukkan Nama Model: ")
            save_data(conf)
        elif pilih == '3':
            key = input("Paste API Key OpenRouter lo: ")
            conf['api_key'] = key
            save_data(conf)
        elif pilih == '4':
            if not conf['api_key'] or "sk-or" not in conf['api_key']:
                print(Fore.RED + "\nAPI Key belom lo pasang atau salah!")
                time.sleep(2)
                continue
            start_chat(conf)
        elif pilih == '5':
            print(Fore.RED + "Cabut...")
            break
        else:
            print("Pilihan kagak ada!")
            time.sleep(1)

if __name__ == "__main__":
    main_menu()
        
