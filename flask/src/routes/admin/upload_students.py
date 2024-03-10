import os
import sys

import os
import sys

# Get the directory of your current script
current_dir = os.path.dirname(__file__)
# Go one folder back
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from file_translators.student_reader import student_csv_to_json
from flask_login import login_required
from util.sql_util import upsert_json
from flask import Blueprint, request
import time
from login.login import admin_login
import psycopg2  # Import psycopg2 for PostgreSQL database connection

upload_students = Blueprint('upload_students', __name__)

@upload_students.route('/upload_students', methods=['POST'])
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

    # If the user does not select a file, the browser submits an empty file without a filename
    if file.filename == '':
        return 'No selected file', 400

    if file:
        # Save the file to a temporary file
        temp_path = './temp_uploaded_file.csv'
        file.save(temp_path)

        # Process the CSV and convert it to JSON
        json_data = student_csv_to_json(temp_path)
        os.remove(temp_path)  # Remove the temporary file

        sql_call = upsert_json(json_data, 'students_enrolled', 'student_id')
        
        for query, value in zip(sql_call[0], sql_call[1]):
            try:
                cursor.execute(query, value)
            except Exception as e:
                print(f"Error executing query: {e}")
                return cursor.mogrify(query, value).decode('utf-8')

            # Sleep for 50 milliseconds
            time.sleep(0.05)

        conn.commit()
        # need to add the sql call here
        conn.close()
        return "success"
