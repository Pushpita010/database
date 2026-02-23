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
('admin', 'ML', 85),
('admin', 'DBMS', 90),
('student1', 'Python', 92),
('student1', 'Web Development', 88),
('student1', 'Database Design', 85),
('john', 'Mathematics', 78),
('john', 'Physics', 82);
