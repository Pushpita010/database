from flask import Flask, render_template, request, redirect, session
from flask_mysqldb import MySQL
import config

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

# MySQL config
app.config["MYSQL_HOST"] = config.MYSQL_HOST
app.config["MYSQL_USER"] = config.MYSQL_USER
app.config["MYSQL_PASSWORD"] = config.MYSQL_PASSWORD
app.config["MYSQL_DB"] = config.MYSQL_DB

mysql = MySQL(app)
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        cur = mysql.connection.cursor()

        cur.execute(
            "INSERT INTO users(username,email,password) VALUES(%s,%s,%s)",
            (username, email, password),
        )

        mysql.connection.commit()
        cur.close()

        return redirect("/")

    return render_template("signup.html")
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (username, password),
        )

        user = cur.fetchone()
        cur.close()

        if user:
            session["username"] = username
            return redirect("/dashboard")

    return render_template("login.html")
@app.route("/dashboard")
def dashboard():
    if "username" in session:
        return render_template("dashboard.html", user=session["username"])
    return redirect("/")
@app.route("/profile", methods=["GET", "POST"])
def profile():
    if "username" not in session:
        return redirect("/")

    if request.method == "POST":
        fullname = request.form["fullname"]
        password = request.form["password"]

        cur = mysql.connection.cursor()
        cur.execute(
            "UPDATE users SET fullname=%s, password=%s WHERE username=%s",
            (fullname, password, session["username"]),
        )
        mysql.connection.commit()
        cur.close()

    return render_template("profile.html")
@app.route("/grades")
def grades():
    if "username" not in session:
        return redirect("/")

    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT subject, marks FROM grades WHERE username=%s",
        (session["username"],),
    )

    data = cur.fetchall()
    cur.close()

    return render_template("grades.html", grades=data)
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
if __name__ == "__main__":
    app.run(debug=True)
