import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# Create SQLAlchemy engine
engine = create_engine('mysql+pymysql://william5:octopus1357@68.178.145.205/Cephalopod')

# Query to fetch data
query = "SELECT Country, Language, TimeDate, Source FROM Cephalopod"

# Fetch data into a DataFrame using SQLAlchemy engine
df = pd.read_sql(query, engine)

# Close the engine connection
engine.dispose()

# Reset index to use it as x-values
df.reset_index(inplace=True)

# Convert Timestamp column to datetime
df['TimeDate'] = pd.to_datetime(df['TimeDate'])

# Extract date and count occurrences per day
df['Date'] = df['TimeDate'].dt.date  # Extract only the date without time
daily_counts = df.groupby('Date').size().reset_index(name='Count')

# Count occurrences of Country and Source
country_counts = df['Country'].value_counts().reset_index(name='Count')
source_counts = df['Source'].value_counts().reset_index(name='Count')

# Initialize Dash app
app = dash.Dash(__name__)
server = app.server
# Define the layout of your Dash app
app.layout = html.Div(children=[
    html.H1("Analytics Dashboard"),
    
    dcc.Dropdown(
        id='country-dropdown',
        options=[
            {'label': 'Country 1', 'value': 'country1'},
            {'label': 'Country 2', 'value': 'country2'},
            # Add more options as needed
        ],
        value='country1'
    ),
    
    dcc.Dropdown(
        id='source-dropdown',
        options=[
            {'label': 'Source 1', 'value': 'source1'},
            {'label': 'Source 2', 'value': 'source2'},
            # Add more options as needed
        ],
        value='source1'
    ),
    
    html.Div([
        dcc.Graph(id='count-over-time-graph'),
        dcc.Graph(id='country-graph'),
        dcc.Graph(id='source-graph')
    ])
])

# Define callback to update graphs
@app.callback(
    [dash.dependencies.Output('count-over-time-graph', 'figure'),
     dash.dependencies.Output('country-graph', 'figure'),
     dash.dependencies.Output('source-graph', 'figure')],
    [dash.dependencies.Input('country-dropdown', 'value'),
     dash.dependencies.Input('source-dropdown', 'value')]
)
# Update the callback function to use 'Date' column explicitly for x-values
def update_graphs(selected_country, selected_source):
    # Filter data based on selected country and source
    filtered_df = df[(df['Country'] == selected_country) & (df['Source'] == selected_source)]
    
    # Create line graph for count over time
    count_over_time_fig = px.line(daily_counts, x='Date', y='Count', labels={'Date': 'Date', 'Count': 'Total Count'})

    # Create column graph for country
    country_fig = px.bar(country_counts, x='Country', y='Count', labels={'Country': 'Country', 'Count': 'Count'})

    # Create column graph for source
    source_fig = px.bar(source_counts, x='Source', y='Count', labels={'Source': 'Source', 'Count': 'Count'})

    return count_over_time_fig, country_fig, source_fig


# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
