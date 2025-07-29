import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from database_utils import fetch_employee_performance_data # Import our data fetching utility

# Initialize the Dash app
app = dash.Dash(__name__)

# --- Data Loading and Preprocessing ---
def get_processed_data():
    df = fetch_employee_performance_data()

    if df.empty:
        print("No data fetched from the database. Dashboard might be empty.")
        return pd.DataFrame()

    # Data type conversion
    df['hire_date'] = pd.to_datetime(df['hire_date'])
    df['performance_date'] = pd.to_datetime(df['performance_date'])

    # Calculate tenure (in years)
    df['tenure'] = (pd.to_datetime('today') - df['hire_date']).dt.days / 365.25

    # Group by employee to get latest performance metrics and overall averages
    # For KPIs, appraisal, and attendance, we take the average across all records for an employee
    # For top/bottom performers, you might want to consider the latest record or an average over a recent period.
    # For simplicity, let's average all historical records for now.
    employee_summary = df.groupby('employee_id').agg(
        first_name=('first_name', 'first'),
        last_name=('last_name', 'first'),
        department=('department', 'first'),
        position=('position', 'first'),
        hire_date=('hire_date', 'first'),
        salary=('salary', 'first'),
        avg_kpi_score=('kpi_score', 'mean'),
        avg_attendance_score=('attendance_score', 'mean'),
        avg_appraisal_rating=('appraisal_rating', 'mean'),
        latest_kpi_score=('kpi_score', lambda x: x.iloc[0] if not x.empty else None), # Get latest for single metric
        latest_attendance_score=('attendance_score', lambda x: x.iloc[0] if not x.empty else None),
        latest_appraisal_rating=('appraisal_rating', lambda x: x.iloc[0] if not x.empty else None),
        num_performance_records=('performance_id', 'count')
    ).reset_index()

    employee_summary['full_name'] = employee_summary['first_name'] + ' ' + employee_summary['last_name']
    employee_summary['tenure'] = (pd.to_datetime('today') - employee_summary['hire_date']).dt.days / 365.25

    return df, employee_summary

df_raw, df_summary = get_processed_data()

# Check if data is loaded
if df_raw.empty or df_summary.empty:
    print("Dashboard will show no data due to empty DataFrames.")

