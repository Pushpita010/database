import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MySQL Database Configuration
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")  # Set in .env file
MYSQL_DB = os.getenv("MYSQL_DB", "flask_auth")

# Secret key for session (NEVER commit your real key to version control!)
SECRET_KEY = os.getenv(
    "SECRET_KEY", "your-secret-key-change-in-production-12345")

# Pre-configured Test Users (username: password)
# NOTE: In production, these should be stored securely in database
# For demo purposes only - remove in production
TEST_USERS = {
    "pushpita": "pushpita123",
    "admin": "admin123",
    "student1": "student@123",
    "john": "john@password"
}

# Application Settings
ITEMS_PER_PAGE = 10
DEBUG = os.getenv("DEBUG", "False").lower() in ["true", "1", "yes"]
