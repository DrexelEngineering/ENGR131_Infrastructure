import pandas as pd
import json
from datetime import datetime, timedelta
import pytz


def student_csv_to_json(csv_path, course = "ENGR 131", year = 2023, semester = "Winter"):
    """function that takes in a csv file and returns a json file for the students
    The raw file is a CSV from blackboards

    Args:
        csv_path (filepath): Path to the CSV file
        course (str, optional): Course which the student is enrolled. Defaults to "ENGR 131".
        year (int, optional): Year of the course. Defaults to 2023.
        winter (str, optional): Semester of the course. Defaults to "Winter".

    Returns:
        JSON: JSON file of all of the students
    """
    
    # Read the CSV file
    data = pd.read_csv(csv_path)

    # Function to split the section into lecture and lab
    def split_section(section):
        parts = section.split('.')
        return parts[0], parts[1] if len(parts) > 1 else None

    # Preparing the JSON structure
    students_json = []
    for index, row in data.iterrows():
        lecture_section, lab_section = split_section(str(row['Child Course ID']))
        student_info = {
            "student_id": row['Username'],
            "first_name": row['First Name'],
            "last_name": row['Last Name'],
            "section": lecture_section,
            "lab_section": lab_section,
            "course": course,
            "year": year,
            "semester":semester,
        }
        students_json.append(student_info)
        
    # Return the JSON data
    return students_json


def lab_csv_to_json(file_path, section_id, day_of_week, start_time):
    """function that takes in a csv file and returns a json file for the lab

    Args:
        file_path (filepath): location where the JSON file is located
        section_id (int): section number for the lab
        day_of_week (str): single value specifying the day of the week
        start_time (datatime): time stamp when the lab starts

    Returns:
        JSON: JSON file of all of the students
    """    
    
    # Get current date in EST timezone
    est_timezone = pytz.timezone('America/New_York')
    current_date_est = datetime.now(est_timezone).date()

    # Parse entered time string
    entered_time_obj = datetime.strptime(start_time, "%H:%M:%S").time()
    
    # Combine current date with entered time
    entered_time_est = datetime.combine(current_date_est, entered_time_obj)

    # Add 1 hour and 50 minutes
    later_time_est = entered_time_est + timedelta(hours=1, minutes=50)
    
    # Read the CSV file
    data = pd.read_csv(file_path)

    # Preparing the JSON structure
    lab_json = []
    for index, row in data.iterrows():
        student_record_template = {
            "lastname": row['lastName'],  # Character varying(255)
            "firstname": row['firstName'],  # Character varying(255)
            "middlename": row['middleName'],  # Character varying(255)
            "levelname": row['levelname'],  # Character varying(255)
            "classificationname": row['classificationname'],  # Character varying(255)
            "majorname": row['majorname'],  # Character varying(255)
            "emailaddress": row['emailAddress'],  # Character varying(255)
            "student_id": row['UserID'],  # Character varying(255)
            "zoomid": row['ZoomID'],  # Character varying(255)
            "sectionnumber": section_id,  # Integer
            "starttime": str(entered_time_est.time()),  # Time with time zone, placeholder None for datetime.time or similar
            "endtime": str(later_time_est.time()),  # Time with time zone, placeholder None for datetime.time or similar
            "day_of_week": day_of_week,  # Text
        }
        lab_json.append(student_record_template)
        
    # Return the JSON data
    return lab_json