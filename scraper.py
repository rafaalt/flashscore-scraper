import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from model import Game, Team

class FlashscoreScraper:
    def __init__(self):
        service = Service()
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(service=service, options=options)

    def getGameUrl(self, gameId): 
        return f'https://www.flashscore.com.br/jogo/{gameId}/#/resumo-de-jogo/resumo-de-jogo'

    def getSummaryIndex(self, text):
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
        
    def getGameInfo(self, gameId):
        url = self.getGameUrl(gameId)
        self.driver.get(url)
        try:
            names = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'participant__participantName')))[0:3:2]
            images = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'participant__image')))[0:2]
            score = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'detailScore__wrapper'))).find_elements(By.TAG_NAME, 'span')[0:3:2]
            homeTeam = Team(name=names[0].text,
                            imageUrl=images[0].get_attribute('src'))
            awayTeam = Team(name=names[1].text,
                            imageUrl=images[1].get_attribute('src'))
            
            summary = self.driver.find_elements(By.CLASS_NAME, 'wcl-summaryMatchInformation_WVEDL')
            infoArray = ["","","",""]
            if len(summary) > 0:
                summaryLeft = summary[0].find_elements(By.CLASS_NAME, 'wcl-infoLabelWrapper_MyVjC')
                summaryRight = summary[0].find_elements(By.CLASS_NAME, 'wcl-infoValue_0JeZb')
                for i in range(len(summaryRight)):
                    values = summaryRight[i].find_elements(By.XPATH, './*')
                    leftValue = summaryLeft[i].find_element(By.CLASS_NAME, 'wcl-overline_rOFfd')
                    info = ""
                    for value in values:
                        info += value.text
                    infoArray[self.getSummaryIndex(leftValue.text)] = info
            startTime = self.driver.find_element(By.CLASS_NAME, 'duelParticipant__startTime').find_element(By.TAG_NAME, 'div').text.split(' ')
            date = startTime[0].replace('.', '/')
            time = startTime[1]

            countryHeader = self.driver.find_element(By.CLASS_NAME, 'tournamentHeader__country')
            country = countryHeader.text.split(':')[0]
            round = countryHeader.find_element(By.TAG_NAME, 'a').text

            titleSections = self.driver.find_elements(By.CLASS_NAME, 'section__title')
            penaltisScore = None
            for section in titleSections:
                elements = section.find_elements(By.TAG_NAME, 'div')
                if len(elements) > 0:
                    if elements[0].text == "PÊNALTIS":
                        penaltisScore = elements[1].text

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
                        round=round,
                        penaltis=penaltisScore)
            return game
        except Exception as e:
            print(f'Erro no jogo {gameId}\n{e}')
            return None

    def getGamesId(self, tourney, year=2024):
        url = f'https://www.flashscore.com.br/futebol/{tourney}-{year}/resultados'
        self.driver.get(url)
        try: 
            WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'button#onetrust-accept-btn-handler')))
            button_cookies = self.driver.find_element(By.CSS_SELECTOR, 'button#onetrust-accept-btn-handler')
            button_cookies.click()
        except:
            print("cookies already closed")
        time.sleep(3)
        while True:
            moreButton = self.driver.find_elements(By.CSS_SELECTOR, 'a.event__more--static')
            if not moreButton:
                break
            moreButton[0].click()
            time.sleep(2)
        gamesId = []
        games = WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'eventRowLink')))
        for game in games:
            id = game.get_attribute('href').split('/')[4]
            gamesId.append(id)

        return gamesId

    def closeDriver(self):
        self.driver.quit()