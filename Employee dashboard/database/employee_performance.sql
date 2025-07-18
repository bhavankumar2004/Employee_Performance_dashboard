CREATE DATABASE employee_performance;
USE employee_performance;

CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    name VARCHAR(100),
    department VARCHAR(50),
    position VARCHAR(50),
    hire_date DATE,
    salary DECIMAL(10,2)
);

CREATE TABLE performance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    quarter VARCHAR(2),
    year INT,
    kpi_score DECIMAL(5,2),
    attendance INT,
    appraisal_rating INT,
    projects_completed INT,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
);