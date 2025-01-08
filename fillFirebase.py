import firebase_admin
from firebase_admin import credentials, firestore
import csv
from datetime import datetime
import unicodedata

# Inicializa o Firebase Admin SDK
cred = credentials.Certificate("firebase/credentials.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def formatted_string(string):
    new_string = unicodedata.normalize('NFKD', string)
    new_string_2 = ''.join(c for c in new_string if not unicodedata.combining(c))
    return new_string_2.lower()

def import_csv_to_firestore(csv_file_name, database_name, tourney):
    with open(csv_file_name, encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            doc_id = row["id"]
            row["homeTeamLowercase"] = formatted_string(row["homeTeam"])
            row["awayeTeamLowercase"] = formatted_string(row["awayTeam"])
            row["tourney"] = tourney
            date_str = f"{row['date']} {row['time']}"
            try:
                if "time" in row:
                    del row["time"]
                date_obj = datetime.strptime(date_str, "%d/%m/%Y %H:%M")
                row["date"] = date_obj
                row["year"] = date_obj.year

            except ValueError:
                print(f"Erro ao converter a data: {date_str}")

            try:
                row["scoreHome"] = int(row["scoreHome"])
                row["scoreAway"] = int(row["scoreAway"])
            except ValueError:
                print(f"Erro ao converter o score do jogo.")

            db.collection(database_name).document(doc_id).set(row)

        print(f"Tabela {database_name} importada com sucesso!")

tourneys = {"america-do-sul/copa-libertadores": "Libertadores",
            "brasil/copa-betano-do-brasil": "CopaDoBrasil",
            "brasil/serie-b": "SerieB",
            "brasil/brasileirao-betano": "Brasileirao",
            "america-do-sul/copa-sul-americana": "Sulameiracana"} 

years = [2021,2022,2023,2024]

for year in years:
    for tourney, database_name in tourneys.items():
        import_csv_to_firestore(f"csv-data/{tourney}/{year}.csv", f"{database_name}-{year}", database_name)
