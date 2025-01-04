from scraper import FlashscoreScraper
import myLib
from tqdm import tqdm

scraper = FlashscoreScraper()

tourneys = [#"america-do-sul/copa-libertadores",
            "brasil/copa-betano-do-brasil"]
            #"brasil/serie-b",
            #"brasil/brasileirao-betano",
            #"america-do-sul/copa-sul-americana"]

years = [2021,2022]

for tourney in tourneys:
    for year in years:
        ids = scraper.getGamesId(tourney=tourney,
                                 year=year)
        games = []
        for id in tqdm(ids, desc="Buscando jogos..", unit="jogo"):
            game = scraper.getGameInfo(id)
            if game:
                games.append(game)

        myLib.getExcelFile(games=games,
                           tourney=tourney,
                           year=year)
        
scraper.closeDriver()