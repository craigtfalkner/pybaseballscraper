import pandas as pd
import requests
import time
import numpy as np
import json
import datetime as dt
import os

# Hitting Stats URL - starting point 
hitting_stats_url = 'https://bdfed.stitch.mlbinfra.com/bdfed/stats/player?stitch_env=prod&season=2023&sportId=1&stats=season&group=hitting&gameType=R&limit=10000&offset=0&sortStat=onBasePlusSlugging&order=desc'

# Make request
testing = requests.get(url = hitting_stats_url).json()

# to DataFrame
df = pd.DataFrame(testing['stats'])

# Get column names
df_columns = list(df.columns)

# Create list of available stat years - starts in 1876
today = dt.date.today()
current_year = today.year
years = [x for x in range(1876, current_year + 1)] 
years = map(str, years)

# Lag added, not sure if this is required.
hitting_df = pd.DataFrame(columns = df_columns)

for y in years:
    api_url = 'https://bdfed.stitch.mlbinfra.com/bdfed/stats/player?stitch_env=prod&season=' + y + '&sportId=1&stats=season&group=hitting&gameType=R&limit=10000&offset=0&sortStat=onBasePlusSlugging&order=desc'
    make_r = requests.get(url = api_url).json()
    temp_df = pd.DataFrame(make_r['stats'], columns = df_columns)
    hitting_df = pd.concat([hitting_df, temp_df], axis = 0)
    print(f'Finished {y} season.')
    lag = np.random.uniform(low = 5, high = 15)
    print(f'Waiting {round(lag, 1)} seconds before getting next season.')
    time.sleep(lag)

# Data saved as csv in current working directory
current_directory = os.getcwd()
hitting_df.to_csv(current_directory + '\\hitting_data.csv')