# 📚 Student Management System

A Flask-based web application for user authentication, profile management, and displaying student grades.

![Flask](https://img.shields.io/badge/Flask-2.3.3-green?logo=flask)
![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-blue?logo=mysql)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple?logo=bootstrap)

---

## ✨ Features

- 🔐 **User Authentication** - Secure login/signup with password hashing
- 👤 **Profile Management** - Update full name and change password securely
- 📊 **Grade Management** - View grades with automatic letter grading
- 🎨 **Responsive Design** - Mobile-friendly Bootstrap 5 interface
- 🔒 **Security Features** - Session management, password verification
- 📱 **Mobile Optimized** - Works perfectly on all devices
- 🎯 **Clean Architecture** - Separated concerns (models, views, templates)

---

## 📂 Project Structure

```
Experiment - 6/
├── app.py                    # Flask application & routes
├── config.py                 # Configuration & environment variables
├── setup_db.py              # Database initialization script
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variables template
├── MYSQL_SETUP_GUIDE.md     # Complete MySQL setup instructions
├── database/
│   └── schema.sql           # Database schema
├── static/
│   ├── style.css            # Responsive CSS styling
│   └── uploads/             # User uploads folder
├── templates/
│   ├── login.html           # Login page
│   ├── signup.html          # Registration page
│   ├── dashboard.html       # Main dashboard
│   ├── profile.html         # User profile page
│   ├── grades.html          # Grades display page
│   └── 404.html             # Error page
└── logs/                    # Application logs
```

---

## 🚀 Quick Start

### **Prerequisites**

- Python 3.8+
- MySQL 8.0+
- MySQL Workbench (optional but recommended)

### **1. Clone/Download Project**

```bash
cd "d:\AD Lab\Experiment - 6"
```

### **2. Install MySQL**

Follow: [MYSQL_SETUP_GUIDE.md](MYSQL_SETUP_GUIDE.md)

### **3. Create Environment File**

```bash
# Copy template to .env
copy .env.example .env

# Edit .env with your MySQL credentials
notepad .env
```

**Example .env:**

```ini
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DB=flask_auth
SECRET_KEY=your-secret-key-here
DEBUG=False
```

### **4. Install Python Dependencies**

```bash
pip install -r requirements.txt
```

### **5. Create Database**

```bash
python setup_db.py
```

**Output:**

```
✅ Database 'flask_auth' created/verified
✅ Table 'users' created/verified
✅ Table 'grades' created/verified
✅ DATABASE SETUP COMPLETE!
```

### **6. Run Application**

```bash
python app.py
```

**Output:**

```
 * Running on http://127.0.0.1:5000
```

### **7. Open in Browser**

```
http://127.0.0.1:5000
```

---

## 🔑 Test Credentials

### Pre-configured Demo Users:

| Username | Password      | Grades                                |
| -------- | ------------- | ------------------------------------- |
| admin    | admin123      | ML: 85, DBMS: 90                      |
| student1 | student@123   | Python: 92, Web Dev: 88, Database: 85 |
| john     | john@password | Mathematics: 78, Physics: 82          |

### Create New Account:

1. Click **"Create New Account"** on login page
2. Fill in username, email, and password
3. Confirm password
4. Click **"Create Account"**
5. Login with your new credentials

---

## 📖 Application Flow

```
User Visits App
       ↓
login.html (or already logged in)
       ↓
authenticate_user() ← Check database/test users
       ↓
Session Created (user_id stored)
       ↓
dashboard.html (Main Page)
    /    |    \
   ↓     ↓     ↓
Profile Grades Logout
  ↓      ↓
Update  View
Details (Read-only)
```

---

## 🔑 File Descriptions

### **app.py** - Main Application

- Flask setup and configuration
- Route definitions
- Login/Signup authentication
- Profile management
- Grade display
- Session management

### **config.py** - Configuration

- Database credentials (from environment)
- Secret key for sessions
- Test users (demo only)
- Application settings

### **setup_db.py** - Database Setup

- Creates MySQL database
- Creates tables (users, grades)
- Inserts sample data
- Error handling for common issues

### **requirements.txt** - Dependencies

```
Flask==2.3.3
flask-mysqldb==2.0.0
Werkzeug==3.0.1
python-dotenv==1.0.0
Flask-WTF==1.2.1
email-validator==2.1.0
```

### **Templates** - Frontend

- **login.html** - Login form with demo credentials hint
- **signup.html** - Registration form with validation
- **dashboard.html** - Main page after login
- **profile.html** - Update profile & change password
- **grades.html** - View grades (read-only)
- **404.html** - Error page

### **style.css** - Styling

- Gradient backgrounds (purple theme)
- Responsive design (mobile & desktop)
- Smooth animations
- Dark navigation bar
- Card-based layout

---

## 🔐 Security Features

✅ **Implemented:**

- Password hashing (Werkzeug)
- Session management
- Login decorator for protected routes
- Old password verification for password changes
- Input validation & sanitization
- Secure database connections

⚠️ **To Add (Future):**

