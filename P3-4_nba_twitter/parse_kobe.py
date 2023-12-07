import json
import pandas as pd

path = "KobeStats.json"

def load_json(path):
    with open(path, "r") as input_file:
        d = json.load(input_file)
    return d

data = load_json(path)["resultSets"][0]["rowSet"]

headers = ["SEASON_ID", "PLAYER_AGE", "GP", "PTS", "REB", "AST"]

# Create a list of dictionaries from the JSON data
data_list = []

for season in data:
    season_data = {
        "SEASON_ID": season[1],
        "PLAYER_AGE": season[5],
        "GP": season[6],
        "PTS": season[26],
        "AST": season[21],
        "REB": season[20],
    }
    data_list.append(season_data)

# Create a Pandas DataFrame from the list of dictionaries
df = pd.DataFrame(data_list, columns=headers)

# Print the resulting DataFrame
print(df)
# Calculate total points for each season
df['Total Points'] = df['PTS'] * df['GP']

# Get season with max total points
season_max_points = df.loc[df['Total Points'].idxmax(), 'SEASON_ID']
# Get season with min total points
season_min_points = df.loc[df['Total Points'].idxmin(), 'SEASON_ID']
print("Best Season: ",season_max_points)
print("Worst Season: ",season_min_points)

total_points = (df["PTS"] * df["GP"]).sum()
total_games_played = df["GP"].sum()

avg_career_points = total_points / total_games_played
print("Average career points",avg_career_points)

total_rebounds = (df["REB"] * df["GP"]).sum()
avg_career_rebounds = total_rebounds / total_games_played

print("Average career rebounds",avg_career_rebounds)
total_assists = (df["AST"] * df["GP"]).sum()

avg_career_assists = total_assists / total_games_played
print("Average career assists",avg_career_assists)
