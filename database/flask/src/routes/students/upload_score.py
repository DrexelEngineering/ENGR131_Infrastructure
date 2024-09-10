import os
import re
import sys
from datetime import datetime, timedelta, timezone

from file_translators.assignment_reader import assignment_JSON
from flask import Blueprint, request
from flask_login import login_required
from login.login import student_login
from util.sql_util import commit_sql, insert_json

# Get the directory of your current script
current_dir = os.path.dirname(__file__)
# Go one folder back
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)


key = "7mPZKa3gJZn4ng0WJ5TsUmuQC2RK9XBAwTzrTEjbyB0="

upload_score = Blueprint("upload_score", __name__)
live_scorer = Blueprint("live_scorer", __name__)


@upload_score.route("/upload_score", methods=["POST"])
@login_required
def upload_score_():
    # Check for assignmentName in the form data
    if "password" not in request.form:
        return "password is required", 400
    password = request.form["password"]

    conn = student_login(password)
    cursor = conn.cursor()

    # Check if the request has the file part
    if "file" not in request.files:
        return "No file part in the request", 400
    file = request.files["file"]

    # Check for assignmentName in the form data
    if "student_id" not in request.form:
        return "student_id is required", 400
    student_id = request.form["student_id"]

    # Check for original_file_name  in the form data
    if "original_file_name" not in request.form:
        return "original_file_name is required", 400
    original_file_name = request.form["original_file_name"]

    # Check for assignmentID in the form data
    if "assignment_id" not in request.form:
        return "assignment_name is required", 400
    else:
        assignment_id = request.form["assignment_id"]

    if "submission_mechanism" in request.form:
        submission_mechanism = request.form["submission_mechanism"]
    else:
        submission_mechanism = "file_upload"

    # Check if the request has the file part
    if "log_file" in request.form:
        log_info = request.form["log_file"]
    else:
        log_info = "None"

    # If the user does not select a file, the browser submits an empty file without a filename
    if file.filename == "":
        return "No selected file", 400

    if file:
        # Save the file to a temporary file
        temp_path = "./temp_uploaded_file.JSON"
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

        percentage_score = (total_score / max_score) * 100

        dict = [
            {
                "submission_id": f"{student_id}_{assignment_id}_{formatted_date_time}",
                "student_id": student_id,
                "assignment_id": assignment_id,
                "submitter_type": "student",
                "total_score": total_score,
                "max_score": max_score,
                "percentage_score": percentage_score,
                "original_file_name": original_file_name,
                "submission_mechanism": submission_mechanism,
                "logfile": log_info,
            }
        ]

        if "start_time" in request.form:
            dict[0]["start_time"] = request.form["start_time"]

        if "end_time" in request.form:
            dict[0]["end_time"] = request.form["end_time"]

        if "flag" in request.form:
            dict[0]["flag"] = request.form["flag"]

        print(dict)

        sql_call = insert_json(dict, "submissions")
        out = commit_sql(cursor, sql_call)
        if not out:
            conn.rollback()  # Rollback in case of failure
            conn.close()
            return "Error occurred during SQL execution", 500

        ############################## QUESTION SCORE ##############################

        dict = []

        for data in json_extracted:
            dict.append(
                {
                    "submission_id": f"{student_id}_{assignment_id}_{formatted_date_time}",
                    "assignment_id": assignment_id,
                    "question_id": data.get("question_id"),
                    "student_id": student_id,
                    "score": data.get("score", 0),
                    "max_score": data.get("max_score", 0),
                    "output": data.get("output", "NA"),
                    "visible": data.get("visibility", True),
                }
            )

        sql_call = insert_json(dict, "question_score")
        out = commit_sql(cursor, sql_call)
        if not out:
            conn.rollback()  # Rollback in case of failure
            conn.close()
            return "Error occurred during SQL execution", 500

        conn.commit()
        # need to add the sql call here
        conn.close()
        return "success"


@live_scorer.route("/live_scorer", methods=["POST"])
@login_required
def live_scorer_():
    # Retrieve JSON data from request
    if not request.json:
        return "Request must be in JSON format", 400

    # Extract 'password' and 'data' from the JSON payload
    password = request.json.get("password")
    if not password:
        return "password is required", 400

    data_ = request.json.get("data")
    if data_ is None:
        return "Data payload is missing", 400

    conn = student_login(password)
    cursor = conn.cursor()

    # Get the current UTC time
    now_utc = datetime.now(timezone.utc)

    # East Coast of the United States is typically UTC-5, but during Daylight Saving Time it's UTC-4
    # Checking if it's Daylight Saving Time
    east_coast_time = now_utc - timedelta(hours=4 if now_utc.dst() else 5)

    # Format the date and time in a nice string format
    formatted_date_time = east_coast_time.strftime("%Y-%m-%d %H:%M:%S")

    json_extracted = []

    for data in data_:
        json_extracted.append(
            {
                "submission_id": f'{data["student_id"]}_{data["assignment_id"]}_{data["question_id"]}_{formatted_date_time}',
                "student_id": data["student_id"],
                "assignment_id": data["assignment_id"],
                "question_id": data["question_id"],
                "submitter_type": "student",
                "score": data.get("score", 0),
                "max_score": data.get("max_score", 0),
                "student_response": data.get("student_response", "NA"),
                "ip_address": data.get("ip_address", "NA"),
                "hostname": data.get("hostname", "NA"),
                "jupyter_user": data.get("JupyterUSER", "NA"),
                "response_time": formatted_date_time,
            }
        )

    sql_call = insert_json(json_extracted, "live_submissions")
    out = commit_sql(cursor, sql_call)
    if not out:
        conn.rollback()  # Rollback in case of failure
        conn.close()
        return "Error occurred during SQL execution", 500

    conn.commit()
    # need to add the sql call here
    conn.close()
    return "responses successfully uploaded to database"


def is_string_number_combo(s):
    pattern = r"^[A-Za-z]+_[0-9]+$"
    return bool(re.match(pattern, s))


def extract_string_number(s):
    pattern = r"^([A-Za-z]+)_([0-9]+)$"
    match = re.match(pattern, s)
    if match:
        return match.group(1), int(match.group(2))
