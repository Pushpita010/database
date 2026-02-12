import mysql.connector
from mysql.connector import Error

try:
    # Connect to MySQL without specifying database
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password=''
    )
    
    cursor = connection.cursor()
    
    # Create database
    cursor.execute("CREATE DATABASE IF NOT EXISTS flask_auth")
    print("✅ Database 'flask_auth' created/verified")
    
    # Use the database
    cursor.execute("USE flask_auth")
    
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
    
    # Insert sample grades for pushpita
    cursor.execute("DELETE FROM grades WHERE username='pushpita'")
    cursor.execute("""
    INSERT INTO grades (username, subject, marks) VALUES 
    ('pushpita', 'ML', 85),
    ('pushpita', 'DBMS', 90)
    """)
    connection.commit()
    print("✅ Sample grades inserted for 'pushpita'")
    
    cursor.close()
    connection.close()
    
    print("\n✅ DATABASE SETUP COMPLETE!")
    print("\nYou can now:")
    print("1. Signup: Create new account")
    print("2. Login: pushpita / pushpita123 (test user)")
    
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
