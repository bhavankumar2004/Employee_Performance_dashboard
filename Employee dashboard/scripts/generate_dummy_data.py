import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Generate 100 dummy employees
departments = ['HR', 'Engineering', 'Marketing', 'Finance', 'Operations']
positions = ['Junior', 'Mid-level', 'Senior', 'Manager', 'Director']

employees = []
for i in range(1, 101):
    hire_date = datetime.now() - timedelta(days=random.randint(30, 365*3))
    employees.append({
        'employee_id': i,
        'name': f'Employee {i}',
        'department': random.choice(departments),
        'position': random.choice(positions),
        'hire_date': hire_date.strftime('%Y-%m-%d'),
        'salary': random.randint(30000, 120000)
    })

# Generate performance metrics
performance = []
for emp in employees:
    for quarter in ['Q1', 'Q2', 'Q3', 'Q4']:
        performance.append({
            'employee_id': emp['employee_id'],
            'quarter': quarter,
            'year': 2023,
            'kpi_score': round(random.uniform(60, 100), 1),
            'attendance': random.randint(85, 100),
            'appraisal_rating': random.randint(1, 5),
            'projects_completed': random.randint(1, 10)
        })

# Save to CSV
pd.DataFrame(employees).to_csv('data/employees.csv', index=False)
pd.DataFrame(performance).to_csv('data/performance.csv', index=False)