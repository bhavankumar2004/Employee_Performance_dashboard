import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import mysql.connector
from mysql.connector import Error
import random

# Database connection details
DB_CONFIG = {
    'host': 'localhost',
    'database': 'employee_performance_db',
    'user': 'root',  # Replace with your MySQL username
    'password': 'Windows@11'  # Replace with your MySQL password
}

def create_db_connection():
    """Establishes a connection to the MySQL database."""
    connection = None
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            print("Successfully connected to the database.")
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
    return connection

def close_db_connection(connection):
    """Closes the database connection."""
    if connection and connection.is_connected():
        connection.close()
        print("MySQL connection closed.")

def insert_employees(connection, employees_data):
    """Inserts employee data into the employees table."""
    cursor = connection.cursor()
    sql = """
        INSERT INTO employees (first_name, last_name, department, position, hire_date, salary, email)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    try:
        cursor.executemany(sql, employees_data)
        connection.commit()
        print(f"Inserted {len(employees_data)} employees.")
    except Error as e:
        print(f"Error inserting employees: {e}")
    finally:
        cursor.close()

def insert_performance(connection, performance_data):
    """Inserts performance data into the performance table."""
    cursor = connection.cursor()
    sql = """
        INSERT INTO performance (employee_id, kpi_score, attendance_score, appraisal_rating, feedback, performance_date)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    try:
        cursor.executemany(sql, performance_data)
        connection.commit()
        print(f"Inserted {len(performance_data)} performance records.")
    except Error as e:
        print(f"Error inserting performance records: {e}")
    finally:
        cursor.close()

def generate_dummy_data(num_employees=50, num_performance_records_per_employee=6):
    """Generates dummy employee and performance data."""
    departments = ['HR', 'Engineering', 'Sales', 'Marketing', 'Finance', 'Operations', 'IT', 'Customer Service']
    positions = ['Analyst', 'Engineer', 'Manager', 'Specialist', 'Director', 'Associate', 'Developer', 'Designer', 'Coordinator']

    # --- START MODIFICATION FOR MEANINGFUL NAMES ---
    first_names = [
        "Arjun", "Bharathi", "Chandran", "Deepa", "Elango", "Gomathi", "Hari", "Indira", "Jagadeesh", "Kalaivani",
        "Lakshmi", "Murali", "Nithya", "Prabhu", "Revathi", "Saravanan", "Thamarai", "Uthra", "Velu", "Yamini",
        "Anand", "Divya", "Ganesh", "Kavitha", "Manoj", "Priya", "Rajesh", "Shanthi", "Suresh", "Vimala"
    ]
    last_names = [
        "Kumar", "Raj", "Mani", "Selvam", "Murugan", "Pillai", "Chettiar", "Nair", "Iyer", "Gopal",
        "Devi", "Amma", "Nathan", "Rao", "Samy", "Vasanth", "Shankar", "Balan", "Rajan", "Sundaram","Kumar", "Raj", "Mani", "Selvam", "Murugan", "Pillai", "Nair", "Iyer", "Gopal","Reddy"
    ]
    # --- END MODIFICATION ---

    employees = []
    performance_records = []

    for i in range(1, num_employees + 1):
        # --- MODIFIED: Use random meaningful names ---
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        # Add a number to ensure uniqueness if names repeat, especially for larger datasets
        # Or you could check for unique email/full_name combinations
        email = f"{first_name.lower()}.{last_name.lower()}{i}@example.com"
        # --- END MODIFIED ---

        department = random.choice(departments)
        position = random.choice(positions)
        hire_date = (datetime.now() - timedelta(days=random.randint(365, 1825))).strftime('%Y-%m-%d') # 1-5 years ago
        salary = round(random.uniform(40000, 120000), 2)

        employees.append((first_name, last_name, department, position, hire_date, salary, email))

        for _ in range(num_performance_records_per_employee):
            kpi_score = round(random.uniform(0.5, 1.0), 2) # 0.5 to 1.0
            attendance_score = round(random.uniform(0.7, 1.0), 2) # 0.7 to 1.0
            appraisal_rating = random.randint(1, 5) # 1 to 5
            feedback = random.choice(["Excellent work!", "Good progress.", "Needs improvement in X.", "Met expectations.", "Exceeded expectations."])
            performance_date = (datetime.now() - timedelta(days=random.randint(30, 730))).strftime('%Y-%m-%d') # Last 2 years
            performance_records.append((i, kpi_score, attendance_score, appraisal_rating, feedback, performance_date))

    return employees, performance_records

if __name__ == "__main__":
    connection = create_db_connection()
    if connection:
        employees_data, performance_data = generate_dummy_data()

        # Clear existing data (optional, for fresh runs)
        try:
            cursor = connection.cursor()
            # Important: Delete from 'performance' first due to foreign key constraint
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0;") # Temporarily disable FK checks
            cursor.execute("TRUNCATE TABLE performance") # TRUNCATE is faster for full table clear
            cursor.execute("TRUNCATE TABLE employees")   # TRUNCATE is faster for full table clear
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1;") # Re-enable FK checks
            connection.commit()
            print("Cleared existing data from tables.")
        except Error as e:
            print(f"Error clearing data: {e}")
        finally:
            cursor.close()

        insert_employees(connection, employees_data)
        insert_performance(connection, performance_data)
        close_db_connection(connection)