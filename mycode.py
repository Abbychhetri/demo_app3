import pandas as pd
import numpy as np
import datetime
import plotly.express as px
import plotly.graph_objects as go
import dash
import dash_bootstrap_components as dbc
import dash_daq as daq

from dash.dependencies import Input, Output
from dash import Dash, dcc, html, Input, Output
from plotly import graph_objects as go

data_1 = pd.read_csv('DataLogMeasurement_2019_09_052.csv')


data_2 = data_1['Device Record ID|Device ID|Time Stamp|Control Name|Description'].str.split('|', expand=True)
data_2.columns = ['Device_record_ID', 'Device_ID', 'Time_stamp', 'Control_name', 'Description']


data_3 = data_2.dropna().reset_index(drop=True)

data_3 = data_3.astype(
    {"Device_record_ID": 'category', "Device_ID": 'category', "Control_name": 'category', "Description": 'category'})
data_3["Time_stamp"] = pd.to_datetime(data_3["Time_stamp"])

data_3['Date'] = data_3['Time_stamp'].dt.normalize()
data_3['Time'] = data_3['Time_stamp'].dt.strftime('%H:%M:%S')
data_3['day_of_week'] = data_3['Date'].dt.day_name()

conditions = [
    (data_3['Time'] >= '06') & (data_3['Time'] <= '12'),
    (data_3['Time'] >= '12') & (data_3['Time'] <= '18'),
    (data_3['Time'] >= '18') & (data_3['Time'] <= '24'),
    (data_3['Time'] >= '24') & (data_3['Time'] <= '6')]
choices = ['Morning', 'Afternoon', 'Evening', 'Night']
data_3['time_of_day'] = np.select(conditions, choices, default='Night')

data_3['Phases'] = np.where(data_3['Device_ID'].str.startswith('2'), 'Phase-2', 'Phase-1')


data_3.loc[data_3['Description'].str.contains('call'), 'Activity'] = 'Call Funtion'
data_3.loc[data_3['Description'].str.contains('Brain Yoga'), 'Activity'] = 'Brain Yoga Application'
data_3.loc[data_3['Description'].str.contains('Weather Scrolled'), 'Activity'] = 'Weather Application'
data_3.loc[data_3['Description'].str.contains('Word Search '), 'Activity'] = 'Word Search Puzzle Application'
data_3.loc[data_3['Description'].str.contains('Mindmate'), 'Activity'] = 'Mindmate Application'
data_3.loc[data_3['Description'].str.contains('Duolingo'), 'Activity'] = 'Duolingo Application'
data_3.loc[data_3['Description'].str.contains('Calendar'), 'Activity'] = 'Calendar Application'
data_3.loc[data_3['Description'].str.contains('BrainyApp'), 'Activity'] = 'Brainy Application'
data_3.loc[data_3['Description'].str.contains('Colorfy'), 'Activity'] = 'Colorfy Application'
data_3.loc[data_3['Description'].str.contains('Tai Chi Fit launched'), 'Activity'] = 'Tai Chi Fit Application'
data_3.loc[data_3['Description'].str.contains('Map My Fitness'), 'Activity'] = 'Map My Fitness Application'
data_3.loc[data_3['Description'].str.contains('My Fitness Pal'), 'Activity'] = 'My Fitness Pal Application'
data_3.loc[data_3['Description'].str.contains('Eidetic'), 'Activity'] = 'Eidetic Application'
data_3.loc[data_3['Description'].str.contains('Camera'), 'Activity'] = 'Camera Application'
data_3.loc[data_3['Description'].str.contains('Daily Yoga'), 'Activity'] = 'Daily Yoga Application'

data_3 = data_3.astype(
    {"day_of_week": 'category', "time_of_day": 'category', "Phases": 'category', "Activity": 'category'})
data_3["Time"] = pd.to_datetime(data_3["Time"])


data_3['time_diff'] = data_3['Time_stamp'].diff()
data_3['time_diff'] = data_3['time_diff'].dt.total_seconds()

app = Dash(__name__, external_stylesheets=[dbc.themes.QUARTZ])  # #
server=app.server
app.title = 'FAME ANALYTICS'

