import pandas as pd
import requests
import time
import numpy as np
import json
import datetime as dt
import os
from pynput import keyboard
import time

break_program = False
today = dt.date.today()
current_year = today.year

# Provides the ability to cancel the request by pressing the end key.
def on_press(key):
    global break_program
    if key == keyboard.Key.end:
        print ('end pressed')
        break_program = True
        return False

def get_hitting(start_season = 1876, end_season = current_year):
    years = list(map(str, range(start_season, end_season + 1)))
    hitting_df = pd.DataFrame()
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    for y in years:
        if break_program:
            break
        api_url = 'https://bdfed.stitch.mlbinfra.com/bdfed/stats/player?stitch_env=prod&season=' + y + '&sportId=1&stats=season&group=hitting&gameType=R&limit=10000&offset=0&sortStat=onBasePlusSlugging&order=desc'
        make_request = requests.get(url = api_url).json()
        temp_df = pd.DataFrame(make_request['stats'])
        hitting_df = pd.concat([hitting_df, temp_df], axis = 0)
        print(f'Finished {y} season.')
        lag = np.random.uniform(low = 2, high = 5)
        print(f'Waiting {round(lag, 1)} seconds before getting next season.')
        time.sleep(lag)
    # Data saved as csv in current working directory
    current_directory = os.getcwd()
    hitting_df.to_csv(current_directory + '\\hitting_data.csv')

def get_pitching(start_season = 1876, end_season = current_year):
    years = list(map(str, range(start_season, end_season + 1)))
    pitching_df = pd.DataFrame()
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    for y in years:
        if break_program:
            break
        api_url = 'https://bdfed.stitch.mlbinfra.com/bdfed/stats/player?stitch_env=prod&season=' + y + '&sportId=1&stats=season&group=pitching&gameType=R&limit=10000&offset=0&sortStat=earnedRunAverage&order=asc'
        make_request = requests.get(url = api_url).json()
        temp_df = pd.DataFrame(make_request['stats'])
        pitching_df = pd.concat([pitching_df, temp_df], axis = 0)
        print(f'Finished {y} season.')
        lag = np.random.uniform(low = 2, high = 5)
        print(f'Waiting {round(lag, 1)} seconds before getting next season.')
        time.sleep(lag)
    # Data saved as csv in current working directory
    current_directory = os.getcwd()
    pitching_df.to_csv(current_directory + '\\pitching_data.csv')

get_pitching()
get_hitting()