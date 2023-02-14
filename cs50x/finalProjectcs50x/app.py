from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session,url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import smtplib
from email.mime.text import MIMEText
import datetime
import re
from email.message import EmailMessage


# Configure application
app = Flask(__name__)

# Requires that "Less secure app access" be on
# https://support.google.com/accounts/answer/6010255
app.config["MAIL_DEFAULT_SENDER"] = "MAIL_DEFAULT_SENDER"
app.config["MAIL_PASSWORD"] ="MAIL_PASWORD"
app.config["MAIL_PORT"] = 587
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = 'TODOs'



# Ensure templates are auto-reloaded return jsonify({ 'status': 'success' })
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



db.execute("CREATE TABLE IF NOT EXISTS todo (id INTEGER PRIMARY KEY, task TEXT,complete INTEGER, user_id INTEGER)")
db.execute("CREATE TABLE IF NOT EXISTS verification(id INTEGER PRIMIMARY KEY, email TEXT,code INTEGER)")


@app.route("/")
def index():
    """show index"""
    return render_template("index.html")


@app.route("/signup", methods=["GET","POST"])
def signup():
    """signup"""
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password",default="password")
        confirmation = request.form.get("confirmation")

        # Check if username, email, password, or confirmation are missing
        if None in (username, email, password, confirmation):
         flash("All fields are required")
         return render_template("signup.html")


         # Check if the email address is valid
        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash("Invalid email address")
            return render_template("signup.html")

        # Check if the password is at least 8 characters long and contains at least one uppercase letter, one lowercase letter, and one number
        if len(password) < 8 or not any(char.isupper() for char in password) or not any(char.islower() for char in password) or not  not re.search(r'[^a-zA-Z0-9]', password):
            flash("The password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one number.")
            return render_template("signup.html")

        # Check if password and confirmation do not match
        if password != confirmation:
            flash ("your passwords do not match")
            return render_template("signup.html")

        #check if the username exists
        user = db.execute("SELECT * FROM users WHERE username = ?", username)
        if user:
            flash("The username already exists")
            return render_template("signup.html")
        #check if the email  exists
        email_check = db.execute("SELECT * FROM users WHERE email = ?", email)
        if email_check:
            flash("You have already signed up with this email")
            return render_template("signup.html")

        #generate password hash and insert the user into the database
        hash = generate_password_hash(password)
        db.execute("INSERT INTO users (username, email, hash) VALUES(?, ?, ?)", username, email, hash)

        # Set up the email message
        msg = EmailMessage
        msg = MIMEText("You've successfully signed up for your account feel free to plan your day")
        msg['Subject'] = 'Email Address Confirmation'
        msg['From'] = 'todosteam510@gmail.com'
        msg['To'] = email
        # Connect to the Gmail SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        # Log in to the server using the email address and password
        server.login('todosteam510@gmail.com', 'ggbbpuhtothdzocq')
        # Send the email
        server.send_message(msg)
        server.quit()

        return render_template("/login.html")

    else:
        return render_template("signup.html")




@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")

        #ensure the username and password are submitted
        if None in (username, password,email):
            flash("All fields are required")
            return render_template("login.html")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            flash("invalid username or password")
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return render_template("/tasks.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")


@app.route("/tasks")
def tasks():


    # Make sure user is logged in
    if "user_id" not in session:
        return redirect("/login")


    # retrieve all tasks from the database
    tasks = db.execute("SELECT * FROM todo WHERE user_id = ?",session["user_id"])

    # render the tasks template, passing the tasks as a parameter
    return render_template("tasks.html", tasks=tasks)


@app.route("/addtask", methods=["POST", "GET"])
def addtask():
  # get the task from the form submission
  task = request.form.get("task")
  today = datetime.datetime.now().strftime('%Y-%m-%d')
  # add the task to the database
  db.execute("INSERT INTO todo (task, user_id,date) VALUES (?,?.?)",task, session["user_id"],today)

  # redirect to the tasks page
  return redirect("/tasks")


@app.route("/delete/<int:item_id>",methods=["POST", "GET"])
def delete(item_id):
    # code to delete item goes here
    db.execute("DELETE FROM todo WHERE id = ?", item_id)
    return redirect("/tasks")

@app.route("/update/<int:item_id>", methods=['POST','GET'])
def update(item_id):
    completed = 0 if request.form.get("update")== 'on' else 1
    db.execute("UPDATE todo SET completed = ? WHERE id = ?", completed, item_id)
    return redirect("/tasks")


