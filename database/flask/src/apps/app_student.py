import argparse
import os
import sys
from datetime import timedelta

from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from routes.students.upload_score import live_scorer, upload_score
from werkzeug.security import check_password_hash, generate_password_hash

# Get the directory of your current script
current_dir = os.path.dirname(__file__)
# Go one folder back
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)


app = Flask(__name__)
app.register_blueprint(upload_score)
app.register_blueprint(live_scorer)

# Builds the login manager
login_manager = LoginManager()
login_manager.init_app(app)

# Set a secret key for security purposes
try:
    app.secret_key = os.environ["STUDENT_SECRET_KEY"]
except KeyError:
    print("STUDENT_SECRET_KEY environment variable not found")

# Set the session to be permanent and expire after 1 hour
app.permanent_session_lifetime = timedelta(hours=5)


# User model
class User(UserMixin):
    def __init__(self, id):
        self.id = id


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


################### LOGIN ROUTES ####################


@app.route("/login", methods=["GET", "POST"])
def login():
    # Clear all data from the session
    session.clear()

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users and check_password_hash(
            users[username]["password"], password
        ):
            user = User(username)
            # Set the session as permanent to apply the custom duration
            session.permanent = True
            login_user(user)
            return redirect(url_for("index"))

        # If the user doesn't exist or password is wrong, reload the page with an error message
        flash("Invalid username/password combination")

    # If the request method is GET, just render the login template
    return render_template("login.html")  # Create a login.html template


@app.route("/")
@login_required
def index():
    return "You are now logged in!"


@app.route("/logout")
def logout():
    logout_user()
    flash("You have logged out successfully")
    return redirect(url_for("login"))


def parse_arguments():
    parser = argparse.ArgumentParser(description="gets the password for the database")
    parser.add_argument(
        "password", type=str, help="The student password for the database"
    )
    parser.add_argument("port", type=int, help="gets the port to start the server on")
    return parser.parse_args()


# runs on gunicorn call
if not __name__ == "__main__":
    password = os.environ.get("DATABASE_PASSWORD")
    users = {"student": {"password": generate_password_hash(password)}}

if __name__ == "__main__":
    args = parse_arguments()
    password = args.password
    port = args.port
    # Replace with your user handling logic
    users = {"student": {"password": generate_password_hash(password)}}
    app.run(debug=True, port=port)
