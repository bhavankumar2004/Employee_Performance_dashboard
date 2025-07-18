import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import mysql.connector
from config import DB_CONFIG

# Initialize the app
app = dash.Dash(__name__)

# Connect to database and fetch data
def fetch_data():
    conn = mysql.connector.connect(**DB_CONFIG)
    query = """
    SELECT e.*, p.* 
    FROM employees e
    JOIN performance p ON e.employee_id = p.employee_id
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

df = fetch_data()

# App layout
app.layout = html.Div([
    html.H1("Employee Performance Dashboard"),
    
    # Filters
    html.Div([
        html.Div([
            html.Label("Department"),
            dcc.Dropdown(
                id='dept-filter',
                options=[{'label': dept, 'value': dept} 
                         for dept in df['department'].unique()],
                multi=True,
                placeholder="Select Department(s)"
            )
        ], style={'width': '30%', 'display': 'inline-block'}),
        
        html.Div([
            html.Label("Position"),
            dcc.Dropdown(
                id='position-filter',
                options=[{'label': pos, 'value': pos} 
                         for pos in df['position'].unique()],
                multi=True,
                placeholder="Select Position(s)"
            )
        ], style={'width': '30%', 'display': 'inline-block'}),
        
        html.Div([
            html.Label("Quarter"),
            dcc.Dropdown(
                id='quarter-filter',
                options=[{'label': q, 'value': q} 
                         for q in df['quarter'].unique()],
                value='Q4',
                clearable=False
            )
        ], style={'width': '20%', 'display': 'inline-block'})
    ]),
    
    # Charts
    dcc.Graph(id='kpi-distribution'),
    dcc.Graph(id='attendance-vs-rating'),
    
    # Top/Bottom performers
    html.Div([
        html.Div([
            html.H3("Top Performers"),
            html.Div(id='top-performers')
        ], style={'width': '48%', 'display': 'inline-block'}),
        
        html.Div([
            html.H3("Bottom Performers"),
            html.Div(id='bottom-performers')
        ], style={'width': '48%', 'display': 'inline-block', 'float': 'right'})
    ])
])

# Callbacks
@app.callback(
    [Output('kpi-distribution', 'figure'),
     Output('attendance-vs-rating', 'figure'),
     Output('top-performers', 'children'),
     Output('bottom-performers', 'children')],
    [Input('dept-filter', 'value'),
     Input('position-filter', 'value'),
     Input('quarter-filter', 'value')]
)
def update_charts(selected_depts, selected_positions, selected_quarter):
    filtered_df = df[df['quarter'] == selected_quarter]
    
    if selected_depts:
        filtered_df = filtered_df[filtered_df['department'].isin(selected_depts)]
    if selected_positions:
        filtered_df = filtered_df[filtered_df['position'].isin(selected_positions)]
    
    # KPI Distribution
    kpi_fig = px.histogram(
        filtered_df, x='kpi_score', 
        title='KPI Score Distribution',
        nbins=20, color='department')
    
    # Attendance vs Rating
    scatter_fig = px.scatter(
        filtered_df, x='attendance', y='appraisal_rating',
        color='department', hover_data=['name'],
        title='Attendance vs Appraisal Rating')
    
    # Top/Bottom performers
    top_performers = filtered_df.nlargest(5, 'kpi_score')
    bottom_performers = filtered_df.nsmallest(5, 'kpi_score')
    
    top_list = html.Ul([html.Li(f"{row['name']} (KPI: {row['kpi_score']})") 
                       for _, row in top_performers.iterrows()])
    bottom_list = html.Ul([html.Li(f"{row['name']} (KPI: {row['kpi_score']})") 
                          for _, row in bottom_performers.iterrows()])
    
    return kpi_fig, scatter_fig, top_list, bottom_list

if __name__ == '__main__':
    app.run_server(debug=True)