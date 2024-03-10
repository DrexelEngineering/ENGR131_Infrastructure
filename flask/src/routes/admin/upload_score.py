import os
import sys
import re

from datetime import datetime, timezone, timedelta

# Get the directory of your current script
current_dir = os.path.dirname(__file__)
# Go one folder back
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from file_translators.assignment_reader import assignment_JSON
from flask_login import login_required
from util.sql_util import upsert_json, commit_sql
from flask import Blueprint, request
import time
from login.login import admin_login

upload_score = Blueprint('upload_score', __name__)

@upload_score.route('/upload_score', methods=['POST'])
@login_required
def upload_score_():
    
    # Check for assignmentName in the form data
    if 'password' not in request.form:
        return 'password is required', 400
    password = request.form['password']
    
    conn = admin_login(password)
    cursor = conn.cursor()
    
    # Check if the request has the file part
    if 'file' not in request.files:
        return 'No file part in the request', 400
    file = request.files['file']
    
    # Check for original_file_name  in the form data
    if 'original_file_name' not in request.form:
        return 'original_file_name is required', 400
    original_file_name = request.form['original_file_name']
    
    # Check for assignmentName in the form data
    if 'student_id' not in request.form:
        return 'student_id is required', 400
    student_id = request.form['student_id']
    
    # Check for assignmentID in the form data
    if 'assignment_id' not in request.form:
        return 'assignment_name is required', 400
    else:
        assignment_id = request.form['assignment_id'] 

    # If the user does not select a file, the browser submits an empty file without a filename
    if file.filename == '':
        return 'No selected file', 400

    if file:
        
        # Save the file to a temporary file
        temp_path = './temp_uploaded_file.JSON'
        file.save(temp_path)

        # need to parse the extracted json file
        json_extracted = assignment_JSON(temp_path)
        
        os.remove(temp_path)  # Remove the temporary file
        
        ############################## SUBMISSION SCORE ##############################
        
        # Get the current UTC time
        now_utc = datetime.now(timezone.utc)

        # East Coast of the United States is typically UTC-5, but during Daylight Saving Time it's UTC-4
        # Checking if it's Daylight Saving Time
        east_coast_time = now_utc - timedelta(hours=4 if now_utc.dst() else 5)

        # Format the date and time in a nice string format
        formatted_date_time = east_coast_time.strftime("%Y-%m-%d %H:%M:%S")
        
        # calculate the total score
        total_score = sum(float(d.get("score", 0)) for d in json_extracted)
        max_score = sum(float(d.get("max_score", 0)) for d in json_extracted)
        
        percentage_score = (total_score/max_score)*100
        
        dict = [{   "submission_id": f"{student_id}_{assignment_id}_{formatted_date_time}",
                    "student_id": student_id,
                    "assignment_id": assignment_id,
                    "submitter_type": "admin",
                    "total_score": total_score,
                    "max_score": max_score,
                    "percentage_score": percentage_score,
                    "original_file_name": original_file_name,
                }]
        
        if 'start_time' in request.form:
            dict[0]["start_time"] = request.form['start_time']
            
        if 'end_time' in request.form:
            dict[0]["end_time"] = request.form['end_time']
        
        sql_call = upsert_json(dict, 'submissions', 'submission_id')        
        out = commit_sql(cursor, sql_call)
        if not out:
            conn.rollback()  # Rollback in case of failure
            conn.close()
            return "Error occurred during SQL execution", 500
        
        ############################## QUESTION SCORE ##############################
        
        dict = []
        
        for data in json_extracted:
        
            dict.append({"submission_id": f"{student_id}_{assignment_id}_{formatted_date_time}",
                    "assignment_id": assignment_id,
                    "question_id": data.get('question_id'),
                    "student_id": student_id,
                    "score": data.get('score', 0),
                    "max_score": data.get('max_score', 0),
                    "output": data.get('output', 'NA'),
                    "visible": data.get('visibility', True)
                    })
            
        sql_call = upsert_json(dict, 'question_score', ['submission_id', 'question_id'])        
        out = commit_sql(cursor, sql_call)
        if not out:
            conn.rollback()  # Rollback in case of failure
            conn.close()
            return "Error occurred during SQL execution", 500
        
        conn.commit()
        # need to add the sql call here
        conn.close()
        return "success"

def is_string_number_combo(s):
    pattern = r'^[A-Za-z]+_[0-9]+$'
    return bool(re.match(pattern, s))

def extract_string_number(s):
    pattern = r'^([A-Za-z]+)_([0-9]+)$'
    match = re.match(pattern, s)
    if match:
        return match.group(1), int(match.group(2))