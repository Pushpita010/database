# 📚 Student Management System - Installation & Setup Guide

This guide explains how to install and run this project on a new device after cloning from GitHub.

---

## **Prerequisites**

Before starting, ensure you have these installed on your machine:

### **1. Python 3.8 or Higher**

- Download: https://www.python.org/downloads/
- During installation: **✅ Check "Add Python to PATH"**
- Verify: Open terminal and run:
  ```
  python --version
  ```

### **2. MySQL Server 8.0 or Higher**

- Download: https://dev.mysql.com/downloads/mysql/
- During installation, set:
  - Username: `root`
  - Password: `admin123` (or your preferred password)
- Verify MySQL is running:
  - Windows: Open Services → Search "MySQL" → Ensure it's running
  - Or run: `mysql -u root -p` (then enter your password)

### **3. Git (Optional, if cloning from GitHub)**

- Download: https://git-scm.com/
- Verify: `git --version`

---

## **Installation Steps**

### **Step 1: Clone or Download the Project**

**Option A: Using Git**

```bash
git clone <repository-url>
cd Experiment\ -\ 6
```

**Option B: Download as ZIP**

1. Download ZIP from GitHub
2. Extract the folder
3. Open terminal in the extracted folder

### **Step 2: Create Virtual Environment**

A virtual environment keeps project dependencies isolated.

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows (Command Prompt):
venv\Scripts\activate

# Windows (PowerShell):
venv\Scripts\Activate.ps1

# macOS/Linux:
source venv/bin/activate
```

You should see `(venv)` appear at the start of terminal lines.

### **Step 3: Install Dependencies**

With the virtual environment activated:

```bash
pip install -r requirements.txt
```

This installs all required packages:

- Flask 2.3.3
- mysql-connector-python 8.2.0
- Werkzeug 3.0.1
- python-dotenv 1.0.0
- Flask-WTF 1.2.1
- email-validator 2.1.0

### **Step 4: Configure Environment Variables**

**Create `.env` file** in the project root (Experiment - 6 folder):

```bash
# Windows (Command Prompt):
type > .env

# Windows (PowerShell):
New-Item .env -Type File

# macOS/Linux:
touch .env
```

**Edit `.env` and add:**

```dotenv
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=admin123
MYSQL_DB=flask_auth
SECRET_KEY=your-secret-key-here
DEBUG=False
```

**⚠️ Important:**

- Replace `admin123` with YOUR MySQL password
- Keep `SECRET_KEY` as-is (already generated and secure)
- Never commit `.env` to Git (it contains sensitive data)

### **Step 5: Initialize the Database**

Run the database setup script:

```bash
python setup_db.py
```

**Output should show:**

```
✅ Table 'users' created/verified
✅ Table 'grades' created/verified
✅ Test users inserted into database with hashed passwords
✅ Sample grades inserted for 'admin', 'student1', and 'john'
✅ DATABASE SETUP COMPLETE!
```

This script:

- Creates the database `flask_auth`
- Creates `users` and `grades` tables
- Inserts 3 test users with hashed passwords
- Inserts sample grades for testing

### **Step 6: Start the Flask Application**

```bash
python app.py
```

**Output should show:**

```
 * Running on http://127.0.0.1:5000
```

Open your browser and go to: **http://127.0.0.1:5000**

---

## **Test the Application**

### **Login with Test Credentials:**

| Username   | Password        | Grades                                    |
| ---------- | --------------- | ----------------------------------------- |
| `admin`    | `admin123`      | 2 (ML: 85, DBMS: 90)                      |
| `student1` | `student@123`   | 3 (Python: 92, Web Dev: 88, Database: 85) |
| `john`     | `john@password` | 2 (Math: 78, Physics: 82)                 |

### **Test Features:**

- ✅ **Login** - Use the test credentials above
- ✅ **View Dashboard** - See student info and grade summary
- ✅ **View Grades** - Check subject marks, letter grades, and average
- ✅ **Edit Profile** - Update fullname and password
- ✅ **Signup** - Create a new account
- ✅ **Logout** - End your session

---

## **Project Structure**

```
Experiment - 6/
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── setup_db.py            # Database initialization script
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (don't commit!)
├── .gitignore             # Git ignore rules
├── database/
│   └── schema.sql         # Alternative database schema (MySQL format)
├── templates/             # HTML files
│   ├── login.html
│   ├── signup.html
│   ├── dashboard.html
│   ├── profile.html
│   ├── grades.html
│   └── 404.html
└── static/
    ├── style.css          # Responsive styling
    └── js/
        └── script.js      # Frontend JavaScript
```

---

## **Troubleshooting**

### **Q: "ModuleNotFoundError: No module named 'flask'"**

- Solution: Activate virtual environment and run `pip install -r requirements.txt` again

### **Q: "Access denied for user 'root'@'localhost' (using password: YES)""**

- Solution: Check your `.env` file - `MYSQL_PASSWORD` must match your MySQL root password

### **Q: "ERROR 2003: Can't connect to MySQL server"**

- Solution: Start MySQL server
  - Windows: Services → MySQL → Right-click → Start
  - Or: `mysql.server start` (macOS/Linux)

### **Q: Grades showing "No grades available"**

- Solution:
  1. Run `python setup_db.py` again
  2. Refresh the browser (Ctrl+Shift+Delete to clear cache)
  3. Login with a test user

### **Q: "Port 5000 is already in use"**

- Solution: Kill the previous Flask process:

  ```bash
  # PowerShell:
  Get-Process python | Stop-Process -Force

  # Or change port in app.py (last line):
  # Change: app.run(port=5000) to app.run(port=5001)
  ```

### **Q: Changes aren't showing in the browser**

- Solution:
  1. Stop Flask (Ctrl+C)
  2. Wait 2 seconds
  3. Restart: `python app.py`
  4. Hard refresh browser (Ctrl+Shift+Delete)

---

## **For Development**

### **Enable Debug Mode**

Edit `.env`:

```dotenv
DEBUG=True
```

This enables:

- Auto-reload on code changes
- Detailed error messages
- Interactive debugger

### **Access Database Directly**

```bash
mysql -u root -p
# Enter your password, then:
USE flask_auth;
SELECT * FROM users;
SELECT * FROM grades;
```

### **Keep Dependencies Updated**

```bash
pip list --outdated
pip install --upgrade <package-name>
```

---

## **Deployment Considerations**

Before deploying to production:

1. **Change Secret Key** in `.env`:

   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

2. **Set `DEBUG=False`** in `.env`

3. **Use production WSGI server** (not Flask dev server):

   ```bash
   pip install gunicorn
   gunicorn app:app
   ```

4. **Use strong MySQL password** (not `admin123`)

5. **Enable CSRF protection** in app.py (Flask-WTF is ready)

6. **Use HTTPS** for all connections

7. **Add `.env` to `.gitignore`** (never commit secrets!)

---

## **Quick Start Summary**

```bash
# 1. Clone and navigate
git clone <url>
cd Experiment\ -\ 6

# 2. Virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file with MySQL credentials
echo MYSQL_PASSWORD=admin123 >> .env

# 5. Setup database
python setup_db.py

# 6. Run the app
python app.py

# 7. Open browser
# http://127.0.0.1:5000
```

---

## **Support**

If you encounter issues:

1. Check that MySQL is running
2. Verify `.env` credentials
3. Check Python version: `python --version` (should be 3.8+)
4. Run `pip install -r requirements.txt` again
5. Delete `__pycache__` folders and restart Flask

---

**Good to go! 🚀 Happy coding!**
