import os
import sys

from file_translators.assignment_reader import assignment_JSON
from flask import Blueprint, request
from flask_login import login_required
from login.login import admin_login
from util.sql_util import commit_sql, upsert_json

from ...util.string_util import extract_string_number, is_string_number_combo

# Adjusting the system path to include the parent directory for relative imports
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

upload_assignment = Blueprint("upload_assignment", __name__)


@upload_assignment.route("/upload_assignment", methods=["POST"])
@login_required
def upload_students_():
    """
    Uploads an assignment and its associated questions to the database.

    Validates the incoming request for required fields ('password', 'assignment_name', 'assignment_id', and 'file'),
    parses the uploaded JSON file for assignment details, and inserts or updates the assignment and question records
    in the database.

    Requires user authentication.

    Returns:
        str: A message indicating the result of the operation. Returns HTTP status code 400 for client errors
            and 500 for server-side SQL execution errors.
    """

    # Validation for required form data 'password'
    if "password" not in request.form:
        return "password is required", 400
    password = request.form["password"]

    # Establish a database connection as an admin
    conn = admin_login(password)
    cursor = conn.cursor()

    # Validation for the file part in the request
    if "file" not in request.files:
        return "No file part in the request", 400
    file = request.files["file"]

    # Validation for 'assignment_name' in form data
    if "assignment_name" not in request.form:
        return "assignment_name is required", 400
    assignment_name = request.form["assignment_name"]

    # Validation and parsing for 'assignment_id' in form data
    if "assignment_id" not in request.form:
        return "assignment_name is required", 400
    else:
        assignment_id = request.form["assignment_id"]
        if is_string_number_combo(assignment_id):
            assignment_type, assignment_num = extract_string_number(assignment_id)
        else:
            return (
                "assignment_id must be a string-number combo in the format AssignmentType_AssignmentNumber",
                400,
            )

    # Check for empty filename submission
    if file.filename == "":
        return "No selected file", 400

    if file:
        # Process the uploaded file
        temp_path = "./temp_uploaded_file.JSON"
        file.save(temp_path)
        json_extracted = assignment_JSON(temp_path)
        os.remove(temp_path)  # Clean up by removing the temporary file

        # Preparing data for insertion into the 'assignments' table
        assignment_data = [
            {
                "assignment_name": assignment_name,
                "assignment_id": assignment_id,
                "assignment_type": assignment_type,
                "assignment_num": assignment_num,
            }
        ]

        # Insert or update assignment record
        sql_call = upsert_json(assignment_data, "assignments", "assignment_id")
        if not commit_sql(cursor, sql_call):
            conn.rollback()  # Rollback and close connection on failure
            conn.close()
            return "Error occurred during SQL execution", 500

        question_data = []
        # Parsing each question from the JSON and preparing data for insertion
        for data in json_extracted:
            question_data.append(
                {
                    "question_id": data.get("question_id", ""),
                    "assignment_id": assignment_id,
                    "question_name": data.get("questions_name", ""),
                    "max_score": data.get("max_score", ""),
                    "visible": data.get("visibility", ""),
                }
            )

        # Insert or update question records
        sql_call = upsert_json(
            question_data, "questions", ["assignment_id", "question_id"]
        )
        if not commit_sql(cursor, sql_call):
            conn.rollback()  # Rollback and close connection on failure
            conn.close()
            return "Error occurred during SQL execution", 500

        # Commit transactions and close the connection
        conn.commit()
        conn.close()
        return "success"
