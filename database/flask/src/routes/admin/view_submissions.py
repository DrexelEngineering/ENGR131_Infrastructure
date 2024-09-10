from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
import os
import sys
from flask import Blueprint
from flask_login import login_required

# Assuming the admin_login function establishes a connection to the database securely
from login.login import admin_login

get_submissions = Blueprint("get_submissions", __name__)


@get_submissions.route("/submissions", methods=["GET"])
@login_required
def get_submissions_():
    # Extract password from request headers
    password = request.headers.get("password")

    # Check if password is provided
    if not password:
        return jsonify({"error": "Password is required"}), 401

    # Extract query parameters
    query_params = request.args

    # Base SQL query
    base_query = "SELECT * FROM public.submissions"
    where_clauses = []
    query_values = []

    # Dynamically build WHERE clause based on query parameters
    for param, value in query_params.items():
        # Ensure the param corresponds to a valid column name to prevent SQL injection
        if param in [
            "submission_id",
            "original_file_name",
            "student_id",
            "assignment_id",
            "submitter_type",
            "total_score",
            "max_score",
            "percentage_score",
            "submission_time",
            "start_time",
            "end_time",
            "flag",
            "submission_mechanism",
        ]:
            where_clauses.append(f"{param} = %s")
            query_values.append(value)

    # Complete SQL query construction
    if where_clauses:
        sql_query = f"{base_query} WHERE {' AND '.join(where_clauses)}"
    else:
        sql_query = base_query

    # Connect to the database and execute the query
    with admin_login(
        password
    ) as conn:  # Assuming admin_login() uses context management for the connection
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(sql_query, query_values)
            submissions = cursor.fetchall()

    # Return the query results as JSON
    return jsonify(submissions)
