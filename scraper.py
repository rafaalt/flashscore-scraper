import time
import pandas as pd
from tqdm import tqdm 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from model import Game, Team

def getUrl(gameId): 
    return f'https://www.flashscore.com.br/jogo/{gameId}/#/resumo-de-jogo/resumo-de-jogo'

def getSummaryIndex(text):
    if text == "ÁRBITRO:":
        return 0
    elif text == "ESTÁDIO:":
        return 1
    elif text == "CAPACIDADE:":
        return 2
    elif text == "PÚBLICO:":
        return 3
    else: 
        return 0
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
        
        summary = driver.find_elements(By.CLASS_NAME, '_summaryMatchInformation_1ky8z_4')
        infoArray = ["","","",""]
        if len(summary) > 0:
            summaryLeft = summary[0].find_elements(By.CLASS_NAME, '_infoLabelWrapper_1ky8z_17')
            summaryRight = summary[0].find_elements(By.CLASS_NAME, '_infoValue_1ky8z_26')
            for i in range(len(summaryRight)):
                values = summaryRight[i].find_elements(By.XPATH, './*')
                leftValue = summaryLeft[i].find_element(By.CLASS_NAME, '_overline_9pgur_4')
                info = ""
                for value in values:
                    info += value.text
                infoArray[getSummaryIndex(leftValue.text)] = info
        startTime = driver.find_element(By.CLASS_NAME, 'duelParticipant__startTime').find_element(By.TAG_NAME, 'div').text.split(' ')
        date = startTime[0].replace('.', '/')
        time = startTime[1]

        countryHeader = driver.find_element(By.CLASS_NAME, 'tournamentHeader__country')
        country = countryHeader.text.split(':')[0]
        round = countryHeader.find_element(By.TAG_NAME, 'a').text
        game = Game(id=gameId,
                    homeTeam=homeTeam,
                    awayTeam=awayTeam,
                    scoreHome=score[0].text,
                    scoreAway=score[1].text,
                    referee=infoArray[0],
                    stadium=infoArray[1],
                    capacity=infoArray[2],
                    public=infoArray[3],
                    date=date,
                    time=time,
                    country=country, 
                    round=round)
        return game
    except Exception as e:
        print(f'Erro no jogo {gameId}\n{e}')
        return None

def getGamesId(ano):
    url = f'https://www.flashscore.com.br/futebol/america-do-sul/copa-libertadores-{ano}/resultados/'
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
    for game in games:
        id = game.get_attribute('href').split('/')[4]
        gamesId.append(id)

    return gamesId

service = Service()
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

driver = webdriver.Chrome(service=service, options=options)
array = [2021, 2022, 2023]
for ano in array:
    ids = getGamesId(ano)
    games = []

    for id in tqdm(ids, desc="Buscando jogos..", unit="jogo"):
        game = getGameInfo(id)
        if game:
            games.append(game)

    def getTable(games):
        data = []
        for game in games:
            data.append({
                'id': game.id,
                'homeTeam': game.homeTeam.name,
                'homeTeamImage': game.homeTeam.imageUrl,
                'awayTeam': game.awayTeam.name,
                'awayTeamImage': game.awayTeam.imageUrl,
                'scoreHome': game.scoreHome,
                'scoreAway': game.scoreAway,
                'pointsHome': game.pointsHome,
                'pointsAway': game.pointsAway,
                'referee': game.referee,
                'stadium': game.stadium,
                'capacity': game.capacity,
                'public': game.public,
                'date': game.date,
                'time': game.time,
                'country': game.country,
                'round': game.round
            })

        df_jogos = pd.DataFrame(data)

        df_jogos.to_excel(f'sulamericana_{ano}.xlsx', index=False)

    getTable(games)

driver.quit()