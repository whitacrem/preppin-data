import pandas as pd

# Import both sources
student_data = pd.read_csv('wk1_input.csv')
transport = pd.read_csv('week_4_travel.csv')

# Rename id column in student_data table to match transport table
student_data = student_data.rename(columns={'id':'Student ID'})

# Merge two tables
student_data = student_data.merge(transport)

# Remove unneeded columns
student_data = student_data.drop({'pupil first name', 'pupil last name', 'Date of Birth', 'gender', 'Parental Contact Name_1', 'Parental Contact Name_2', 
                                'Preferred Contact Employer', 'Parental Contact'}, axis=1)

# Pivot the data to create one column of weekdays and one of students' travel choices
student_data = pd.melt(student_data, id_vars=['Student ID'], value_name='Method of Travel', var_name='Weekday')

# Group data together by method of travel
# student_data = student_data.groupby(['Method of Travel', 'Weekday'], as_index=False)['Student ID'].count()
# Ran a print here to locate misspellings
# Correct misspellings
corrections = {'Bicycle':'^B.*', 'Car':'^Ca.*', 'Scooter':'^Sco.*', 'Helicopter': '^Heli.*', 'Walk':'^W.*'}
student_data['Method of Travel'] = student_data['Method of Travel'].replace(list(corrections.values()), list(corrections.keys()), regex=True)

# Group by method of travel and weekday now that spelling is corrected
student_data = student_data.groupby(['Method of Travel', 'Weekday'], as_index=False)['Student ID'].count()

# Rename student id column
student_data = student_data.rename(columns={'Student ID':'Number of Trips'})

# Create new column on sustainable or non-sustainable
student_data['Sustainable?'] = student_data['Method of Travel'].apply(lambda x: 'Non-Sustainable' if (x == 'Aeroplane') |(x =='Car') | (x =='Helicopter') | (x =='Van') 
                                 else 'Sustainable')

# Calculate the number of trips per day
student_data['Trips per day'] = student_data['Number of Trips'].groupby(student_data['Weekday']).transform('sum')

# Calculate percentage of trips for each method, rounded to two decimal points
student_data['% of trips per day'] = round(student_data['Number of Trips']/student_data['Trips per day'], 2)

# Reorganize columns to match challenge output
student_data = student_data[['Sustainable?', 'Method of Travel', 'Weekday', 'Number of Trips', 'Trips per day', '% of trips per day']]
student_data.to_csv('wk_4_output.csv')