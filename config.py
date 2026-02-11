# MySQL Database Configuration
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "your_password"
MYSQL_DB = "flask_auth"

# Secret key for session
SECRET_KEY = "your-secret-key-change-in-production-12345"

# Pre-configured Test Users (username: password)
# In production, these should be stored securely in database
TEST_USERS = {
    "pushpita": "pushpita123",
    "admin": "admin123",
    "student1": "student@123",
    "john": "john@password"
}

# Application Settings
ITEMS_PER_PAGE = 10
DEBUG = True
