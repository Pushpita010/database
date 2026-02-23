import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

# Load environment variables
load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_DB = os.getenv("MYSQL_DB", "flask_auth")

try:
    # Connect to MySQL without specifying database
    connection = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD
    )

    cursor = connection.cursor()

    # Drop database if it exists (to ensure clean slate)
    cursor.execute(f"DROP DATABASE IF EXISTS {MYSQL_DB}")
    print(f"✅ Cleaned up old database (if existed)")

    # Create database
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DB}")
    print(f"✅ Database '{MYSQL_DB}' created/verified")

    # Use the database
    cursor.execute(f"USE {MYSQL_DB}")

    # Create users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(100) UNIQUE NOT NULL,
        email VARCHAR(100),
        password VARCHAR(255),
        fullname VARCHAR(100)
    )
    """)
    print("✅ Table 'users' created/verified")

    # Create grades table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS grades (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(100),
        subject VARCHAR(100),
        marks INT
    )
    """)
    print("✅ Table 'grades' created/verified")

    # Insert test users into users table with hashed passwords
    cursor.execute(
        "DELETE FROM users WHERE username IN ('admin', 'student1', 'john')")

    # Hash passwords before inserting
    admin_hash = generate_password_hash('admin123')
    student1_hash = generate_password_hash('student@123')
    john_hash = generate_password_hash('john@password')

    cursor.execute(
        "INSERT INTO users (username, email, password, fullname) VALUES (%s, %s, %s, %s)",
        ('admin', 'admin@test.com', admin_hash, 'Admin User')
    )
    cursor.execute(
        "INSERT INTO users (username, email, password, fullname) VALUES (%s, %s, %s, %s)",
        ('student1', 'student1@test.com', student1_hash, 'Student One')
    )
    cursor.execute(
        "INSERT INTO users (username, email, password, fullname) VALUES (%s, %s, %s, %s)",
        ('john', 'john@test.com', john_hash, 'John Doe')
    )
    print("✅ Test users inserted into database with hashed passwords")

    # Insert sample grades for test users
    cursor.execute(
        "DELETE FROM grades WHERE username IN ('admin', 'student1', 'john')")
    cursor.execute("""
    INSERT INTO grades (username, subject, marks) VALUES 
    ('admin', 'ML', 85),
    ('admin', 'DBMS', 90),
    ('student1', 'Python', 92),
    ('student1', 'Web Development', 88),
    ('student1', 'Database Design', 85),
    ('john', 'Mathematics', 78),
    ('john', 'Physics', 82)
    """)
    connection.commit()
    print("✅ Sample grades inserted for 'admin', 'student1', and 'john'")

    cursor.close()
    connection.close()

    print("\n✅ DATABASE SETUP COMPLETE!")
    print("\nYou can now:")
    print("1. Signup: Create new account")
    print(f"2. Login: admin / admin123 (test user)")

except Error as err:
    if err.errno == 2003:
        print("❌ ERROR: MySQL Server is not running!")
        print("\nSolution:")
        print("1. Start MySQL Server")
        print("2. Then run this script again")
    elif err.errno == 1045:
        print("❌ ERROR: Access denied - MySQL password is incorrect")
        print("\nSolution:")
        print("1. Edit config.py")
        print("2. Set MYSQL_PASSWORD to your actual MySQL root password")
        print("3. Run this script again")
    else:
        print(f"❌ ERROR: {err}")
except Exception as e:
    print(f"❌ ERROR: {e}")
