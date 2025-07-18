import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from IPython.display import display, HTML
import os

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# ========================
# DATA GENERATION FUNCTIONS
# ========================

def generate_employees(num_employees=100):
    """Generate employee master data"""
    departments = ['HR', 'Engineering', 'Marketing', 'Finance', 'Operations', 'Sales']
    positions = ['Junior', 'Associate', 'Senior', 'Manager', 'Director', 'VP']
    first_names = ['James', 'Mary', 'Robert', 'Patricia', 'John', 'Jennifer', 
                 'Michael', 'Linda', 'David', 'Elizabeth']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 
                'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez']
    
    employees = []
    for emp_id in range(1, num_employees + 1):
        hire_date = datetime.now() - timedelta(days=random.randint(30, 365*5))
        department = random.choice(departments)
        
        # Department-specific position weights
        if department in ['Engineering', 'Finance']:
            position = random.choices(positions, weights=[20, 30, 25, 15, 8, 2], k=1)[0]
        else:
            position = random.choices(positions, weights=[25, 30, 20, 15, 8, 2], k=1)[0]
        
        # Position-based salary ranges
        salary_ranges = {
            'Junior': (30000, 45000),
            'Associate': (45000, 65000),
            'Senior': (65000, 90000),
            'Manager': (90000, 120000),
            'Director': (120000, 160000),
            'VP': (160000, 250000)
        }
        salary = random.randint(*salary_ranges[position])
        
        employees.append({
            'employee_id': emp_id,
            'first_name': random.choice(first_names),
            'last_name': random.choice(last_names),
            'full_name': f"{random.choice(first_names)} {random.choice(last_names)}",
            'department': department,
            'position': position,
            'hire_date': hire_date.strftime('%Y-%m-%d'),
            'salary': salary,
            'email': f"{random.choice(first_names).lower()}.{random.choice(last_names).lower()}@company.com"
        })
    
    return pd.DataFrame(employees)

def generate_performance(employees_df):
    """Generate quarterly performance metrics"""
    quarters = ['Q1', 'Q2', 'Q3', 'Q4']
    year = 2023
    performance = []
    
    for _, emp in employees_df.iterrows():
        # Base performance level with position adjustment
        base_kpi = random.uniform(60, 90) + (5 if emp['position'] in ['Manager', 'Director', 'VP'] else 0)
        
        for quarter in quarters:
            # Quarterly variation with department influence
            kpi_variation = random.uniform(-10, 10)
            if emp['department'] == 'Engineering':
                kpi_variation += random.uniform(0, 5)
            kpi_score = max(40, min(100, base_kpi + kpi_variation))
            
            # Generate correlated metrics
            attendance = max(75, min(100, kpi_score/2 + random.uniform(30, 50)))
            appraisal = min(5, max(1, round(kpi_score/20 + random.uniform(-0.5, 0.5))))
            projects = min(10, max(1, int(kpi_score/12 + random.uniform(-2, 2))))
            
            performance.append({
                'employee_id': emp['employee_id'],
                'employee_name': emp['full_name'],
                'department': emp['department'],
                'position': emp['position'],
                'quarter': quarter,
                'year': year,
                'kpi_score': round(kpi_score, 1),
                'attendance_pct': round(attendance),
                'appraisal_rating': appraisal,
                'projects_completed': projects,
                'training_hours': random.randint(0, 20),
                'satisfaction_score': random.randint(1, 10),
                'promotion_eligible': 'Yes' if kpi_score > 75 and appraisal >=4 else 'No'
            })
    
    return pd.DataFrame(performance)

# ====================
# GENERATE AND SAVE DATA
# ====================

# Create data directory if it doesn't exist
os.makedirs('data', exist_ok=True)

# Generate datasets
employees_df = generate_employees(150)  # 150 employees
performance_df = generate_performance(employees_df)

# Save to CSV
employee_file = 'data/employee_records.csv'
performance_file = 'data/performance_metrics.csv'
employees_df.to_csv(employee_file, index=False)
performance_df.to_csv(performance_file, index=False)

# ====================
# DOWNLOAD LINKS
# ====================

# Create HTML download links
html_content = f"""
<h3>Employee Performance Datasets</h3>
<p>Generated {len(employees_df)} employee records and {len(performance_df)} performance metrics</p>

<h4>Download CSV Files:</h4>
<ul>
    <li><a href='{employee_file}' download>Employee Records (Master Data)</a> - {os.path.getsize(employee_file)/1024:.1f} KB</li>
    <li><a href='{performance_file}' download>Performance Metrics (Quarterly Data)</a> - {os.path.getsize(performance_file)/1024:.1f} KB</li>
</ul>

<h4>Sample Employee Data:</h4>
{employees_df.head(3).to_html()}

<h4>Sample Performance Data:</h4>
{performance_df.head(5).to_html()}
"""

display(HTML(html_content))
print("\nCSV files saved to the 'data' folder in your working directory")