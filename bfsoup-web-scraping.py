import sys
from bs4 import BeautifulSoup
import requests
import pandas as pd

# System Info
print(
    f"System Info:\nI am using Python version {sys.version[0:5]}", end=('\n\n')
)

# Web Scraping
webpage_request = requests.get('https://www.premierleague.com/tables')
webpage = webpage_request.content
soup = BeautifulSoup(webpage, 'html.parser')
league_positions = soup.find_all(attrs={'class': 'resultHighlight'})
league_teams = soup.find_all(attrs={'class': "long"})
league_points = soup.find_all(attrs={'class': "points"})

# Data Manipulation
position = sorted(
    set(list(
        [int(position.get_text().strip())
         for position in league_positions][:21])))
teams = [team.get_text().strip() for team in league_teams][:21]
points = [point.get_text().strip() for point in league_points][1:21]
premier_league_table = list(zip(teams, points))


# Data in a DataFrame
print("Final Premier league standing:", end=('\n'))
df = pd.DataFrame(
    premier_league_table,
    index=position,
    columns=['team', 'points'])
print(df, end=("\n\n"))

# Rename the index column to position
df.index.rename("position", inplace=True)

# Export the data to csv
df.to_csv("preimer_league_season_20-21.csv")
print("Your Webscraping is complete")