# --- Dashboard Layout ---
app.layout = html.Div(style={'fontFamily': 'Times new roman, sans-serif'}, children=[
    html.H1("Employee Performance Dashboard", style={'textAlign': 'center', 'color': '#2C3E50'}),

    html.Div(style={'display': 'flex', 'justifyContent': 'space-around', 'padding': '20px', 'backgroundColor': "#59B8D0", 'borderRadius': '8px', 'marginBottom': '20px'}, children=[
        html.Div(children=[
            html.H3("Filter by Department"),
            dcc.Dropdown(
                id='department-dropdown',
                options=[{'label': i, 'value': i} for i in df_summary['department'].unique()] if not df_summary.empty else [],
                placeholder="Select Department",
                multi=True,
                style={'width': '300px'}
            )
        ]),
        html.Div(children=[
            html.H3("Filter by Position"),
            dcc.Dropdown(
                id='position-dropdown',
                options=[{'label': i, 'value': i} for i in df_summary['position'].unique()] if not df_summary.empty else [],
                placeholder="Select Position",
                multi=True,
                style={'width': '300px'}
            )
        ])
    ], id='filter-div'),

    html.Div(className='row', style={'display': 'flex', 'flexWrap': 'wrap'}, children=[
        html.Div(className='four columns', style={'flex': '1', 'minWidth': '45%', 'margin': '10px', 'padding': '20px', 'border': '1px solid #CCC', 'borderRadius': '8px', 'boxShadow': '2px 2px 5px rgba(0,0,0,0.1)'}, children=[
            html.H2("Overall Performance Metrics (Avg)", style={'textAlign': 'center'}),
            dcc.Graph(id='overall-kpi-attendance-appraisal-bar')
        ]),
        html.Div(className='four columns', style={'flex': '1', 'minWidth': '45%', 'margin': '10px', 'padding': '20px', 'border': '1px solid #CCC', 'borderRadius': '8px', 'boxShadow': '2px 2px 5px rgba(0,0,0,0.1)'}, children=[
            html.H2("Performance by Department", style={'textAlign': 'center'}),
            dcc.Graph(id='kpi-by-department-bar')
        ])
    ]),

    html.Div(className='row', style={'display': 'flex', 'flexWrap': 'wrap'}, children=[
        html.Div(className='four columns', style={'flex': '1', 'minWidth': '45%', 'margin': '10px', 'padding': '20px', 'border': '1px solid #CCC', 'borderRadius': '8px', 'boxShadow': '2px 2px 5px rgba(0,0,0,0.1)'}, children=[
            html.H2("Top 10 Performers (Avg KPI)", style={'textAlign': 'center'}),
            dcc.Graph(id='top-performers-kpi')
        ]),  
        html.Div(className='four columns', style={'flex': '1', 'minWidth': '45%', 'margin': '10px', 'padding': '20px', 'border': '1px solid #CCC', 'borderRadius': '8px', 'boxShadow': '2px 2px 5px rgba(0,0,0,0.1)'}, children=[
            html.H2("Bottom 10 Performers (Avg KPI)", style={'textAlign': 'center'}),
            dcc.Graph(id='bottom-performers-kpi')
        ])
    ]),

    html.Div(className='row', style={'display': 'flex', 'flexWrap': 'wrap'}, children=[
        html.Div(className='four columns', style={'flex': '1', 'minWidth': '45%', 'margin': '10px', 'padding': '20px', 'border': '1px solid #CCC', 'borderRadius': '8px', 'boxShadow': '2px 2px 5px rgba(0,0,0,0.1)'}, children=[
            html.H2("Appraisal Rating Distribution", style={'textAlign': 'center'}),
            dcc.Graph(id='appraisal-distribution-pie')
        ]),
        html.Div(className='four columns', style={'flex': '1', 'minWidth': '45%', 'margin': '10px', 'padding': '20px', 'border': '1px solid #CCC', 'borderRadius': '8px', 'boxShadow': '2px 2px 5px rgba(0,0,0,0.1)'}, children=[
            html.H2("Attendance Score Distribution", style={'textAlign': 'center'}),
            dcc.Graph(id='attendance-distribution-hist')
        ])
    ]),

    html.Div(className='row', style={'display': 'flex', 'flexWrap': 'wrap'}, children=[
        html.Div(className='twelve columns', style={'width': '100%', 'margin': '10px', 'padding': '20px', 'border': '1px solid #CCC', 'borderRadius': '8px', 'boxShadow': '2px 2px 5px rgba(0,0,0,0.1)'}, children=[
            html.H2("Employee Performance Trends (by selected employee)", style={'textAlign': 'center'}),
            dcc.Dropdown(
                id='employee-trend-dropdown',
                options=[{'label': row['full_name'], 'value': row['employee_id']} for index, row in df_summary.iterrows()] if not df_summary.empty else [],
                placeholder="Select an Employee",
                style={'width': '50%'}
            ),
            dcc.Graph(id='employee-performance-trend')
        ])
    ])
])

# --- Callbacks for Interactivity ---

