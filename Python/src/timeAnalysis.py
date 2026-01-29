import numpy
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

import fastf1

import logging
logging.getLogger("fastf1").setLevel(logging.WARNING)

# session = fastf1.get_session(2024, 'Azerbaijan', 'R')

# session.load()

# leclercLaps = session.laps.pick_driver('LEC')
# print(leclercLaps)

# times = leclercLaps['LapTime'].dt.total_seconds().tolist()
# lapNums = leclercLaps['LapNumber'].tolist()

def plotRaceLapTimes(lapNumbers, lapTimes):
    fig, ax = plt.subplots()
    ax.plot(lapNumbers, lapTimes)
    ax.set_ylim(min(lapTimes) - 1, max(lapTimes) + 1)
    plt.show()

# def plotDriverSeason(driverCode, year):

def getListDriverSeason(year):
    drivers = set()
    schedule = fastf1.get_event_schedule(year, include_testing=False)

    for _, event in schedule.iterrows():
        if event["EventFormat"] is None:
            continue

        session = fastf1.get_session(year, event["EventName"], "R")
        session.load(telemetry=False, weather=False)

        drivers.update(session.drivers)

    driver_codes = sorted(drivers)
    return driver_codes


driverSeasons = {}
for driver in getListDriverSeason(2024):
    driverSeasons[driver] = []

sessions = fastf1.get_event_schedule(2024, include_testing=False)
driver_races = []
for _, event in sessions.iterrows():
    
    session = fastf1.get_session(2024, event['EventName'], 'R')
    session.load(telemetry=False, weather=False, messages=False)

    results = session.results

    
    for driver in driverSeasons.keys():
        driver_result = results[results['Abbreviation'] == driver]
        if not driver_result.empty:
            position = int(driver_result['Position'])
        else:
            position = 0  # Did not finish or did not participate

        print("appedning")
        driverSeasons[driver].append(position)
        print("Position of " + driver + str(position))

print(driverSeasons)

'''
print(sessions["RoundNumber"].tolist())
fig, ax = plt.subplots()
for driver in driverSeasons.keys():
    places = driverSeasons[driver]
    print(places)
    ax.plot(sessions["RoundNumber"].tolist(), places.tolist())
plt.show()
'''
