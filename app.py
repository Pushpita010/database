from flask import Flask, render_template, request, redirect, session, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import config
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

# Track registered users in memory (fallback when DB not available)
registered_users = {}

# Helper function to get database connection


def get_db_connection():
    """Create a new database connection"""
    try:
        conn = mysql.connector.connect(
            host=config.MYSQL_HOST,
            user=config.MYSQL_USER,
            password=config.MYSQL_PASSWORD,
            database=config.MYSQL_DB
        )
        return conn
    except Error as e:
        print(f"Database connection error: {e}")
        return None

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

    # Then check registered users in memory
    if username in registered_users:
        user = registered_users[username]
        if check_password_hash(user['password'], password):
            return {"id": user['id'], "username": user['username'], "email": user['email']}

    # Then try database
    try:
        conn = get_db_connection()
        if not conn:
            return None

        cur = conn.cursor()
        cur.execute(
            "SELECT id, username, email, password FROM users WHERE username=%s", (username,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user and check_password_hash(user[3], password):
            return {"id": user[0], "username": user[1], "email": user[2]}
    except Exception as e:
        print(f"Database auth error: {e}")
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
        if username in registered_users or username in config.TEST_USERS:
            flash("Username already exists!", "error")
            return redirect(url_for("signup"))

        # Try database first
        try:
            cur = mysql.connection.cursor()
            cur.execute(
                "SELECT username FROM users WHERE username=%s", (username,))
            existing_user = cur.fetchone()

            if existing_user:
                flash("Username already exists!", "error")
                cur.close()
                return redirect(url_for("signup"))

            # If DB available, save to database
            hashed_password = generate_password_hash(password)
            cur.execute(
                "INSERT INTO users(username, email, password) VALUES(%s, %s, %s)",
                (username, email, hashed_password)
            )
            mysql.connection.commit()
            cur.close()

            flash("✅ Account created successfully! Please login now.", "success")
            return redirect(url_for("login"))

        except Exception as db_error:
            # If DB not available, save to memory
            try:
                hashed_password = generate_password_hash(password)
                registered_users[username] = {
                    "id": len(registered_users) + 1000,
                    "username": username,
                    "email": email,
                    "password": hashed_password
                }
                flash("✅ Account created successfully! Please login now.", "success")
                return redirect(url_for("login"))
            except Exception as e:
                flash("Error creating account. Please try again.", "error")
                return redirect(url_for("signup"))

    return render_template("signup.html")


@app.route("/dashboard")
@login_required
def dashboard():
    fullname = "User"
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT fullname FROM users WHERE username=%s",
                    (session["username"],))
        user_data = cur.fetchone()
        cur.close()
        fullname = user_data[0] if user_data and user_data[0] else "User"
    except:
        if session["username"] in registered_users:
            fullname = registered_users[session["username"]].get(
                "fullname", "User")

    return render_template("dashboard.html", username=session["username"], fullname=fullname)


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        fullname = request.form.get("fullname", "").strip()
        new_password = request.form.get("password", "").strip()
        old_password = request.form.get("old_password", "").strip()

        # Validate password change request
        if new_password:
            if not old_password:
                flash("❌ Please enter your current password to change it!", "error")
                return redirect(url_for("profile"))

            if len(new_password) < 6:
                flash("❌ New password must be at least 6 characters!", "error")
                return redirect(url_for("profile"))

            # Verify old password first (SECURITY: Always verify before allowing change)
            user = authenticate_user(session["username"], old_password)
            if not user:
                flash("❌ Current password is incorrect!", "error")
                return redirect(url_for("profile"))

        try:
            print(f"\n=== PROFILE UPDATE ===")
            print(f"Username: {session['username']}")
            print(f"New fullname: {fullname}")
            print(f"Changing password: {bool(new_password)}")

            conn = get_db_connection()
            if not conn:
                raise Exception("Database connection failed")

            cur = conn.cursor()
            print(f"Database cursor opened")

            if new_password:
                hashed_password = generate_password_hash(new_password)
                print(f"Executing UPDATE with password change")
                cur.execute(
                    "UPDATE users SET fullname=%s, password=%s WHERE username=%s",
                    (fullname, hashed_password, session["username"])
                )
            else:
                print(f"Executing UPDATE without password change")
                cur.execute(
                    "UPDATE users SET fullname=%s WHERE username=%s",
                    (fullname, session["username"])
                )

            print(f"Rows affected: {cur.rowcount}")
            conn.commit()
            print(f"✅ Commit successful")
            flash("✅ Profile updated successfully!", "success")
            cur.close()
            conn.close()
            print(f"=== END PROFILE UPDATE ===\n")
        except Exception as e:
            print(f"\n❌ Profile update error: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            print(f"=== END PROFILE UPDATE (ERROR) ===\n")
            # If DB not available, save to memory
            if session["username"] in registered_users:
                registered_users[session["username"]]["fullname"] = fullname
                if new_password:
                    registered_users[session["username"]]["password"] = generate_password_hash(
                        new_password)
                flash("✅ Profile updated successfully!", "success")
            else:
                flash("Error updating profile. Please try again.", "error")

    # Get current profile data
    profile_data = {"fullname": "", "email": session.get("email", "")}

    try:
        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT fullname, email FROM users WHERE username=%s", (session["username"],))
            user_data = cur.fetchone()
            cur.close()
            conn.close()

            if user_data:
                profile_data = {
                    "fullname": user_data[0] if user_data[0] else "",
                    "email": user_data[1] if user_data[1] else session.get("email", "")
                }
    except Exception as e:
        print(f"Profile GET error: {e}")
        if session["username"] in registered_users:
            profile_data = {
                "fullname": registered_users[session["username"]].get("fullname", ""),
                "email": registered_users[session["username"]].get("email", "")
            }

    return render_template("profile.html", profile=profile_data, username=session["username"])


@app.route("/grades")
@login_required
def grades():
    data = []
    total_marks = 0
    total_subjects = 0

    username = session.get("username", "")
    print(f"\n{'='*70}")
    print(f"GRADES REQUEST - Username: {username}")
    print(
        f"Session: user_id={session.get('user_id')}, username={session.get('username')}")

    try:
        print(f"[1] Creating database connection...")
        conn = get_db_connection()
        if not conn:
            raise Exception("Failed to create database connection")
        print(f"[1] ✅ Connected")

        print(f"[2] Executing grades query...")
        cur = conn.cursor()
        sql = "SELECT subject, marks FROM grades WHERE username=%s ORDER BY subject"
        print(f"    SQL: {sql}")
        print(f"    Param: ('{username}',)")

        cur.execute(sql, (username,))
        data = cur.fetchall()
        cur.close()
        conn.close()

        print(f"[3] ✅ Query executed successfully")
        print(f"    Rows returned: {len(data)}")

        if data:
            print(f"    Data found:")
            for subject, marks in data:
                print(f"       {subject}: {marks}")
            total_subjects = len(data)
            total_marks = sum(int(grade[1]) for grade in data)
            avg = total_marks / total_subjects if total_subjects > 0 else 0
            print(
                f"    Statistics: {total_subjects} subjects, total {total_marks}, avg {avg:.1f}")
            print(
                f"    Passing to template: total_marks={total_marks}, total_subjects={total_subjects}")
        else:
            print(f"    ⚠️  No grades found for user '{username}'")

    except Exception as e:
        print(f"[ERROR] {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        data = []

    print(f"[4] Rendering template with {len(data)} grade records")
    print(f"{'='*70}\n")

    return render_template("grades.html", grades=data, username=username,
                           total_marks=total_marks, total_subjects=total_subjects)


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
