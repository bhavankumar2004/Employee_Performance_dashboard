-- Create the database
CREATE DATABASE IF NOT EXISTS employee_performance_db;

-- Use the database
USE employee_performance_db;

-- Create the employees table
CREATE TABLE IF NOT EXISTS employees (
    employee_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    department VARCHAR(50),
    position VARCHAR(50),
    hire_date DATE,
    salary DECIMAL(10, 2),
    email VARCHAR(100) UNIQUE
);

-- Create the performance table
CREATE TABLE IF NOT EXISTS performance (
    performance_id INT PRIMARY KEY AUTO_INCREMENT,
    employee_id INT NOT NULL,
    kpi_score DECIMAL(5, 2),
    attendance_score DECIMAL(5, 2),
    appraisal_rating INT,
    feedback TEXT,
    performance_date DATE,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
);