- CSRF protection (Flask-WTF ready)
- Rate limiting
- Two-factor authentication
- Email verification
- Audit logging

---

## 📊 Database Schema

### **users Table**

```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(100),
    password VARCHAR(255),
    fullname VARCHAR(100)
);
```

### **grades Table**

```sql
CREATE TABLE grades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100),
    subject VARCHAR(100),
    marks INT
);
```

---

## 🎨 Styling Features

- **Color Scheme**: Purple gradient (#667eea to #764ba2)
- **Responsive**: Works on mobile, tablet, desktop
- **Animations**: Smooth transitions and hover effects
- **Icons**: Bootstrap Icons for visual appeal
- **Typography**: Clean, modern fonts
- **Accessibility**: Proper form labels and contrast

---

## ⚙️ Configuration Options

### Environment Variables (.env)

```ini
# MySQL Connection
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DB=flask_auth

# Flask Settings
SECRET_KEY=your-secure-key
DEBUG=False              # True only in development
```

### Application Routes

| Route        | Method   | Purpose            | Auth Required |
| ------------ | -------- | ------------------ | ------------- |
| `/`          | GET/POST | Login page         | No            |
| `/signup`    | GET/POST | Registration       | No            |
| `/dashboard` | GET      | Main dashboard     | Yes           |
| `/profile`   | GET/POST | Profile management | Yes           |
| `/grades`    | GET      | View grades        | Yes           |
| `/logout`    | GET      | Logout             | Yes           |
| `/404`       | GET      | Error page         | No            |

---

## 🐛 Common Issues & Solutions

### **"MySQL Server not running"**

```powershell
Start-Service MySQL80
```

### **"Connection refused - Access denied"**

- Check .env file credentials
- Verify MySQL password is correct
- Run: `python setup_db.py`

### **"Module not found: flask_mysqldb"**

```bash
pip install -r requirements.txt
```

### **"No module named 'dotenv'"**

```bash
pip install python-dotenv
```

---

## 📝 Usage Examples

### **Login Flow**

1. Go to http://127.0.0.1:5000
2. Enter username: `admin`
3. Enter password: `admin123`
4. Click "Login"

### **Update Profile**

1. After login, click "My Profile"
2. Update full name
3. Leave password blank to keep it
4. Click "Update Profile"

### **Change Password**

1. Go to "My Profile"
2. Enter current password in "Current Password"
3. Enter new password (minimum 6 characters)
4. Click "Update Profile"

### **View Grades**

1. Click "My Grades" on dashboard
2. See all subjects and marks
3. Automatic letter grades: A/B/C/D/F
4. Average score calculated automatically

---

## 🧪 Testing

### **Test User Creation**

```bash
# Login page shows demo credentials
admin / admin123

# Or create new account
username: testuser
password: Test@1234

# Then add grades via MySQL:
INSERT INTO grades VALUES (null, 'testuser', 'Python', 95);
```

### **Test Grade Calculation**

Visit grades page and verify:

- Marks correctly displayed
- Letter grades assigned (90+ = A, 80+ = B, etc.)
- Average calculated correctly
- Color-coded badges show

---

## 📱 Responsive Design

- **Desktop** (992px+) - Full layout
- **Tablet** (768px - 991px) - Adjusted padding
- **Mobile** (576px - 767px) - Stack layout
- **Small Mobile** (<576px) - Optimized for touch

---

## 🔍 Performance Tips

1. **Connection Pooling**: Use connection pooling for high traffic
2. **Caching**: Cache frequently accessed data
3. **Indexing**: Add indexes on frequently queried columns
4. **Query Optimization**: Use appropriate WHERE clauses

---

## 📚 Learning Resources

- Flask Docs: https://flask.palletsprojects.com/
- MySQL Docs: https://dev.mysql.com/doc/
- Werkzeug Security: https://werkzeug.palletsprojects.com/
- Bootstrap 5: https://getbootstrap.com/docs/5.0/
- Jinja2 Templates: https://jinja.palletsprojects.com/

---

## 📋 Future Enhancements

- [ ] Email verification on signup
- [ ] Forgot password functionality
- [ ] Profile picture upload
- [ ] Admin dashboard
- [ ] Grade statistics & charts
- [ ] Export grades to PDF
- [ ] Dark mode toggle
- [ ] Two-factor authentication
- [ ] Activity logging
- [ ] API endpoints (REST)

---

## 📄 License

This project is created for educational purposes.

---

## ✍️ Author

Created as part of an academic lab project for demonstrating:

- Flask web development
- MySQL database management
- User authentication systems
- Responsive web design
- Security best practices

---

## 🤝 Contributing

Feel free to fork and improve this project!

---

## 📞 Support Issues

If you encounter issues:

1. Check [MYSQL_SETUP_GUIDE.md](MYSQL_SETUP_GUIDE.md)
2. Verify .env file configuration
3. Check MySQL is running: `Get-Service MySQL80`
4. Check error logs in console output
5. Verify all dependencies: `pip install -r requirements.txt`

---

**Happy Coding! 🚀**
