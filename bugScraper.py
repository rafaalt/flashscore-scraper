from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from model import Game
from fake_useragent import UserAgent

def getProxyList(): 
    with open("proxies/all_proxies.txt", "r") as f:
        proxies = f.read().split("\n")
        return proxies
    
def getGameUrl(gameId): 
    return f"https://www.flashscore.com.br/jogo/{gameId}/#/resumo-de-jogo/resumo-de-jogo"

def getGameInfo(gameId):
    url = getGameUrl(gameId)
    service = Service()
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    wait = WebDriverWait(driver, 20)  # Aguarda até 20 segundos
    names = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "participant__participantName")))[0:3:2]
    score = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "detailScore__wrapper")))[0:3:2]
    driver.quit()
    game = Game(id=gameId,
                homeTeam=names[0].text,
                awayTeam=names[1].text,
                scoreHome=score[0].text,
                scoreAway=score[1].text)
    return game

def getGamesId():
    
game = getGameInfo("jZ8WU45J")
print(game)