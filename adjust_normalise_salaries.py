from email.mime import base
import re
import string
import cpi
import pandas as pd
import numpy as np
from sklearn import preprocessing

# Save Data Locally 
# File Path

basePath = '/Users/jamesburkinshaw/Desktop/Masters/Project/Baseball/Data/'
salaryPath = basePath +'Salaries/'
dataPath = basePath +'Refined/'


# # Target Years
targetYears = [2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]

#set to True to load from files and adjust for inflation
update = False

if update:
    # Get most recent CPI values
    cpi.update()
    
    allSalaries = []
    for year in targetYears:
        # Load salaries for year
        yearSalaries = pd.DataFrame(pd.read_csv(salaryPath + 'MLB-Salaries-'+str(year)+'.csv', encoding='cp1252'))
        
        # Remove forfeited salaries
        yearSalaries = yearSalaries[yearSalaries.Salary != 'forfeited']
        
        # Add year column
        yearSalaries['Year'] = str(year)
        
        # Adjust for inflation
        yearSalaries['Salary'] = yearSalaries['Salary'].astype('float')
        yearSalaries['Salary'] = cpi.inflate(yearSalaries['Salary'], year)
        
        yearSalariesList = yearSalaries.values.tolist()
        for row in yearSalariesList:
            allSalaries.append(row)
        
    allSalariesDf = pd.DataFrame(data=allSalaries, columns=['name', 'pos', 'mls', 'salary', 'year'])
    allSalariesDf.to_csv(salaryPath + 'All-Salaries-Adjusted.csv')

else:
    # If update is not required just load the adjusted salaries from a file
    allSalariesDf = pd.read_csv(salaryPath + 'All-Salaries-Adjusted.csv')

# # Normalise salaries (sklearn)
# minMaxScaler = preprocessing.MinMaxScaler()
# allSalaries = np.array(allSalariesDf['salary'])
# allSalariesNorm = minMaxScaler.fit_transform(allSalaries.reshape(allSalaries.size, -1))
# allSalariesDf['normalised_salary'] = allSalariesNorm.reshape(-1, allSalariesNorm.size)

# Normalise salaries (manual)
allSalariesDf['normalised_salary'] = (allSalariesDf['salary'] - allSalariesDf['salary'].min()) / (allSalariesDf['salary'].max() - allSalariesDf['salary'].min())

# Split names into surname and firstname
allSalariesDf['surname'] = allSalariesDf['name'].str.split(',', expand=True)[0].str.upper()
allSalariesDf['fname'] = allSalariesDf['name'].str.split(',', expand=True)[1].str.upper()

allSalariesDf['surname'] = allSalariesDf['surname'].str.strip()
allSalariesDf['fname'] = allSalariesDf['fname'].str.strip()

# # Testing
# allSalariesDf.to_csv(basePath + 'all-salaries-test.csv')
# allSalariesDfTest = allSalariesDf.loc[(allSalariesDf['surname'] == 'RODRIGUEZ') & (allSalariesDf['fname'] == 'ALEX')]
# print(allSalariesDfTest)

peopleDf = pd.read_csv(dataPath + 'people.csv')
peopleDf['surname'] = peopleDf['nameLast'].str.upper()
peopleDf['fname'] = peopleDf['nameFirst'].str.upper()
peopleDf = peopleDf[['playerID', 'fname', 'surname', 'retroID', 'bbrefID']]

# # Testing
# peopleDf.to_csv(basePath + 'people-test.csv')
# peopleDfTest = peopleDf.loc[(peopleDf['surname'] == 'RODRIGUEZ') & (peopleDf['fname'] == 'ALEX')]
# print(peopleDfTest)

allSalariesIdsDf = allSalariesDf.merge(peopleDf, how='inner', on=['fname', 'surname'])
# print(allSalariesIdsDf)
allSalariesIdsDf.to_csv(salaryPath + 'all-salaries-normalised-adjusted-IDs.csv')
