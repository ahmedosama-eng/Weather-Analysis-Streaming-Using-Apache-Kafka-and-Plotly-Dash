import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime

from consumer import consumer

# Initialize the Dash app
app = dash.Dash(__name__)

# Global variable to keep track of the current index
current_index = 0

# Define the app layout with centered graphs and tables, and added space
app.layout = html.Div(
    style={
        'fontFamily': 'Arial, sans-serif',
        'backgroundImage': 'linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)),url("https://st2.depositphotos.com/1162190/6186/i/600/depositphotos_61868743-stock-photo-weather-forecast-concept.jpg")',
        'backgroundSize': 'cover',
        'backgroundRepeat': 'no-repeat',
        'backgroundAttachment': 'fixed',
        'textAlign': 'center',
        'padding': '20px'
    },
    children=[
        html.Div(
            [
                html.H1("Live Line Plot of Temperature and Weather Data")
            ],
            style={
                'color': 'white'
            }
        ),
        html.Div([
            html.Div([
                dcc.Graph(id='live-update-temperature-graph', style={'height': '200px', 'width': '400px'}),
                dash_table.DataTable(
                    id='live-update-temperature-table',
                    columns=[{'name': 'Date', 'id': 'Formatted Date'}, {'name': 'Temperature (C)', 'id': 'Temperature (C)'}],
                    style_table={'height': '200px', 'width': '400px'},
                    style_cell={'textAlign': 'left'},
                    page_size=10
                )
            ], style={'display': 'flex', 'flexDirection': 'row', 'alignItems': 'center', 'margin': '10px', 'justifyContent': 'center', 'gap': '20px'}),
            html.Div([
                dcc.Graph(id='live-update-apparent-temperature-graph', style={'height': '200px', 'width': '400px'}),
                dash_table.DataTable(
                    id='live-update-apparent-temperature-table',
                    columns=[{'name': 'Date', 'id': 'Formatted Date'}, {'name': 'Apparent Temperature (C)', 'id': 'Apparent Temperature (C)'}],
                    style_table={'height': '200px', 'width': '400px'},
                    style_cell={'textAlign': 'left'},
                    page_size=10
                )
            ], style={'display': 'flex', 'flexDirection': 'row', 'alignItems': 'center', 'margin': '10px', 'justifyContent': 'center', 'gap': '20px'}),
            html.Div([
                dcc.Graph(id='live-update-humidity-graph', style={'height': '200px', 'width': '400px'}),
                dash_table.DataTable(
                    id='live-update-humidity-table',
                    columns=[{'name': 'Date', 'id': 'Formatted Date'}, {'name': 'Humidity', 'id': 'Humidity'}],
                    style_table={'height': '200px', 'width': '400px'},
                    style_cell={'textAlign': 'left'},
                    page_size=10
                )
            ], style={'display': 'flex', 'flexDirection': 'row', 'alignItems': 'center', 'margin': '10px', 'justifyContent': 'center', 'gap': '20px'}),
            html.Div([
                dcc.Graph(id='live-update-wind-speed-graph', style={'height': '200px', 'width': '400px'}),
                dash_table.DataTable(
                    id='live-update-wind-speed-table',
                    columns=[{'name': 'Date', 'id': 'Formatted Date'}, {'name': 'Wind Speed (km/h)', 'id': 'Wind Speed (km/h)'}],
                    style_table={'height': '200px', 'width': '400px'},
                    style_cell={'textAlign': 'left'},
                    page_size=10
                )
            ], style={'display': 'flex', 'flexDirection': 'row', 'alignItems': 'center', 'margin': '10px', 'justifyContent': 'center', 'gap': '20px'}),
            html.Div([
                dcc.Graph(id='live-update-wind-bearing-graph', style={'height': '200px', 'width': '400px'}),
                dash_table.DataTable(
                    id='live-update-wind-bearing-table',
                    columns=[{'name': 'Date', 'id': 'Formatted Date'}, {'name': 'Wind Bearing (degrees)', 'id': 'Wind Bearing (degrees)'}],
                    style_table={'height': '200px', 'width': '400px'},
                    style_cell={'textAlign': 'left'},
                    page_size=10
                )
            ], style={'display': 'flex', 'flexDirection': 'row', 'alignItems': 'center', 'margin': '10px', 'justifyContent': 'center', 'gap': '20px'}),
            html.Div([
                dcc.Graph(id='live-update-visibility-graph', style={'height': '200px', 'width': '400px'}),
                dash_table.DataTable(
                    id='live-update-visibility-table',
                    columns=[{'name': 'Date', 'id': 'Formatted Date'}, {'name': 'Visibility (km)', 'id': 'Visibility (km)'}],
                    style_table={'height': '200px', 'width': '400px'},
                    style_cell={'textAlign': 'left'},
                    page_size=10
                )
            ], style={'display': 'flex', 'flexDirection': 'row', 'alignItems': 'center', 'margin': '10px', 'justifyContent': 'center', 'gap': '20px'}),
            html.Div([
                dcc.Graph(id='live-update-pressure-graph', style={'height': '200px', 'width': '400px'}),
                dash_table.DataTable(
                    id='live-update-pressure-table',
                    columns=[{'name': 'Date', 'id': 'Formatted Date'}, {'name': 'Pressure (millibars)', 'id': 'Pressure (millibars)'}],
                    style_table={'height': '200px', 'width': '400px'},
                    style_cell={'textAlign': 'left'},
                    page_size=10
                )
            ], style={'display': 'flex', 'flexDirection': 'row', 'alignItems': 'center', 'margin': '10px', 'justifyContent': 'center', 'gap': '20px'}),
        ], style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'}),
        dcc.Interval(
            id='interval-component',
            interval=2*1000,   
            n_intervals=0
        ),
    ]
)

@app.callback(
    [
        Output('live-update-temperature-graph', 'figure'),
        Output('live-update-apparent-temperature-graph', 'figure'),
        Output('live-update-humidity-graph', 'figure'),
        Output('live-update-wind-speed-graph', 'figure'),
        Output('live-update-wind-bearing-graph', 'figure'),
        Output('live-update-visibility-graph', 'figure'),
        Output('live-update-pressure-graph', 'figure'),
        Output('live-update-temperature-table', 'data'),
        Output('live-update-apparent-temperature-table', 'data'),
        Output('live-update-humidity-table', 'data'),
        Output('live-update-wind-speed-table', 'data'),
        Output('live-update-wind-bearing-table', 'data'),
        Output('live-update-visibility-table', 'data'),
        Output('live-update-pressure-table', 'data')
    ],
    Input('interval-component', 'n_intervals')
)
def update_graph_and_table(n):

    batch = pd.DataFrame(next(consumer).value)
    # Prepare the data for each feature
    data = {
        'Formatted Date': batch['Formatted Date'].values.tolist(),
        'Temperature (C)': batch['Temperature (C)'].values.tolist(),
        'Apparent Temperature (C)': batch['Apparent Temperature (C)'].values.tolist(),
        'Humidity': batch['Humidity'].values.tolist(),
        'Wind Speed (km/h)': batch['Wind Speed (km/h)'].values.tolist(),
        'Wind Bearing (degrees)': batch['Wind Bearing (degrees)'].values.tolist(),
        'Visibility (km)': batch['Visibility (km)'].values.tolist(),
        'Pressure (millibars)': batch['Pressure (millibars)'].values.tolist()
    }
    df = pd.DataFrame(data)
    
    
    # Create the figures and tables for each feature
    figures = []
    tables = []
    features = [
        'Temperature (C)',
        'Apparent Temperature (C)',
        'Humidity',
        'Wind Speed (km/h)',
        'Wind Bearing (degrees)',
        'Visibility (km)',
        'Pressure (millibars)'
    ]
    
    for feature in features:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['Formatted Date'],
            y=df[feature],
            mode='lines+markers',
            name=feature
        ))
        fig.update_layout(
            title=feature,
            xaxis_title='Date',
            yaxis_title=feature,
            margin=dict(l=30, r=30, t=30, b=20),
            height=200  # Adjust height as needed
        )
        figures.append(fig)
        
        # Prepare table data
        table_data = df[['Formatted Date', feature]].rename(columns={feature: feature}).to_dict('records')
        tables.append(table_data)
    
    return figures + tables

# Run the Dash app
if __name__ == '__main__':
    app.run_server()