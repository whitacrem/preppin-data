import pandas as pd
import numpy as np
from datetime import datetime

student_data = pd.read_csv('wk_1_input.csv')

#print(student_data.columns)
#print(student_data.dtypes)

# Format the pupil's name in Firstname Lastname format
student_data["Pupil Name"] = student_data["pupil first name"] + " " + student_data["pupil last name"]

# Calculate pupil's birthdays in 2022
student_data["This Year's Birthday"] = student_data["Date of Birth"].apply(lambda x:x.replace(x[-4:], '2022'))

# Determine day of week birthday falls on
student_data["Birthday Date"] = pd.to_datetime(student_data["This Year's Birthday"])
student_data["Cake Needed On"] = student_data["Birthday Date"].dt.day_name().replace({'Saturday':'Friday', 'Sunday':'Friday'})

#Determine the month each birthday falls in
student_data["Month"] = student_data["Birthday Date"].dt.month_name()

#Determine BDs per weekday per month
student_data["BDs per Weekday and Month"] = student_data.groupby(["Cake Needed On", "Month"])["id"].transform('count')

#Remove extra columns and reorganize columns
student_data = student_data[["Pupil Name", "Date of Birth", "This Year's Birthday", "Month", "Cake Needed On", "BDs per Weekday and Month"]]

#Export to new CSV
student_data.to_csv('wk_2_output.csv')

