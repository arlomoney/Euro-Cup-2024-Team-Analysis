import pandas as pd

# importing the data
df = pd.read_csv(r'C:\Users\arlen\OneDrive\Python and data\matches.csv')

# cleaning the data to make it easier to work with
df['team1'] = df['team1'].str.lower()
df['team2'] = df['team2'].str.lower()

df_clean = df.dropna().drop_duplicates()
df_clean = df_clean.drop(columns=['stadium', 'audience', 'team1_corners', 'team2_corners', 
                                  'team1_passes', 'team2_passes', 'team1_offsides', 'team2_offsides', 
                                  'team1_throws', 'team2_throws', 'team1_clearances', 'team2_clearances'])

metrics = ['goals', 'total_shots', 'shots_on_target', 'blocked_shots', 'interceptions', 'keeper_saves', 'duels_won']

# function that evaluates a certain teams performance
def evaluate_team_performance(team_name):
    team_wins = 0
    total_games = 0

    # iterates through the metrics and counts up scores to see which team did better
    for index, row in df_clean.iterrows():
        if row['team1'] == team_name or row['team2'] == team_name:
            team1_score = 0
            team2_score = 0

            for metric in metrics:
                team1_metric = f'team1_{metric}'
                team2_metric = f'team2_{metric}'

                if team1_metric in df_clean.columns and team2_metric in df_clean.columns:
                    if row[team1_metric] > row[team2_metric]:
                        team1_score += 1
                    elif row[team1_metric] < row[team2_metric]:
                        team2_score += 1

            if (row['team1'] == team_name and team1_score > team2_score) or \
               (row['team2'] == team_name and team2_score > team1_score):
                team_wins += 1
            
            total_games += 1

    #if user inputs a country that didn't participate in the euro cup
    if total_games == 0:
        return f"Team {team_name} did not play any games in the UEFA Euro Cup 2024."
    
    # calculates objective percentage based off the data from metrics
    win_percentage = (team_wins / total_games) * 100
    if(win_percentage > 50.00):
        return f"Team {team_name} outperformed the opposing team, achieving an objective score of {win_percentage:.2f}%"
    else:
        return f"Team {team_name} underperformed compared to the opposing team, with an objective score of {win_percentage:.2f}%"

team_name = input("Enter the name of the team: ").lower()

print("Entered team name:", team_name)

result = evaluate_team_performance(team_name)
print(result)
