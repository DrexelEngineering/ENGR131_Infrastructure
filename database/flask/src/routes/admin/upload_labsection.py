import os
import sys
from file_translators.student_reader import lab_csv_to_json
from flask_login import login_required
from util.sql_util import upsert_json
from flask import Blueprint, request
import time
from login.login import admin_login
import psycopg2  # Import psycopg2 for PostgreSQL database connection

# Adjusting the system path to include the parent directory
# This allows for the importation of modules from the parent directory
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

upload_lab_section = Blueprint("upload_lab_section", __name__)


@upload_lab_section.route("/upload_lab_section", methods=["POST"])
@login_required
def upload_lab_section_():
    """
    Uploads lab section details and associated student information from a CSV file, converting it to JSON,
    and then upserts this data into a PostgreSQL database.

    This endpoint requires a POST request with form data including a 'password' for database login, 'lab_section',
    'day_of_week', and 'start_time'. It also requires a file part with the CSV file containing student information.

    Returns:
        str: A response indicating the success or failure of the operation, along with appropriate HTTP status codes.
    """

    # Validate required form data
    if "password" not in request.form:
        return "password is required", 400
    password = request.form["password"]

    # Additional form data validations
    if "lab_section" not in request.form:
        return "lab_section is required", 400
    lab_section = request.form["lab_section"]

    if "day_of_week" not in request.form:
        return "day_of_week is required", 400
    day_of_week = request.form["day_of_week"]

    if "start_time" not in request.form:
        return "start_time is required", 400
    start_time = request.form["start_time"]

    # Establish database connection
    conn = admin_login(password)
    cursor = conn.cursor()

    # File part validation
    if "file" not in request.files:
        return "No file part in the request", 400
    file = request.files["file"]
    if file.filename == "":
        return "No selected file", 400

    # File processing and database upsert
    if file:
        temp_path = "./temp_uploaded_file.csv"
        file.save(temp_path)  # Save the file to a temporary file

        # Process the CSV and convert it to JSON for database insertion
        json_data = lab_csv_to_json(temp_path, lab_section, day_of_week, start_time)
        os.remove(temp_path)  # Cleanup: Remove the temporary file

        # Generate SQL for upsert and execute
        sql_call = upsert_json(json_data, "students_lab_section", "student_id")
        for query, value in zip(sql_call[0], sql_call[1]):
            try:
                cursor.execute(query, value)
            except psycopg2.DatabaseError as e:
                conn.rollback()  # Ensure atomicity on failure
                conn.close()
                return f"Database error: {e}", 500

            time.sleep(0.05)  # Brief pause to reduce database load

        conn.commit()  # Commit all changes
        conn.close()  # Close the database connection
        return "success", 200
