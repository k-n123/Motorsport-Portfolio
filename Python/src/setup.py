
# I recommend running this file whenever you install the code.
# It will extract the required data to CSV files in the data/ directory.

import fastf1
import os.path
import pandas as pd

import logging
logging.getLogger("fastf1").setLevel(logging.WARNING)

# Verify Data directory exists. If not, create it.
dataDirPath = "../data"
if not os.path.exists(dataDirPath):
    os.makedirs(dataDirPath)

# Create Fastf1 Cache
fastf1.Cache.enable_cache('../data/fastf1_cache')  

# Download Season Results for years 2018-2025
def downloadSeasonResults(year):
    results = {} # "Race Name Year" : Results
    schedule = fastf1.get_event_schedule(year, include_testing=False)

    for race in range(len(schedule)):
        race_name = schedule.get_event_by_round(race + 1)["EventName"]
        session = fastf1.get_session(year, race_name, 'R')
        session.load(telemetry=False, weather=False, messages=False)
        sessionResults = session.results['Abbreviation'].tolist()
        if len(sessionResults) != 20:
            sessionResults += ['N/A'] * (20 - len(sessionResults))

        results[str(race_name + " " + str(year))] = sessionResults

    results_df = pd.DataFrame(results)
    print(results_df)
    results_df.to_csv(f"../data/{year}_season.csv", index=False)

# Check if data already exists
seasons = [2018, 2019, 2020, 2021, 2022, 2023, 2024]
for year in seasons:
    filePath = f"../data/{year}_season.csv"
    if os.path.isfile(filePath):
        print(f"Data for {year} already exists. Skipping download.")
        continue

    downloadSeasonResults(year)