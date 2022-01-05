import pandas as pd
import numpy as np
from datetime import datetime

student_data = pd.read_csv('wk_1_input.csv')

print(student_data.columns)

# Format the pupil's name in the Lastname, Firstname format
student_data["Pupil's Name"] = student_data["pupil last name"] + ", " + student_data["pupil first name"]

#Format the parental contact in the same way
student_data["Parental Contact Full Name"] = np.where(student_data["Parental Contact"] == 1, 
                                             student_data["pupil last name"] + ", " + student_data["Parental Contact Name_1"],
                                             student_data["pupil last name"] + ", " + student_data["Parental Contact Name_2"])

#Create parental contact email address that is firstname.lastname@company.com
student_data["Parental Contact Email Address"] = np.where(student_data["Parental Contact"] == 1,
                                                 student_data["Parental Contact Name_1"] + "." + student_data["pupil last name"] + "@" + student_data["Preferred Contact Employer"] + ".com",
                                                 student_data["Parental Contact Name_2"] + "." + student_data["pupil last name"] + "@" + student_data["Preferred Contact Employer"] + ".com")

#Create academic year field based on birthdate
student_birthdays = student_data["Date of Birth"]  #create temporary birthday list
student_year = []
for student in student_birthdays:  #change birthdays to academic year notation
    if datetime.strptime(student,'%m/%d/%Y') >= datetime.strptime('9/1/2014', '%m/%d/%Y'):
        student = 1
    elif datetime.strptime(student,'%m/%d/%Y') >= datetime.strptime('9/1/2013', '%m/%d/%Y'):
        student = 2
    elif datetime.strptime(student,'%m/%d/%Y') >= datetime.strptime('9/1/2012', '%m/%d/%Y'):
        student = 3
    elif datetime.strptime(student,'%m/%d/%Y') >= datetime.strptime('9/1/2011', '%m/%d/%Y'):
        student = 4
    elif datetime.strptime(student,'%m/%d/%Y') >= datetime.strptime('9/1/2010', '%m/%d/%Y'):
        student = 5
    student_year.append(student)
    
student_data["Academic Year"] = student_year #add converted list back to data frame as an "Academic Year" column

#Remove extra columns and reorder columns
student_data = student_data[["Academic Year", "Pupil's Name", "Parental Contact Full Name", "Parental Contact Email Address"]]

#Export to new CSV
student_data.to_csv('wk_1_output.csv')

