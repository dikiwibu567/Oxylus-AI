import requests
import json
import os
import pyfiglet
from colorama import Fore, Style, init

init(autoreset=True)

def load_data():
    try:
        with open('config.json', 'r') as f:
            conf = json.load(f)
        with open('prompt.txt', 'r') as s:
            sys_prompt = s.read()
        return conf, sys_prompt
    except FileNotFoundError:
        print(Fore.RED + "Error: File config.json atau prompt.txt tidak ditemukan!")
        exit()

def banner(owner):
    os.system('clear')
    logo = pyfiglet.figlet_format("OXYLUS-AI", font="slant")
    print(Fore.CYAN + logo)
    print(f"{Fore.WHITE}Created by: {Fore.YELLOW}{owner} {Fore.WHITE}| Status: {Fore.GREEN}Online")
    print(Fore.CYAN + "==============================================\n")

def chat_engine(pesan, history, api_key, model, system):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    messages = [{"role": "system", "content": system}]
    messages.extend(history)
    messages.append({"role": "user", "content": pesan})
    data = {"model": model, "messages": messages}
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        return response.json()['choices'][0]['message']['content']
    except:
        return "Gagal konek! Cek API Key lo."

def main():
    conf, system = load_data()
    banner(conf['owner'])
    history = []
    while True:
        user_input = input(Fore.CYAN + f"[{conf['owner']}@oxylus]~# " + Style.RESET_ALL)
        if user_input.lower() in ['exit', 'quit']: break
        print(Fore.YELLOW + "Oxylus is thinking...")
        result = chat_engine(user_input, history, conf['api_key'], conf['model'], system)
        print(Fore.WHITE + f"\n[OXYLUS-AI]: {result}\n")
        history.append({"role": "user", "content": user_input})
        history.append({"role": "assistant", "content": result})

if __name__ == "__main__":
    main()
        
        history.append({"role": "user", "content": user_input})
        history.append({"role": "assistant", "content": result})

if __name__ == "__main__":
    main()
