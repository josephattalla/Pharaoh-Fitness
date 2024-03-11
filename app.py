# Import necessary modules
import os
from datetime import date, datetime, timedelta
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash


# Configure application
app = Flask(__name__)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///gym.db")


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():

    days_remaining = 0

    # if logged in
    if "user_id" in session:
        membership = db.execute("SELECT membership FROM users WHERE id = ?", session["user_id"])[0]["membership"]

        # if membership is 0 in sql
        if membership == 0:
            days_remaining = 0
            return render_template("home.html", days_remaining=days_remaining)

        # Parse the membership expiration date from the database
        membership = datetime.strptime(str(membership), "%Y-%m-%d")

        # Calculate the number of days remaining in the membership
        current_date = datetime.now()
        days_remaining = (membership - current_date).days


    return render_template("home.html", days_remaining=days_remaining)



@app.route("/membership", methods=["GET", "POST"])
def membership():

    # membership options for html
    membership_options = [
        {"title": "Free 7-Day Membership", "days": 7, "description": "24/7 Access to all of our state of the art facilities for free for an entire week!"},
        {"title": "Monthly Agreement", "days": 30, "description": "Monthly access to all our state of the art facilities! Open from 7:00AM - 10:00PM daily"},
        {"title": "Yearly Agreement", "days": 365, "description": "Yearly access to all our state of the art facilities! Open 24/7"}
    ]

    if request.method == "POST":
        if request.form.get("membership"):
            membershipType = int(request.form.get("membership"))

            # Check if the user already purchased 7 Day
            if db.execute("SELECT * FROM purchases WHERE order_id = ? AND order_type = 7", session["user_id"]) and membershipType == 7:
                flash("Only 1 free pass per customer!")
                return render_template("membership.html", membership_options=membership_options)

            # Insert a new purchase record
            db.execute("INSERT INTO purchases (order_id, order_type, date) VALUES (?, ?, DATE())", session["user_id"], membershipType)

            # Get the current membership date from the user's record
            current_membership_date = db.execute("SELECT membership FROM users WHERE id = ?", session["user_id"])[0]["membership"]

            # If current date is 0 create string to use in sql that adds to the date the membership type
            if current_membership_date == 0:
                date_str = "+{} day".format(membershipType)
                db.execute("UPDATE users SET membership = DATE('now', ?) WHERE id = ?", date_str, session["user_id"])
                flash("Purchase successful!")
                return render_template("home.html")

            # Parse the current membership date and calculate the new membership end date
            current_membership_date = datetime.strptime(str(current_membership_date), "%Y-%m-%d")
            new_membership_date = current_membership_date + timedelta(days=membershipType)

            # Update the user's membership date to the new end date
            db.execute("UPDATE users SET membership = ? WHERE id = ?", new_membership_date.strftime("%Y-%m-%d"), session["user_id"])

            flash("Purchase successful!")
            return render_template("membership.html", membership_options=membership_options)

    return render_template("membership.html", membership_options=membership_options)



# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()  # Clear any previous user session data

    # Check if the request method is POST (when the user submits the login form)
    if request.method == "POST":
        # Ensure username and password are provided in the form
        if not request.form.get("username"):
            flash("Must provide username")  # Flash an error message
            return render_template("login.html")  # Render the login template again with an error message
        elif not request.form.get("password"):
            flash("Must provide password")  # Flash an error message
            return render_template("login.html")  # Render the login template again with an error message

        # Query the database to find the user with the provided username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure there is exactly one user with the provided username and the password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash("Invalid username/password")  # Flash an error message if the credentials are invalid
            return render_template("login.html")  # Render the login template again with an error message

        # If the credentials are valid, store the user's ID in the session to keep them logged in
        session["user_id"] = rows[0]["id"]

        # Redirect the user to the home page after successful login
        return redirect("/")  # Redirect user to home page

    # If the request method is GET, render the login template to display the login form
    return render_template("login.html")


# Registration route
@app.route("/register", methods=["GET", "POST"])
def register():
    # Check if the request method is POST (when the user submits the registration form)
    if request.method == "POST":
        # Validate user input from the registration form
        if not request.form.get("username"):
            flash("Must provide username")  # Flash an error message if username is missing
            return render_template("register.html")  # Render the registration template with an error message
        elif not request.form.get("password"):
            flash("Must provide password")  # Flash an error message if password is missing
            return render_template("register.html")  # Render the registration template with an error message
        elif not request.form.get("confirmation"):
            flash("Must re-enter password")  # Flash an error message if password confirmation is missing
            return render_template("register.html")  # Render the registration template with an error message
        elif request.form.get("password") != request.form.get("confirmation"):
            flash("Passwords must match")  # Flash an error message if passwords do not match
            return render_template("register.html")  # Render the registration template with an error message

        # Validate password complexity requirements
        alphas = []  # List to store uppercase letters in the password
        digits = []  # List to store digits in the password
        password = request.form.get("password")  # Get the password from the form
        username = request.form.get("username")  # Get the username from the form

        # Iterate through the characters in the password
        for i in range(len(password)):
            if password[i].isupper():
                alphas.append(password[i])  # Add uppercase letters to the alphas list
            if password[i].isdigit():
                digits.append(password[i])  # Add digits to the digits list

        # Validate password complexity requirements
        if not digits:
            flash("Password must have at least 1 non-alphabetic digit")  # Flash an error message if no digits are present
            return render_template("register.html")  # Render the registration template with an error message
        if not alphas:
            flash("Password must have at least 1 capital letter digit")  # Flash an error message if no uppercase letters are present
            return render_template("register.html")  # Render the registration template with an error message
        if len(password) < 8:
            flash("Password must be at least 8 characters long")  # Flash an error message if password length is less than 8 characters
            return render_template("register.html")  # Render the registration template with an error message

        # Attempt to insert the new user into the database
        try:
            db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)", username, generate_password_hash(password))  # Hash the password before storing it in the database

        except:
            flash("Username already in use")  # Flash an error message if the username is already in the database
            return render_template("register.html")  # Render the registration template with an error message

        flash("Account created successfully")  # Flash a success message
        return render_template("login.html")  # Render the login template to allow the user to log in after registration

    # If the request method is GET, render the registration template to display the registration form
    return render_template("register.html")


# Logout route
@app.route("/logout")
def logout():
    session.clear()  # Forget any user_id
    return redirect("/")  # Redirect