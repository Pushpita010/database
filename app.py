from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import config

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

# MySQL config
app.config["MYSQL_HOST"] = config.MYSQL_HOST
app.config["MYSQL_USER"] = config.MYSQL_USER
app.config["MYSQL_PASSWORD"] = config.MYSQL_PASSWORD
app.config["MYSQL_DB"] = config.MYSQL_DB

mysql = MySQL(app)

# Decorator for login required
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please login first!", "error")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

# Helper function to authenticate user with test users
def authenticate_user(username, password):
    """
    Authenticate user against test users or database.
    Returns user data if authentication successful, None otherwise.
    """
    # First check test users
    if username in config.TEST_USERS:
        if config.TEST_USERS[username] == password:
            return {"id": hash(username) % 10000, "username": username, "email": username}
    
    # Then check database
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, username, email, password FROM users WHERE username=%s", (username,))
        user = cur.fetchone()
        cur.close()
        
        if user and check_password_hash(user[3], password):
            return {"id": user[0], "username": user[1], "email": user[2]}
    except:
        pass
    
    return None

@app.route("/", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        
        if not username or not password:
            flash("Username and password are required!", "error")
            return redirect(url_for("login"))
        
        user = authenticate_user(username, password)
        
        if user:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["email"] = user.get("email", "")
            flash(f"Welcome back, {username}!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password!", "error")
    
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        confirm_password = request.form.get("confirm_password", "").strip()
        
        # Validation
        if not username or not email or not password:
            flash("All fields are required!", "error")
            return redirect(url_for("signup"))
        
        if len(username) < 3:
            flash("Username must be at least 3 characters!", "error")
            return redirect(url_for("signup"))
        
        if len(password) < 6:
            flash("Password must be at least 6 characters!", "error")
            return redirect(url_for("signup"))
        
        if password != confirm_password:
            flash("Passwords do not match!", "error")
            return redirect(url_for("signup"))
        
        # Check if username already exists
        cur = mysql.connection.cursor()
        cur.execute("SELECT username FROM users WHERE username=%s", (username,))
        existing_user = cur.fetchone()
        
        if existing_user:
            flash("Username already exists!", "error")
            cur.close()
            return redirect(url_for("signup"))
        
        # Hash password and insert user
        hashed_password = generate_password_hash(password)
        
        try:
            cur.execute(
                "INSERT INTO users(username, email, password) VALUES(%s, %s, %s)",
                (username, email, hashed_password)
            )
            mysql.connection.commit()
            flash("Account created successfully! Please login.", "success")
            cur.close()
            return redirect(url_for("login"))
        except Exception as e:
            mysql.connection.rollback()
            flash("Error creating account. Please try again.", "error")
            cur.close()
            return redirect(url_for("signup"))
    
    return render_template("signup.html")

@app.route("/dashboard")
@login_required
def dashboard():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT fullname FROM users WHERE username=%s", (session["username"],))
        user_data = cur.fetchone()
        cur.close()
        
        fullname = user_data[0] if user_data and user_data[0] else "User"
    except:
        fullname = "User"
    
    return render_template("dashboard.html", username=session["username"], fullname=fullname)

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        fullname = request.form.get("fullname", "").strip()
        new_password = request.form.get("password", "").strip()
        
        try:
            cur = mysql.connection.cursor()
            
            if new_password:
                if len(new_password) < 6:
                    flash("Password must be at least 6 characters!", "error")
                    cur.close()
                    return redirect(url_for("profile"))
                
                hashed_password = generate_password_hash(new_password)
                cur.execute(
                    "UPDATE users SET fullname=%s, password=%s WHERE username=%s",
                    (fullname, hashed_password, session["username"])
                )
            else:
                cur.execute(
                    "UPDATE users SET fullname=%s WHERE username=%s",
                    (fullname, session["username"])
                )
            
            mysql.connection.commit()
            flash("Profile updated successfully!", "success")
            cur.close()
        except Exception as e:
            flash("Error updating profile. Please try again.", "error")
    
    # Get current profile data
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT fullname, email FROM users WHERE username=%s", (session["username"],))
        user_data = cur.fetchone()
        cur.close()
        
        profile_data = {
            "fullname": user_data[0] if user_data and user_data[0] else "",
            "email": user_data[1] if user_data and user_data[1] else session.get("email", "")
        }
    except:
        profile_data = {"fullname": "", "email": session.get("email", "")}
    
    return render_template("profile.html", profile=profile_data, username=session["username"])

@app.route("/grades")
@login_required
def grades():
    try:
        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT subject, marks FROM grades WHERE username=%s ORDER BY subject",
            (session["username"],)
        )
        data = cur.fetchall()
        cur.close()
    except:
        data = []
    
    return render_template("grades.html", grades=data, username=session["username"])

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out successfully!", "success")
    return redirect(url_for("login"))

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(debug=config.DEBUG, host="127.0.0.1", port=5000)
