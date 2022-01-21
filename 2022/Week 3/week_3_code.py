import pandas as pd
import numpy as np

student_data = pd.read_csv('wk1_input.csv')
grades = pd.read_csv('wk3_grades.csv')

# Rename id column in student data table
student_data = student_data.rename(columns={'id':'Student ID'})

# Merge two tables
student_data = student_data.merge(grades)

# Drop parent contact columns
student_data = student_data.drop({'pupil first name', 'pupil last name', 'Date of Birth', 'Parental Contact Name_1', 'Parental Contact Name_2', 'Preferred Contact Employer', 'Parental Contact'}, axis=1)

# Pivot the data to create one row per subject per student and rename columns
student_data = pd.melt(student_data, id_vars=['Student ID', 'gender'], value_name='Score', var_name='Subject')

# Determine if subject has been passed
student_data['Pass Fail'] = [1 if x >= 75 else 0 for x in student_data['Score']]

# Aggregate passed courses and average scores
student_data = student_data.groupby(['Student ID', 'gender'], as_index=False).agg(
    avg_score = ('Score', 'mean'),
    passed = ('Pass Fail', 'sum')
)

# Rename aggregate columns
student_data = student_data.rename(columns={'avg_score':'Student\'s Avg Score', 'passed':'Passed Subjects', 'gender':'Gender'})

# Round decimal place of avg score to one decimal place 
student_data['Student\'s Avg Score'] = student_data['Student\'s Avg Score'].round(1)

# Reorganize the columns and output as a CSV
student_data = student_data[['Passed Subjects', 'Student\'s Avg Score', 'Student ID', 'Gender']]
student_data.to_csv('wk_3_output.csv')
