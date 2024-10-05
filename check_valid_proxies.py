import threading
import queue
import requests

q = queue.Queue()
valid_proxies = []
url = "https://www.flashscore.com.br/jogo/jZ8WU45J/#/resumo-de-jogo/resumo-de-jogo"

with open("proxies/all_proxies.txt", "r") as f:
    proxies = f.read().split("\n")
    valid_proxies = proxies
    for p in proxies:
        q.put(p)

def check_proxies():
    global q
    while not q.empty():
        proxy = q.get()
        try: 
            res = requests.get(url,
                                proxies={"http": proxy,
                                "https":proxy},
                                timeout=3)
        except:
            continue
        if res.status_code == 200:
            valid_proxies.append(proxy)
            print(proxy)

for _ in range(100):
    threading.Thread(target=check_proxies).start()

def check_proxy(proxy):
    proxies = {
        'http': proxy,
        'https': proxy,
    }
    try:
        response = requests.get('https://www.flashscore.com', proxies=proxies, timeout=5)
        return response.status_code == 200
    except Exception:
        return False
    


