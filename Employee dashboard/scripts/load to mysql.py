import mysql.connector
import pandas as pd
from config import DB_CONFIG  # Create this with your DB credentials

# Load CSV data
employees = pd.read_csv('data/employees.csv')
performance = pd.read_csv('data/performance.csv')

# Connect to MySQL
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

# Insert employees
for _, row in employees.iterrows():
    cursor.execute("""
        INSERT INTO employees VALUES (%s, %s, %s, %s, %s, %s)
    """, tuple(row))

# Insert performance
for _, row in performance.iterrows():
    cursor.execute("""
        INSERT INTO performance 
        (employee_id, quarter, year, kpi_score, attendance, appraisal_rating, projects_completed)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, tuple(row[1:]))

conn.commit()
conn.close()