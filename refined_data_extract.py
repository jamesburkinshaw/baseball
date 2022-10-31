import pybaseball as baseball
import pandas as pd

# Save Data Locally 
# File Path
path = '/Users/jamesburkinshaw/Desktop/Masters/Project/Baseball/Data/Refined/'

# # Target Years
targetYears = [2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]

# People
baseballPeople = pd.DataFrame(baseball.people())
baseballPeople.to_csv(path + 'people.csv')

# Teams
baseballTeams = pd.DataFrame(baseball.teams())
baseballTeams.to_csv(path + 'teams.csv')

# Batting Stats
battingStats = pd.DataFrame(baseball.batting_stats(targetYears[0],targetYears[-1]))
battingStats.to_csv(path + 'batting_stats_2011-2021.csv')

# Fielding Stats
fieldingStats = pd.DataFrame(baseball.fielding_stats(targetYears[0],targetYears[-1]))
fieldingStats.to_csv(path + 'fielding_stats_2011-2021.csv')

# Pitching Stats
pitchingStats = pd.DataFrame(baseball.pitching_stats(targetYears[0],targetYears[-1]))
pitchingStats.to_csv(path + 'pitching_stats_2011-2021.csv')

# # WAR
batWAR = pd.DataFrame(baseball.bwar_bat())
batWAR = batWAR[batWAR['year_ID'].isin(targetYears)]
batWAR.to_csv(path + 'batting_war_2011-2021.csv')

pitchWAR = pd.DataFrame(baseball.bwar_pitch())
pitchWAR = pitchWAR[pitchWAR['year_ID'].isin(targetYears)]
pitchWAR.to_csv(path + 'pitching_war_2011-2021.csv')


