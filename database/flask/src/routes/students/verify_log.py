# import os
# import sys
# import re
# from datetime import datetime, timezone, timedelta

# # Get the directory of your current script
# current_dir = os.path.dirname(__file__)
# # Go one folder back
# parent_dir = os.path.dirname(current_dir)
# sys.path.append(parent_dir)

# from flask import Blueprint, request
# from flask_login import login_required
# from login.login import student_login

# verify_log_file = Blueprint('verify_log_file', __name__)

# @verify_log_file.route('/verify_log_file', methods=['POST'])
# @login_required
# def live_scorer_():

#     # Retrieve JSON data from request
#     if not request.json:
#         return 'Request must be in JSON format', 400

#     # Extract 'password' and 'data' from the JSON payload
#     password = request.json.get('password')
#     if not password:
#         return 'password is required', 400

#     data_ = request.json.get('data')
#     if data_ is None:
#         return 'Data payload is missing', 400

#     conn = student_login(password)
#     cursor = conn.cursor()

#     # Get the current UTC time
#     now_utc = datetime.now(timezone.utc)

#     # East Coast of the United States is typically UTC-5, but during Daylight Saving Time it's UTC-4
#     # Checking if it's Daylight Saving Time
#     east_coast_time = now_utc - timedelta(hours=4 if now_utc.dst() else 5)

#     # Format the date and time in a nice string format
#     formatted_date_time = east_coast_time.strftime("%Y-%m-%d %H:%M:%S")

#     json_extracted = []

#     for data in data_:
#         json_extracted.append({
#             "submission_id": f'{data["student_id"]}_{data["assignment_id"]}_{data["question_id"]}_{formatted_date_time}',
#             "student_id": data["student_id"],
#             "assignment_id": data["assignment_id"],
#             "question_id": data["question_id"],
#             "submitter_type": "student",
#             "score": data.get('score', 0),
#             "max_score": data.get('max_score', 0),
#             "student_response": data.get('student_response', "NA"),
#             "ip_address": data.get('ip_address', "NA"),
#             "hostname": data.get('hostname', "NA"),
#             "jupyter_user": data.get('JupyterUSER', "NA"),
#             "response_time": formatted_date_time,
#         })

#     sql_call = insert_json(json_extracted, 'live_submissions')
#     out = commit_sql(cursor, sql_call)
#     if not out:
#         conn.rollback()  # Rollback in case of failure
#         conn.close()
#         return "Error occurred during SQL execution", 500

#     conn.commit()
#     # need to add the sql call here
#     conn.close()
#     return "responses successfully uploaded to database"

# def is_string_number_combo(s):
#     pattern = r'^[A-Za-z]+_[0-9]+$'
#     return bool(re.match(pattern, s))

# def extract_string_number(s):
#     pattern = r'^([A-Za-z]+)_([0-9]+)$'
#     match = re.match(pattern, s)
#     if match:
#         return match.group(1), int(match.group(2))
