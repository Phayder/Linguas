from flask import Flask
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import pymysql

# Connect to your MySQL database
# Replace 'your_host', 'your_username', 'your_password', and 'your_database' with your actual database credentials
conn = pymysql.connect(
    host='68.178.145.205',
    user='william5',
    password='octopus1357',
    database='Cephalopod'
)

# Define Flask app
server = Flask(__name__)

# Define Dash app
app = dash.Dash(__name__, server=server, url_base_pathname='/dashboard/')
server = app.server
# Define layout
app.layout = html.Div([
    dcc.Graph(id='live-update-graph'),
    dcc.Interval(
        id='interval-component',
        interval=5*1000,  # Update every 5 seconds
        n_intervals=0
    )
])

# Define callback to update graph
@app.callback(
    Output('live-update-graph', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_graph(n):
   # Query data from database
    query = "SELECT LanguageOne, COUNT(*) as count FROM Cephalopod GROUP BY LanguageOne"
    df = pd.read_sql(query, con=conn)

    # Create plot
    fig = go.Figure(data=[go.Bar(x=df['LanguageOne'], y=df['count'])])
    fig.update_layout(title='Users by Country', xaxis_title='Country', yaxis_title='Number of Users')


    return fig

# Run the app
if __name__ == '__main__':
    server.run(debug=True)
