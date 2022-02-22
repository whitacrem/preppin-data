import pandas as pd
import numpy as np

# Join people, location. and leader data sets together
people = pd.read_csv('people.csv')
location = pd.read_csv('location.csv')
leaders = pd.read_csv('leaders.csv')

final = people.merge(location, on='Location ID')
final = final.rename(columns={'id':'People ID', 'Leader 1':'id'})
final = final.merge(leaders, on='id')
final['Agent Name'] = final['last_name_x'].str.cat(final['first_name_x'], sep=', ')
final['Leader Name'] = final['last_name_y'].str.cat(final['first_name_y'], sep=', ')
final = final.drop(columns=['Location ID', 'first_name_x', 'last_name_x', 'first_name_y', 'last_name_y'])
final = final.rename(columns={'People ID':'id', 'id':'Leader 1'})

# Add the month start dates, limit to just 2021, and add to final df
dates = pd.read_csv('Date Dim.csv')
dates['Month Start Date'] = pd.to_datetime(dates['Month Start Date'])
dates = dates[dates['Month Start Date'] < '2022/01/01']
final = final.merge(dates, how='cross')

# Merge monthly data, merge mismatched fields, create a monthly start date, and remove table names + file paths fields
metrics = pd.read_excel('MetricData2021.xlsx', sheet_name=['Jan','Feb','Mar','Apr'])
metrics = pd.concat([metrics.assign(Month=n) for n,metrics in metrics.items()])
col_names = {'Calls Offered':'Offered', 'Calls Not Answered':'Not Answered', 'Calls Answered':'Answered'}
metrics = metrics.rename(columns=col_names)
metrics2 = pd.read_excel('MetricData2021.xlsx', sheet_name=['May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
metrics2 = pd.concat([metrics2.assign(Month=n) for n,metrics2 in metrics2.items()])
metrics = pd.concat([metrics, metrics2], ignore_index=True)
metrics['Month Start Date'] = pd.to_datetime('2021 ' + metrics['Month'],format='%Y %b')
metrics['Month Start Date'] = metrics['Month Start Date'].dt.strftime('%Y-%d-%m').astype('datetime64[ns]')
metrics = metrics.merge(dates, on='Month Start Date')

# Join the metrics data with the people data
final = final.merge(metrics, left_on='id', right_on='AgentID')

# Add goals, clean to have goal name and numeric value, combine with people data
final['Not Answered Percent < 5'] = 5
final['Sentiment Score >= 0'] = 0

# Calculations and Met Goal Flags
final.fillna('').reset_index()
final['Not Answered Rate'] = final['Not Answered'] / final['Offered']
final['Agent Avg Duration'] = final['Total Duration'].groupby(final['id']).mean()
final['Met Sentiment Goal'] = final['Sentiment'] >= final['Sentiment Score >= 0']
final['Met Not Answered Rate'] = final['Not Answered Rate'] < final['Not Answered Percent < 5']

# Format and output
final = final[['id', 'Agent Name', 'Leader 1', 'Leader Name', 'Month Start Date_x', 'Location', 'Answered', 'Not Answered', 'Not Answered Rate', 'Met Not Answered Rate', 
            'Not Answered Percent < 5', 'Offered', 'Total Duration', 'Agent Avg Duration', 'Transfers', 'Sentiment', 'Sentiment Score >= 0', 'Met Sentiment Goal']]
final = final.rename(columns={'Month Start Date_x':'Month Start Date', 'Answered':'Calls Answered', 'Not Answered':'Calls Not Answered', 'Offered':'Calls Offered'})
final.to_csv('week7_output.csv')