app.layout = html.Div([

    html.Img(
        src="https://user-images.githubusercontent.com/64204173/199643617-abf87dc1-3ff1-4910-bff0-36ad790352db.png",
        style={'display': 'inline-block', 'width': '3%', 'height': '3%'}),
    html.H1("WELCOME TO FAME DASHBOARD ANALYTICS", style={'text-align': 'center'}),
    html.P("Explore your device usage with charts, graphs and summary cards", style={'text-align': 'center'}),
    html.P('Todays Date: ' + str(datetime.datetime.now().date())),

    html.Br(),
    dcc.Dropdown(data_3.Device_ID.unique(), id='participants-dropdown',
                 multi=False,
                 value='FAME040',
                 style={'width': "100%", 'color': 'Black'}
                 ),

    html.Div(id='output_container', children=[]),
    html.Br(),

    html.Div(
        daq.Gauge(showCurrentValue=True, units="Hours", color="#9B51E0",
                  id="my-daq-gauge1", min=0, max=100, value=0, label="Hours Used"
                  ),
        className="four columns",
    ),

    dbc.Row([

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6("Device Last Accessed on (Date):", style={"font-weight": "bold"}),
                    html.H2(id='last-accessed', children='000', style={'fontSize': 16})

                ], style={'textAlign': 'center'})
            ], style={'backgroundColor': '#191970'}),
        ], width=3),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6("Device Last Accessed on (Time):", style={"font-weight": "bold"}),
                    html.H2(id='total-usage', children='000', style={'fontSize': 16})

                ], style={'textAlign': 'center'})
            ], style={'backgroundColor': '#191970'}),
        ], width=3),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6("Most Used Application:", style={"font-weight": "bold"}),
                    html.H2(id='most-used-app', children='000', style={'fontSize': 16})

                ], style={'textAlign': 'center'})
            ], style={'backgroundColor': '#191970'}),
        ], width=3),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6("Least Used Application:", style={"font-weight": "bold"}),
                    html.H2(id='least-used-app', children='000', style={'fontSize': 16})

                ], style={'textAlign': 'center'})
            ], style={'backgroundColor': '#191970'}),
        ], width=3)
    ], className='mb-2'),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([html.Div([
                ]),
                    dcc.Graph(id='pie_chart', figure={}),

                ])
            ]),
        ], width=6),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([html.Div([
                ]),
                    dcc.Graph(id='histogram', figure={}),

                ])
            ]),
        ], width=6),

    ], className='mr-5'),

])


# Connect the Plotly graphs with Dash Components
@app.callback(

    Output(component_id='output_container', component_property='children'),
    Output("my-daq-gauge1", "value"),
    Output(component_id='last-accessed', component_property='children'),
    Output(component_id='total-usage', component_property='children'),
    Output(component_id='most-used-app', component_property='children'),
    Output(component_id='least-used-app', component_property='children'),
    Output(component_id='pie_chart', component_property='figure'),
    Output(component_id='histogram', component_property='figure'),

    Input(component_id='participants-dropdown', component_property='value'),
)
def update_graph(option_slctd):
    container = "You have choosen {} ".format(option_slctd) + " as your device"

    dff = data_3.copy()
    dff = dff[dff["Device_ID"] == option_slctd]

    g = dff[(dff['Device_ID'] == option_slctd)]
    g1 = g.groupby(["Activity"]).count().reset_index()
    g2 = g1.loc[:, ['Activity', 'time_diff']]

    g2 = g1.sort_values(by='time_diff', ascending=False)
    g3 = g2.loc[:, ['Activity', 'time_diff']]

    g3["Minutes"] = g3["time_diff"] / 60
    g3["Hours"] = g3["Minutes"] / 60
    g3.columns = ['Activities', 'Seconds', 'Minutes', 'Hours']

    g3.round(2)

    table = go.Figure(data=[go.Table(
        header=dict(values=list(g3.columns),
                    fill_color='paleturquoise',
                    align=['left', 'center']), columnwidth=[300, 80],

        cells=dict(values=[g3.Activities, g3.Seconds.round(2), g3.Minutes.round(2), g3.Hours.round(2)],
                   fill=dict(color=['paleturquoise', 'white']), line_color='darkslategray', font_size=12, height=30,
                   align=['left', 'center']))
    ])

    hours_used = g3['Minutes'].sum().round(2)

    first_card_calc_1 = dff['Date'].max()
    first_card = pd.to_datetime(first_card_calc_1).date()

    second_card_calc_1 = dff['Time'].max()
    second_card = pd.to_datetime(second_card_calc_1).time()

    third_card_calc = dff[(dff['Device_ID'] == option_slctd)]
    third_card_calc_1 = pd.value_counts(third_card_calc['Activity']).head(3).reset_index()
    third_card_calc_1.columns = ['Applications', 'Frequency']
    third_card = third_card_calc_1['Applications'].iloc[0]

    fourth_card_calc = dff[(dff['Device_ID'] == option_slctd)]
    fourth_card_calc_1 = pd.value_counts(fourth_card_calc['Activity']).tail(3).reset_index()
    fourth_card_calc_1.columns = ['Applications', 'Frequency']
    fourth_card = fourth_card_calc_1['Applications'].iloc[2]

    pie_process_1 = dff[(dff['Device_ID'] == option_slctd)]
    pie_process_2 = pd.value_counts(pie_process_1['time_of_day']).reset_index()
    pie_process_2.columns = ['Time', 'Frequency']
    pie = px.pie(pie_process_2, values='Frequency', names='Time',
                 title="Pie chart showing FAME App usage according to time of day for device -  " + option_slctd,
                 color='Time',
                 color_discrete_map={'Afternoon': 'lightcyan',
                                     'Evening': 'cyan',
                                     'Morning': 'royalblue',
                                     'Night': 'darkblue'})
    pie.update_layout(title={'font': {'size': 15}, 'font_family': 'Arial'})

    histogram_day_of_week = px.histogram(dff, x="day_of_week", color_discrete_sequence=['#2AB4F5']
                                         , labels={'x': 'Days', 'y': 'Count'}).update_xaxes(
        categoryorder='total ascending'
        , title="Bar chart showing Device Usage according to Days for device - " + option_slctd)

    return container, hours_used, first_card, second_card, third_card, fourth_card, pie, histogram_day_of_week


if __name__ == '__main__':
    app.run_server(debug=False, port=8904)



