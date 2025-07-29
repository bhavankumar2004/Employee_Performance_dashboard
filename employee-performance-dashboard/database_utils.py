import mysql.connector
from mysql.connector import Error
import pandas as pd

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
            print("Database connection successful.")
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
    return connection

def fetch_employee_performance_data():
    """Fetches combined employee and performance data from the database."""
    connection = create_db_connection()
    if connection is None:
        return pd.DataFrame() # Return empty DataFrame if connection fails

    try:
        query = """
            SELECT
                e.employee_id,
                e.first_name,
                e.last_name,
                e.department,
                e.position,
                e.hire_date,
                e.salary,
                p.performance_id, -- <--- ADD THIS LINE
                p.kpi_score,
                p.attendance_score,
                p.appraisal_rating,
                p.feedback,
                p.performance_date
            FROM
                employees e
            JOIN
                performance p ON e.employee_id = p.employee_id
            ORDER BY
                e.employee_id, p.performance_date DESC;
        """
        df = pd.read_sql(query, connection)
        print("Data fetched successfully.")
        return df
    except Error as e:
        print(f"Error fetching data: {e}")
        return pd.DataFrame()
    finally:
        if connection.is_connected():
            connection.close()
            print("Database connection closed.")

if __name__ == "__main__":
    # Example usage:
    df_performance = fetch_employee_performance_data()
    print("\nSample Data from Database:")
    print(df_performance.head())
    print(f"\nTotal records fetched: {len(df_performance)}")