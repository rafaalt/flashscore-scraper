import myLib

tourneys = ["america-do-sul/copa-libertadores",
            "brasil/copa-betano-do-brasil",
            "brasil/serie-b",
            "brasil/brasileirao-betano",
            "america-do-sul/copa-sul-americana"]

years = [2021,2022,2023,2024]

for tourney in tourneys:
    for year in years:
        myLib.xlsx_to_csv(xlsx_file_folder=f'data/{tourney}',
                          xlsx_file_name=year,
                          csv_file_folder=f'csv-data/{tourney}',
                          csv_file_name=year)
        