# 🚀 QUICK START REFERENCE

## ONE-MINUTE SETUP

```
Step 1: Open MySQL Command Line
Step 2: Paste and run the SQL below
Step 3: Update MySQL password in config.py
Step 4: Run: python app.py
Step 5: Go to http://127.0.0.1:5000
Step 6: Login with: pushpita / pushpita123
```

---

## DATABASE SETUP - COPY & PASTE

```sql
CREATE DATABASE flask_auth;
USE flask_auth;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(100),
    password VARCHAR(255),
    fullname VARCHAR(100)
);

CREATE TABLE grades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100),
    subject VARCHAR(100),
    marks INT
);

INSERT INTO grades (username, subject, marks) VALUES
('pushpita', 'ML', 85),
('pushpita', 'DBMS', 90);
```

---

## LOGIN CREDENTIALS (For Testing)

| User | Password | Status |
|------|----------|--------|
| pushpita | pushpita123 | ✅ Has 2 grades |
| admin | admin123 | ✅ Ready to use |
| student1 | student@123 | ✅ Ready to use |
| john | john@password | ✅ Ready to use |

---

## FILE STRUCTURE

```
✅ UPDATED:
  - app.py (Secure auth, password hashing, error handling)
  - config.py (Test users, better structure)
  - requirements.txt (Flask, Werkzeug, MySQL)
  - style.css (Complete Bootstrap redesign)

✅ NEW:
  - login.html (Modern UI)
  - signup.html (Registration form)
  - dashboard.html (Dashboard cards)
  - profile.html (Profile management)
  - grades.html (Grades with stats)
  - 404.html (Error page)
  - README.md (Documentation)
  - SETUP_GUIDE.md (Setup instructions)
```

---

## TEST USERS CREDENTIALS IN CONFIG.PY

```python
TEST_USERS = {
    "pushpita": "pushpita123",
    "admin": "admin123",
    "student1": "student@123",
    "john": "john@password"
}
```

These are stored in config.py for quick testing!
Change MYSQL_PASSWORD to your actual MySQL password.

---

## KEY SECURITY FEATURES

✅ Password Hashing (Werkzeug)
✅ Session Management
✅ SQL Injection Prevention
✅ Form Validation
✅ Protected Routes
✅ Secure Logout

---

## WHAT YOU CAN DO

1. **Login** with test users
2. **Register** new account
3. **Update Profile** with full name & password
4. **View Grades** with letter grades & average
5. **Logout** securely
6. **Mobile Responsive** on any device

---

## COMMANDS

### Start Application:
```bash
cd c:\Users\KIIT0001\Documents\ADLAB\database
python app.py
```

### Install Dependencies (if needed):
```bash
python -m pip install -r requirements.txt
```

### Test Imports:
```bash
python -c "from flask import Flask; print('OK')"
```

---

## URL MAPPING

```
http://127.0.0.1:5000             → Login Page
http://127.0.0.1:5000/signup      → Register
http://127.0.0.1:5000/dashboard   → Dashboard (needs login)
http://127.0.0.1:5000/profile     → Profile (needs login)
http://127.0.0.1:5000/grades      → Grades (needs login)
http://127.0.0.1:5000/logout      → Logout
```

---

## TROUBLESHOOTING

**Can't connect to MySQL?**
- Check if MySQL is running
- Update password in config.py line 4

**Module not found?**
- Run: `python -m pip install -r requirements.txt`

**Port 5000 already in use?**
- Change line 159 in app.py from 5000 to 5001

**Database not found?**
- Run the SQL setup commands above

---

## DOCUMENTATION

📘 See **README.md** for complete guide
📘 See **SETUP_GUIDE.md** for detailed setup

---

**Everything is ready to use! Just run: `python app.py`**
