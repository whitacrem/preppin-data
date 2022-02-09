import pandas as pd
import numpy as np

# Import both sources
grades = pd.read_csv('week_5_input.csv')

# Divide the students into 6 evenly distributed groups
grades = pd.melt(grades, id_vars=['Student ID'], var_name = 'Subject', value_name = 'Score')
label = ['F', 'E', 'D', 'C', 'B', 'A']
grades['Grade'] = grades.groupby('Subject')['Score'].transform(lambda x: pd.qcut(x, q=6, labels=label))

# Add metrics for high school application: A = 10, B = 8, C = 6, D = 4, E = 2, F = 1
point_convert = {'A': 10, 'B': 8, 'C': 6, 'D': 4, 'E': 2, 'F': 1}
grades['Points'] = grades['Grade'].apply(lambda x: point_convert[x]).astype(int)

# Determine total application points per student
grades['Total Points per Student'] = grades.groupby('Student ID')['Points'].transform('sum')

# Work out the average total points per student by grade
grades['Avg student total points per grade'] = round(grades.groupby('Grade')['Total Points per Student'].transform('mean'), 2)

# Take the average total score for students who have received at least one A and remove anyone who scored less than this
grades['Average scores per student'] = grades.groupby('Student ID')['Score'].transform('mean')
average_total_score_with_A = np.mean(grades[grades['Grade']=='A']['Average scores per student'])
grades = grades.loc[grades['Average scores per student'] >= average_total_score_with_A]

# Remove results where students received an A grade
grades = grades.loc[grades['Grade'] != 'A']

# How many students scored more than average if you ignore their As?
count = grades[grades['Average scores per student'] >= average_total_score_with_A]['Student ID'].nunique()

# Reformat for output
grades = grades[['Avg student total points per grade', 'Total Points per Student', 'Grade', 'Points', 'Subject', 'Score', 'Student ID']]
grades.to_csv('week_5_output.csv')




