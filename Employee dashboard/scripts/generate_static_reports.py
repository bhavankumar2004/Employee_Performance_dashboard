import pandas as pd
import matplotlib.pyplot as plt
from config import DB_CONFIG
import mysql.connector

# Connect to database
conn = mysql.connector.connect(**DB_CONFIG)
query = """
SELECT e.department, AVG(p.kpi_score) as avg_kpi, 
       AVG(p.attendance) as avg_attendance,
       AVG(p.appraisal_rating) as avg_rating
FROM employees e
JOIN performance p ON e.employee_id = p.employee_id
GROUP BY e.department, p.quarter, p.year
"""
df = pd.read_sql(query, conn)
conn.close()

# Department-wise KPI
plt.figure(figsize=(10, 6))
df.groupby('department')['avg_kpi'].mean().sort_values().plot(
    kind='barh', title='Average KPI Score by Department')
plt.tight_layout()
plt.savefig('static/department_kpi.png')

# Correlation matrix
corr_df = df[['avg_kpi', 'avg_attendance', 'avg_rating']].corr()
fig, ax = plt.subplots(figsize=(8, 6))
cax = ax.matshow(corr_df, cmap='coolwarm')
plt.xticks(range(len(corr_df.columns)), corr_df.columns)
plt.yticks(range(len(corr_df.columns)), corr_df.columns)
plt.colorbar(cax)
plt.title('Metrics Correlation Matrix')
plt.savefig('static/correlation_matrix.png')