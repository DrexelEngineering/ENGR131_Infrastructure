import os
import sys
import argparse

# Get the directory of your current script
current_dir = os.path.dirname(__file__)

# Go one folder back
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

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

app = Flask(__name__)
app.register_blueprint(upload_students)
app.register_blueprint(upload_assignment)
app.register_blueprint(upload_score)
app.register_blueprint(upload_lab_section)

# Builds the login manager
login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = 'fBLwqnX5PCJVQtDcicLzUPYu7uU' # Set a secret key for security purposes
# Set the session to be permanent and expire after 1 hour
app.permanent_session_lifetime = timedelta(hours=1)

# User model
class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


def initialize_database():
    conn = admin_login(password)
    cursor = conn.cursor()
    
    cursor.execute("GRANT INSERT on ALL TABLES IN SCHEMA public TO student")
    conn.commit()
    conn.close()
                
################### LOGIN ROUTES ####################

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    # Clear all data from the session
    session.clear()
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and check_password_hash(users[username]['password'], password):
            user = User(username)
            # Set the session as permanent to apply the custom duration
            session.permanent = True
            login_user(user)
            return redirect(url_for('index'))
        
        # If the user doesn't exist or password is wrong, reload the page with an error message
        flash('Invalid username/password combination')
    
    # If the request method is GET, just render the login template    
    return render_template('login.html') # Create a login.html template

@app.route('/')
@login_required
def index():
    return "You are now logged in!"

@app.route('/logout')
def logout():
    logout_user()
    flash('You have logged out successfully')
    return redirect(url_for('login'))

def parse_arguments():
    parser = argparse.ArgumentParser(description='gets the password for the database')
    parser.add_argument('password', type=str, help='The admin password for the database')
    parser.add_argument('port', type=int, help='gets the port to start the server on')
    return parser.parse_args()

# runs on gunicorn call
if not __name__ == '__main__':
    password = os.environ.get('DATABASE_PASSWORD')
    users = {'admin': {'password': generate_password_hash(password)}}
    initialize_database()
    
if __name__ == '__main__':
    args = parse_arguments()
    password = args.password
    port = args.port
    # Replace with your user handling logic
    users = {'admin': {'password': generate_password_hash(password)}}
    initialize_database()
    app.run(debug=True)
