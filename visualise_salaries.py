from statistics import mean, median, stdev
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import re

# Determine if a player is a pitcher or position player
def playerType (row):
    # Find if player is primarily a pitcher by checking if lhp or rhp is first
    rhp = re.findall('^rhp', str(row['pos']))
    lhp = re.findall('^lhp', str(row['pos']))
    
    if len(rhp) > 0 or len(lhp) > 0:
        # player is a pitcher
        return 'pitcher'
    else:
        # player is not a pitcher
        return'position'
    
basePath = '/Users/jamesburkinshaw/Desktop/Masters/Project/Baseball/Data/'
salaryPath = basePath +'Salaries/'
dataPath = basePath +'Refined/'

# Target Years
targetYears = [2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]

# Read in File from initial Salary manipulation
salariesDf = pd.read_csv(salaryPath + 'all-salaries-normalised-adjusted-IDs.csv')

# All Salaries Stats
allSalariesList = salariesDf['salary'].to_list()
meanAllSalary = mean(allSalariesList)
stdDevAllSalary = stdev(allSalariesList)
salariesDf['salary_percentile'] = (salariesDf['normalised_salary']*100).round(5)

# Distrbution of all normalised salaries
salariesDfSample = salariesDf.sample(frac=1)
percentileCountsDf = salariesDfSample.groupby(['salary_percentile'])['salary_percentile'].size().reset_index(name='count')
plt.bar(percentileCountsDf['salary_percentile'], percentileCountsDf['count'], label='Normalised Salaries', color ='orange')
plt.xlabel('Rounded Normalised Salary')
plt.legend(loc="upper right")
plt.ylabel('Number of Salaries')
plt.title('Number of Normalised Salaries 2011-2021')
plt.text(0, -7, 'n=' + str(len(salariesDfSample.index)))
plt.show()

# Bin Salaries + Plot 
# Figure out number of bins using Sturge’s Rule
bins = round(1 + (3.222 * np.log([len(salariesDf.index)]))[0])
salariesDf['bin'] = pd.cut(salariesDf['salary'], bins=bins, precision = 2, right=True)
binCountsDf = salariesDf.groupby(['bin'])['bin'].size().reset_index(name='count')
binCountsDf['binLabel'] = binCountsDf['bin'].astype(str)
binCountsDf['binLabel'] = binCountsDf['binLabel'].str.replace(', ', ', ≤ ')
binCountsDf['binLabel'] = binCountsDf['binLabel'].str.replace('(', '> ')
binCountsDf['binLabel'] = binCountsDf['binLabel'].str.replace(']', '')
print(binCountsDf)

fig, ax = plt.subplots(figsize=(11,7))
plot = ax.bar(binCountsDf['binLabel'],binCountsDf['count'], label='Salaries in Bin', color='purple')
xticks_pos = [0.65*patch.get_width() + patch.get_xy()[0] for patch in plot]
ax.set_xticks(xticks_pos, labels=binCountsDf['binLabel'].astype(str), ha='right', rotation=45)
ax.set_title('Binned Salary Counts 2011-2021')
ax.set_ylabel('Count')
ax.set_xlabel('Salary Bin')
ax.legend(loc='upper right')
ax.bar_label(plot)
plt.show()

# Yearly Salary Stats
yearSalariesStats = []
yearSalariesCountsList = []
yearPositionSalariesStats = []
for year in targetYears:
    # Stats
    yearSalariesDf = salariesDf.loc[salariesDf['year'] == year]
    yearSalariesStats.append([year,mean(yearSalariesDf['salary'].to_list()),median(yearSalariesDf['salary'].to_list()),stdev(yearSalariesDf['salary'].to_list())])
    
    # Counts
    yearSalariesCountsDf = yearSalariesDf.groupby(['salary_percentile'])['salary_percentile'].size().reset_index(name='count')
    yearSalariesCountsDf['year'] = str(year)
    
    for row in yearSalariesCountsDf.values.tolist():
        yearSalariesCountsList.append(row)
        
    # By Position
    yearSalariesDf['player_type'] = yearSalariesDf.apply(lambda row: playerType(row), axis=1)
    yearPitcherSalariesDf = yearSalariesDf.loc[yearSalariesDf['player_type'] == 'pitcher']
    yearPosPlayerSalariesDf = yearSalariesDf.loc[yearSalariesDf['player_type'] == 'position']
    yearPositionSalariesStats.append([year, mean(yearPitcherSalariesDf['salary'].tolist()),median(yearPitcherSalariesDf['salary'].tolist()), mean(yearPosPlayerSalariesDf['salary'].tolist()), median(yearPosPlayerSalariesDf['salary'].tolist())])

yearSalariesStatsDf = pd.DataFrame(data=yearSalariesStats, columns=['year', 'mean_salary', 'median_salary', 'stdev_salary'])
allYearSalariesCountsDf = pd.DataFrame(yearSalariesCountsList, columns=['normalised_salary','count', 'year'])
yearPositionSalaryStatsDf = pd.DataFrame(data=yearPositionSalariesStats, columns=['year', 'mean_pitcher_salary','median_pitcher_salary', 'mean_pos_player_salary', 'median_pos_player_salary'])

# Yearly Mean Salaries Plot
plt.plot(yearSalariesStatsDf['year'], yearSalariesStatsDf['mean_salary'], color='orange', label='Mean Salary')
plt.plot(yearSalariesStatsDf['year'], yearSalariesStatsDf['median_salary'], color='purple', label='Median Salary')
plt.legend(loc="right")
plt.xticks(yearSalariesStatsDf['year'])
plt.xlabel('Year')
plt.ylabel('Salary')
plt.title('Mean Salary 2011-2021')
plt.show()

# Plot Distribution of Salaries for each Year
for year in targetYears:  
    plt.bar(allYearSalariesCountsDf.loc[allYearSalariesCountsDf['year'] == str(year)]['normalised_salary'], allYearSalariesCountsDf.loc[allYearSalariesCountsDf['year'] == str(year)]['count'], label=str(year), color = 'C'+str(year-2011))
plt.show()

# Yearly Mean Salaries Plot
plt.plot(yearPositionSalaryStatsDf['year'], yearPositionSalaryStatsDf['mean_pitcher_salary'], color='orange', label='Mean Pitcher Salary')
plt.plot(yearPositionSalaryStatsDf['year'], yearPositionSalaryStatsDf['median_pitcher_salary'], color='red', label='Median Pitcher Salary')
plt.plot(yearPositionSalaryStatsDf['year'], yearPositionSalaryStatsDf['mean_pos_player_salary'], color='purple', label='Mean Position Player Salary')
plt.plot(yearPositionSalaryStatsDf['year'], yearPositionSalaryStatsDf['median_pos_player_salary'], color='blue', label='Median Position Player Salary')
plt.legend()
plt.xticks(yearSalariesStatsDf['year'])
plt.xlabel('Year')
plt.ylabel('Salary')
plt.title('Average Salaries by Position 2011-2021')
plt.show()
