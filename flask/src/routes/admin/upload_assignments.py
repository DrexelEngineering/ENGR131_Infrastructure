import os
import sys
import re

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

upload_assignment = Blueprint('upload_assignment', __name__)

@upload_assignment.route('/upload_assignment', methods=['POST'])
@login_required
def upload_students_():
    
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
    
    # Check for assignmentName in the form data
    if 'assignment_name' not in request.form:
        return 'assignment_name is required', 400
    assignment_name = request.form['assignment_name']
    
    # Check for assignmentID in the form data
    if 'assignment_id' not in request.form:
        return 'assignment_name is required', 400
    else:
        assignment_id = request.form['assignment_id'] 
        if is_string_number_combo(assignment_id):
            assignment_type, assignment_num = extract_string_number(assignment_id)
        else:
            return 'assignment_id must be a string in the format AssignmentType_AssignmentNumber', 400

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
        
        # Upsert into Assignment_table
        dict = [{"assignment_name": assignment_name,
                "assignment_id": assignment_id,
                "assignment_type": assignment_type,
                "assignment_num": assignment_num}]
        
        sql_call = upsert_json(dict, 'assignments', 'assignment_id')        
        out = commit_sql(cursor, sql_call)
        if not out:
            conn.rollback()  # Rollback in case of failure
            conn.close()
            return "Error occurred during SQL execution", 500
        
        dict = []
        
        # loops around all the entries in the json file and adds them to the dict for the question record
        for data in json_extracted:
            
            dict.append({"question_id": data.get('question_id', ''),
                        "assignment_id": assignment_id,
                        "question_name": data.get('questions_name', ''),
                        "max_score": data.get('max_score', ''),
                        "visible": data.get('visibility', '')})

        # Upsert into Question_table
        sql_call = upsert_json(dict, 'questions', ["assignment_id", "question_id"])   
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