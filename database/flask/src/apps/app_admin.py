import os
import sys
import argparse
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask import session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import psycopg2
import psycopg2.extras
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
from routes.admin.upload_students import upload_students
from routes.admin.upload_labsection import upload_lab_section
from routes.admin.upload_assignments import upload_assignment
from routes.admin.upload_score import upload_score
from login.login import admin_login


# Get the directory of your current script
current_dir = os.path.dirname(__file__)

# Go one folder back
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Initialize the Flask app
app = Flask(__name__)

# Register the blueprints
app.register_blueprint(upload_students)
app.register_blueprint(upload_assignment)
app.register_blueprint(upload_score)
app.register_blueprint(upload_lab_section)

# Builds the login manager
login_manager = LoginManager()
login_manager.init_app(app)

# TODO: Put this in a secret
# Set a secret key for security purposes
app.secret_key = "fBLwqnX5PCJVQtDcicLzUPYu7uU"

# Set the session to be permanent and expire after 1 hour
app.permanent_session_lifetime = timedelta(hours=1)


# User model
class User(UserMixin):
    """User class

    Args:
        UserMixin (obj): UserMixin object from flask_login
    """

    def __init__(self, id):
        """init method

        Args:
            id (str): User id
        """
        self.id = id


@login_manager.user_loader
def load_user(user_id):
    """function to load the user

    Args:
        user_id (str): User id name

    Returns:
        obj: UserMixin object
    """
    return User(user_id)


def initialize_database():
    """Initializes the database"""

    # Connect to the database
    conn = admin_login(password)
    cursor = conn.cursor()

    # Creates rights to fhe student user to the tables
    cursor.execute("GRANT INSERT on ALL TABLES IN SCHEMA public TO student")

    # commits the changes
    conn.commit()

    # Close the connection
    conn.close()


################### LOGIN ROUTES ####################


@app.route("/login", methods=["GET", "POST"])
def login():
    """login function

    Returns:
        url: URL to the login page
    """

    # Clear all data from the session
    session.clear()

    # If the request method is POST, get the username and password from the form
    if request.method == "POST":
        # Get the username and password from the form
        username = request.form["username"]
        password = request.form["password"]

        # Check if the user exists and the password is correct
        if username in users and check_password_hash(
            users[username]["password"], password
        ):
            # Create a user object
            user = User(username)

            # Set the session as permanent to apply the custom duration
            session.permanent = True
            login_user(user)

            # Redirect to the index page
            return redirect(url_for("index"))

        # If the user doesn't exist or password is wrong, reload the page with an error message
        flash("Invalid username/password combination")

    # If the request method is GET, just render the login template
    return render_template("login.html")  # Create a login.html template


@app.route("/")
@login_required
def index():
    """Route for login

    Returns:
        str: string message that verifies the login
    """
    return "You are now logged in!"


@app.route("/logout")
def logout():
    """logout function

    Returns:
        url: URL for the logout page
    """

    # Clear all data from the session
    logout_user()

    # Redirect to the login page
    flash("You have logged out successfully")
    return redirect(url_for("login"))


def parse_arguments():
    """parses the arguments to the function

    Returns:
        obj: collection of parsed arguments
    """

    # Create the parser
    parser = argparse.ArgumentParser(description="gets the password for the database")

    # Add the arguments
    parser.add_argument(
        "password", type=str, help="The admin password for the database"
    )
    parser.add_argument("port", type=int, help="gets the port to start the server on")
    parser.add_argument(
        "debug", type=bool, default=False, help="gets the debug mode for the server"
    )

    # returns the parser
    return parser.parse_args()


# runs on gunicorn call
if not __name__ == "__main__":
    """function that runs on gunicorn call
    """
    # gets the password from the environment
    password = os.environ.get("DATABASE_PASSWORD")

    # hashes the password and saves it to the users
    users = {"admin": {"password": generate_password_hash(password)}}

    # calls the initialize database function
    initialize_database()

if __name__ == "__main__":
    """main function
    """

    # Parse the arguments
    args = parse_arguments()

    # Get the password and port from the arguments
    password = args.password
    port = args.port

    # Generate the password hash
    users = {"admin": {"password": generate_password_hash(password)}}

    # Initialize the database
    initialize_database()

    # runs the application
    app.run(debug=args.debug)
