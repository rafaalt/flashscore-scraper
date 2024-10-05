import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from model import Game, Team

def getUrl(gameId): 
    return f'https://www.flashscore.com.br/jogo/{gameId}/#/resumo-de-jogo/resumo-de-jogo'

def getGameInfo(gameId):
    url = getUrl(gameId)
    driver.get(url)
    try:
        names = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'participant__participantName')))[0:3:2]
        images = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'participant__image')))[0:2]
        score = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'detailScore__wrapper'))).find_elements(By.TAG_NAME, 'span')[0:3:2]
        homeTeam = Team(name=names[0].text,
                        imageUrl=images[0].get_attribute('src'))
        awayTeam = Team(name=names[1].text,
                        imageUrl=images[1].get_attribute('src'))
        game = Game(id=gameId,
                    homeTeam= homeTeam,
                    awayTeam= awayTeam,
                    scoreHome= score[0].text,
                    scoreAway= score[1].text)
        return game
    except:
        print(f'Erro no jogo {gameId}')
        return None

def getGamesId():
    url = 'https://www.flashscore.com.br/futebol/brasil/brasileirao-betano-2022/resultados/'
    driver.get(url)
    try: 
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'button#onetrust-accept-btn-handler')))
        button_cookies = driver.find_element(By.CSS_SELECTOR, 'button#onetrust-accept-btn-handler')
        button_cookies.click()
    except:
        print("cookies already closed")
    time.sleep(3)
    while True:
        moreButton = driver.find_elements(By.CSS_SELECTOR, 'a.event__more--static')
        if not moreButton:
            break
        moreButton[0].click()
        time.sleep(2)
    gamesId = []
    games = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'eventRowLink')))
    print(len(games))
    for game in games:
        id = game.get_attribute('href').split('/')[4]
        gamesId.append(id)

    return gamesId

service = Service()
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

driver = webdriver.Chrome(service=service, options=options)
game = getGameInfo('tQx0SNrj')
print(game)
#ids = getGamesId()

#for id in ids:
#    print(getGameInfo(id))

driver.quit()