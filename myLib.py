import pandas as pd
import os

def xlsx_to_csv(xlsx_file_folder,
                xlsx_file_name,
                csv_file_folder,
                csv_file_name):
    try:
        df = pd.read_excel(f'{xlsx_file_folder}/{xlsx_file_name}.xlsx')
        
        if not os.path.exists(csv_file_folder):
            os.makedirs(csv_file_folder)
        csv_file = f'{csv_file_folder}/{csv_file_name}.csv'
        df.to_csv(csv_file, index=False, encoding='utf-8')
        print(f"Arquivo convertido com sucesso! Salvo como: {csv_file}.csv")
    except Exception as e:
        print(f"Erro ao converter o arquivo: {e}")

def getExcelFile(games,tourney,year):
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
            'referee': game.referee,
            'stadium': game.stadium,
            'capacity': game.capacity,
            'public': game.public,
            'date': game.date,
            'time': game.time,
            'country': game.country,
            'round': game.round,
            'penaltis': game.penaltis
           })

        df_jogos = pd.DataFrame(data)

        destiny_folder = f"data/{tourney}"
        file_name = f"{destiny_folder}/{year}.xlsx"
        if not os.path.exists(destiny_folder):
            os.makedirs(destiny_folder)
            print(f"Pasta '{destiny_folder}' criada com sucesso.")
        df_jogos.to_excel(file_name, index=False)
