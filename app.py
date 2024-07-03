from datetime import date, datetime, timedelta
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import *

# Create a Flask application instance
app = Flask(__name__)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set response headers to prevent caching
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Route for the home page
@app.route("/")
def index():
    days_remaining = 0

    # Check if user is logged in
    if "user_id" in session.keys():
        # Get membership expiration date for the logged-in user
        membership = query("SELECT membership FROM users WHERE id = ?", [session["user_id"]])[0]["membership"]

        # If no membership, set days remaining to 0 and render home page
        if membership == 0:
            days_remaining = 0
            return render_template("home.html", days_remaining=days_remaining)

        # Convert membership expiration date to datetime object
        membership = datetime.strptime(str(membership), "%Y-%m-%d")

        # Calculate days remaining until membership expires
        current_date = datetime.now()
        days_remaining = (membership - current_date).days

    return render_template("home.html", days_remaining=days_remaining)

# Route for the membership page
@app.route("/membership", methods=["GET", "POST"])
def membership():
    # Define available membership options
    membership_options = [
        {"title": "Free 7-Day Membership", "days": 7, "description": "24/7 Access to all of our state of the art facilities for free for an entire week!"},
        {"title": "Monthly Agreement", "days": 30, "description": "Monthly access to all our state of the art facilities! Open from 7:00AM - 10:00PM daily"},
        {"title": "Yearly Agreement", "days": 365, "description": "Yearly access to all our state of the art facilities! Open 24/7"}
    ]

    if request.method == "POST":
        if request.form.get("membership"):
            membershipType = int(request.form.get("membership"))

            # Check if user already has a free pass
            if query("SELECT * FROM purchases WHERE order_id = ? AND order_type = 7", [session["user_id"]]) and membershipType == 7:
                flash("Only 1 free pass per customer!")
                return render_template("membership.html", membership_options=membership_options)

            # Record membership purchase in the database
            execute("INSERT INTO purchases (order_id, order_type, date) VALUES (?, ?, DATE())", (session["user_id"], membershipType))

            # Get current membership date for the user
            current_membership_date = query("SELECT membership FROM users WHERE id = ?", [session["user_id"]])[0]["membership"]

            # If no current membership, set new membership date
            if current_membership_date == 0:
                date_str = "+{} day".format(membershipType)
                execute("UPDATE users SET membership = DATE('now', ?) WHERE id = ?", (date_str, session["user_id"]))
                flash("Purchase successful!")
                return render_template("membership.html", membership_options=membership_options)

            # Calculate new membership expiration date
            current_membership_date = datetime.strptime(str(current_membership_date), "%Y-%m-%d")
            new_membership_date = current_membership_date + timedelta(days=membershipType)

            # Update membership date in the database
            execute("UPDATE users SET membership = ? WHERE id = ?", (new_membership_date.strftime("%Y-%m-%d"), session["user_id"]))

            flash("Purchase successful!")
            return render_template("membership.html", membership_options=membership_options)

    return render_template("membership.html", membership_options=membership_options)

# Route for the login page
@app.route("/login", methods=["GET", "POST"])
def login():
    # Clear session data
    session.clear()

    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Must provide username")
            return render_template("login.html")
        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Must provide password")
            return render_template("login.html")

        # Query database for username
        rows = query("SELECT * FROM users WHERE username = ?", [request.form.get("username")])

        # Check if username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash("Invalid username/password")
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    return render_template("login.html")

# Route for the registration page
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Must provide username")
            return render_template("register.html")
        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Must provide password")
            return render_template("register.html")
        # Ensure password confirmation was submitted
        elif not request.form.get("confirmation"):
            flash("Must re-enter password")
            return render_template("register.html")
        # Ensure passwords match
        elif request.form.get("password") != request.form.get("confirmation"):
            flash("Passwords must match")
            return render_template("register.html")

        # Check password strength
        alphas = []
        digits = []
        password = request.form.get("password")
        username = request.form.get("username")

        for i in range(len(password)):
            if password[i].isupper():
                alphas.append(password[i])
            if password[i].isdigit():
                digits.append(password[i])

        if not digits:
            flash("Password must have at least 1 non-alphabetic digit")
            return render_template("register.html")
        if not alphas:
            flash("Password must have at least 1 capital letter digit")
            return render_template("register.html")
        if len(password) < 8:
            flash("Password must be at least 8 characters long")
            return render_template("register.html")

        try:
            # Insert new user into the database
            execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, generate_password_hash(password)))
        except:
            flash("Username already in use")
            return render_template("register.html")

        flash("Account created successfully")
        return render_template("login.html")

    return render_template("register.html")

# Route for logging out
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