@app.callback(
    Output('overall-kpi-attendance-appraisal-bar', 'figure'),
    Output('kpi-by-department-bar', 'figure'),
    Output('top-performers-kpi', 'figure'),
    Output('bottom-performers-kpi', 'figure'),
    Output('appraisal-distribution-pie', 'figure'),
    Output('attendance-distribution-hist', 'figure'),
    Input('department-dropdown', 'value'),
    Input('position-dropdown', 'value')
)
def update_dashboard(selected_departments, selected_positions):
    filtered_df_summary = df_summary.copy()

    if selected_departments:
        filtered_df_summary = filtered_df_summary[filtered_df_summary['department'].isin(selected_departments)]
    if selected_positions:
        filtered_df_summary = filtered_df_summary[filtered_df_summary['position'].isin(selected_positions)]

    # Handle empty filtered data
    if filtered_df_summary.empty:
        empty_figure = go.Figure().add_annotation(text="No data to display for the selected filters",
                                                 xref="paper", yref="paper", showarrow=False,
                                                 font=dict(size=20, color='grey'))
        return empty_figure, empty_figure, empty_figure, empty_figure, empty_figure, empty_figure

    # Overall Performance Metrics
    avg_kpi = filtered_df_summary['avg_kpi_score'].mean()
    avg_attendance = filtered_df_summary['avg_attendance_score'].mean()
    avg_appraisal = filtered_df_summary['avg_appraisal_rating'].mean()

    overall_metrics_fig = px.bar(
        x=['Avg KPI Score', 'Avg Attendance Score', 'Avg Appraisal Rating'],
        y=[avg_kpi, avg_attendance, avg_appraisal],
        title='Overall Average Performance Metrics',
        labels={'x': 'Metric', 'y': 'Average Score'},
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    overall_metrics_fig.update_yaxes(range=[0, 1] if any(m in ['Avg KPI Score', 'Avg Attendance Score'] for m in overall_metrics_fig.data[0].x) else [0, 5])

    # KPI by Department
    kpi_by_department = filtered_df_summary.groupby('department')['avg_kpi_score'].mean().reset_index()
    kpi_by_department_fig = px.bar(
        kpi_by_department,
        x='department',
        y='avg_kpi_score',
        title='Average KPI Score by Department',
        labels={'department': 'Department', 'avg_kpi_score': 'Average KPI Score'},
        color='department',
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    kpi_by_department_fig.update_yaxes(range=[0, 1])

    # Top N Performers (by average KPI)
    top_performers = filtered_df_summary.nlargest(10, 'avg_kpi_score')
    top_performers_fig = px.bar(
        top_performers,
        x='full_name',
        y='avg_kpi_score',
        title='Top 10 Performers (by Avg KPI Score)',
        labels={'full_name': 'Employee', 'avg_kpi_score': 'Average KPI Score'},
        color='avg_kpi_score',
        color_continuous_scale=px.colors.sequential.Greens
    )
    top_performers_fig.update_yaxes(range=[0, 1])

    # Bottom N Performers (by average KPI)
    bottom_performers = filtered_df_summary.nsmallest(10, 'avg_kpi_score')
    bottom_performers_fig = px.bar(
        bottom_performers,
        x='full_name',
        y='avg_kpi_score',
        title='Bottom 10 Performers (by Avg KPI Score)',
        labels={'full_name': 'Employee', 'avg_kpi_score': 'Average KPI Score'},
        color='avg_kpi_score',
        color_continuous_scale=px.colors.sequential.Reds
    )
    bottom_performers_fig.update_yaxes(range=[0, 1])

    # Appraisal Rating Distribution
    appraisal_distribution_fig = px.pie(
        filtered_df_summary,
        names='latest_appraisal_rating', # Using latest for a snapshot
        title='Appraisal Rating Distribution',
        color_discrete_sequence=px.colors.qualitative.Vivid
    )
    appraisal_distribution_fig.update_traces(textinfo='percent+label', pull=[0.05 if str(x) == str(filtered_df_summary['latest_appraisal_rating'].mode()[0]) else 0 for x in appraisal_distribution_fig.data[0].labels]) # Highlight mode

    # Attendance Score Distribution (Histogram)
    attendance_distribution_hist = px.histogram(
        filtered_df_summary,
        x='avg_attendance_score',
        nbins=10,
        title='Attendance Score Distribution',
        labels={'avg_attendance_score': 'Average Attendance Score'},
        color_discrete_sequence=px.colors.qualitative.D3 # Use a qualitative color scale
    )
    attendance_distribution_hist.update_xaxes(range=[0, 1]) # Set range for attendance scores


    return (
        overall_metrics_fig,
        kpi_by_department_fig,
        top_performers_fig,
        bottom_performers_fig,
        appraisal_distribution_fig,
        attendance_distribution_hist
    )

@app.callback(
    Output('employee-performance-trend', 'figure'),
    Input('employee-trend-dropdown', 'value')
)
def update_employee_trend(selected_employee_id):
    if not selected_employee_id:
        return go.Figure().add_annotation(text="Please select an employee to see performance trends.",
                                         xref="paper", yref="paper", showarrow=False,
                                         font=dict(size=16, color='grey'))

    employee_df = df_raw[df_raw['employee_id'] == selected_employee_id].sort_values('performance_date')

    if employee_df.empty:
        return go.Figure().add_annotation(text="No performance data available for this employee.",
                                         xref="paper", yref="paper", showarrow=False,
                                         font=dict(size=16, color='grey'))

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=employee_df['performance_date'], y=employee_df['kpi_score'],
                             mode='lines+markers', name='KPI Score'))
    fig.add_trace(go.Scatter(x=employee_df['performance_date'], y=employee_df['attendance_score'],
                             mode='lines+markers', name='Attendance Score'))
    fig.add_trace(go.Scatter(x=employee_df['performance_date'], y=employee_df['appraisal_rating'],
                             mode='lines+markers', name='Appraisal Rating'))

    fig.update_layout(
        title=f"Performance Trend for {employee_df['first_name'].iloc[0]} {employee_df['last_name'].iloc[0]}",
        xaxis_title="Performance Date",
        yaxis_title="Score/Rating",
        hovermode="x unified"
    )

    fig.update_yaxes(range=[0, 1] if not employee_df.empty and employee_df[['kpi_score', 'attendance_score']].max().max() <= 1 else [0,5])

    return fig

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True, port=8050)