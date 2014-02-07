
import pandas as pd
import os
import pprint
import csv

cwd = os.getcwd() + '/2012_nfl_pbp_data_reg.csv'

data = pd.read_csv(cwd)

game_ids = list(set(data.values[:,0]))
team_ids = list(set(data.values[:,4]))
team_ids = team_ids[1:]

season_gap = dict()
actual_gap = dict()
wins = dict()
losses = dict()
scores = dict()
for i in team_ids:
    season_gap[i] = 0
    actual_gap[i] = 0
    wins[i] = 0
    losses[i] = 0
    scores[i] = dict()

def get_gap(game, wins, losses):
    
    # initialize values
    last_play = game[0,:]
    time_passed = 0
    [team1,team2] = game[0][4:6] 
    average_gap = dict()
    actual_gap = dict()
    total_time = 0
    average_gap[team1] = 0
    average_gap[team2] = 0
    old_score_diff = 0
    old_time = 3600

    for play in game[1:]:
        score_diff = float(play[10])-float(play[11]) # current offense - current defense
        if old_score_diff != score_diff: # if the score changed
            curr_time = float(play[2])*60 + float(play[3])
            time_passed = old_time - curr_time # find that amount of time that passed
            old_time = curr_time
            offense = play[4]
            if team1 == offense: # updated the average gap
                average_gap[team1] += time_passed*score_diff
                average_gap[team2] += time_passed*-score_diff
            elif team2 == offense:
                average_gap[team1] += time_passed*-score_diff
                average_gap[team2] += time_passed*score_diff
    total_time += 3600 - curr_time

    average_gap[team1] = average_gap[team1]/total_time 
    average_gap[team2] = average_gap[team2]/total_time # calculate average gap
    
    if team1 == offense:
        actual_gap[team1] = score_diff
        actual_gap[team2] = -score_diff
    else:
        actual_gap[team1] = -score_diff
        actual_gap[team2] = score_diff
    if actual_gap[team1] > 0: # if team 1 won
        wins[team1] += 1
        losses[team2] += 1
    elif actual_gap[team2] > 0:
        wins[team2] += 1
        losses[team1] += 1      
    return average_gap, actual_gap, wins, losses

for i in game_ids:
    game = data.values[data.gameid==i]
    average_gap, gap, wins, losses = get_gap(game, wins, losses)
    for j in average_gap:
        season_gap[j] += average_gap[j]
        actual_gap[j] += gap[j]

with open("2012_nfl_gap.csv", "wb") as csvfile:
    c = csv.writer(csvfile, delimiter=',')
    for i in wins:
        c.writerow([i,season_gap[i],actual_gap[i],wins[i]])

