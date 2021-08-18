# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 14:04:14 2021
@author: balag
"""

import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
from collections import deque
import numpy as np
import pandas as pd
import time
from collections import OrderedDict

date_time_ws= deque(maxlen=20)#date time for ws
date_time_pht= deque(maxlen=20)#date time for pressure temperature and humidity
date_time_pm = deque(maxlen=20)# date time for pm
date_time_co = deque(maxlen=20)#date time for co
date_time_no2 = deque(maxlen=20)#date time for no2
date_time_c4h10 = deque(maxlen=20)#date time for c4h10



ws = deque(maxlen=20)#wind speed
press = deque(maxlen=20)# pressure
temp = deque(maxlen=20)# temperature
hum = deque(maxlen=20)# humidity
pm1 = deque(maxlen=20)#pm 1
pm2_5 = deque(maxlen=20)# pm 2.5
pm10 = deque(maxlen=20)# pm 10
co = deque(maxlen=20)#co
no2 = deque(maxlen=20)# no2
c4h10 = deque(maxlen=20)# c4h10
lat = deque(maxlen=20)# lat
lon = deque(maxlen=20)# lon

app = dash.Dash(__name__)
app_color = {"graph_bg": "#082255", "graph_line": "#007ACE"}
app.layout = html.Div(
	[  
################################################ HEADER ##################################################

        html.Div(
            [
                html.Div(
                    [
                        html.H4("MINTS DASHBOARD", className="app__header__title"),
                        html.P(
                            " ",
                            # className="app__header__title--grey",
                        ),
                    ],
                   # className="app__header__desc",
                ),

            ],
            className="app__block",
        ),
############################################## BODY ###################################################################
        html.Div([
           html.Div([ 
            ############### WindSpeed #################### 
            html.Div([
                html.Div(
                    [html.H6("Wind Speed", className="graph__title")]
                ),
        		dcc.Graph(id = 'wind-live-graph', animate = True),
        		dcc.Interval(
        			id = 'wind-graph-update',
        			interval = 5000,
        			n_intervals = 0
        		),
            ],
                className="one-third column graph__container first" #wind__speed__container,
            ),
            
            ############### PHT #################### 
            html.Div([
                html.Div(
                    [html.H6("Pressure Humidity Temperature", className="graph__title")]
                ),
        		dcc.Graph(id = 'pht-live-graph', animate = True),
        		dcc.Interval(
        			id = 'pht-graph-update',
        			interval = 5000,
        			n_intervals = 0
        		),
            ],
                className="one-third column graph__container first" #wind__speed__container,
            ),
            
            ############### PM #################### 
            html.Div([
                html.Div(
                    [html.H6("Particulate Matter", className="graph__title")]
                ),
        		dcc.Graph(id = 'pm-live-graph', animate = True),
        		dcc.Interval(
        			id = 'pm-graph-update',
        			interval = 5000,
        			n_intervals = 0
        		),
            ],
                className="one-third column graph__container first" #wind__speed__container,
            ),
    ]),
    html.Div([   
            ############### CO #################### 
            html.Div([
                html.Div(
                    [html.H6("CO", className="graph__title")]
                ),
        		dcc.Graph(id = 'co-live-graph', animate = True),
        		dcc.Interval(
        			id = 'co-graph-update',
        			interval = 5000,
        			n_intervals = 0
        		),
            ],
                className="one-third column graph__container first" #wind__speed__container,
            ),
########################### NO2 #######################            
            html.Div([
              html.Div(
                  [html.H6("NO2", className="graph__title")]
              ),
      		dcc.Graph(id = 'no2-live-graph', animate = True),
      		dcc.Interval(
      			id = 'no2-graph-update',
      			interval = 5000,
      			n_intervals = 0
      		),
          ],
              className="one-third column graph__container first" #wind__speed__container,
          ),
            
########################### C4H10 #######################             
                                    html.Div([
                html.Div(
                    [html.H6("C4H10", className="graph__title")]
                ),
        		dcc.Graph(id = 'c4h10-live-graph', animate = True),
        		dcc.Interval(
        			id = 'c4h10-graph-update',
        			interval = 5000,
        			n_intervals = 0
        		),
            ],
                className="one-third column graph__container first" #wind__speed__container,
            ),
                                    
          ]),
            html.Div([
                # html.Div([
                #             html.Div(
                #                 [html.H6("Location of the Nodes", className="graph__title")]
                #             ),
                #     		dcc.Graph(id = 'Nodes-live-graph', animate = True),
                #     		dcc.Interval(
                #     			id = 'nodes-graph-update',
                #     			interval = 5000,
                #     			n_intervals = 0
                #     		),
                #         ],
                #             className="one-third column graph__container first" #wind__speed__container,
                #         ),
                ])
        ])
	]
)

@app.callback(Output('wind-live-graph', 'figure'),[ Input('wind-graph-update', 'n_intervals') ])
def update_graph_wind(n):
    df_json = pd.read_json('mintsData\\rawMQTT\\001e0636e527\\WIMDA.json', lines = True)
 
    date_time_ws.append(df_json['dateTime'][0])

    ws.append(df_json['windSpeedMetersPerSecond'][0])

    data = go.Scatter(
        x= list(date_time_ws),
        y= list(ws),
        name='Scatter',
        mode= 'lines+markers'
        )
    layout = go.Layout(xaxis = dict(range = [min(date_time_ws),max(date_time_ws)]),yaxis = dict(range = [min(ws),max(ws)]))

    fig1=go.Figure(data,layout)
    fig1.update_layout(
                        xaxis_title="Date Time ",
                        yaxis_title="Wind Speed (m/s)",
                        plot_bgcolor=app_color["graph_bg"],
                        paper_bgcolor=app_color["graph_bg"],
                        font_color="white",
                        legend_title="Wind Speed",
                        font=dict(
                        color="white"
                            ))
    return fig1

@app.callback(Output('pht-live-graph', 'figure'),[ Input('pht-graph-update', 'n_intervals') ])
def update_graph_pht(n):
    df_json = pd.read_json('mintsData\\rawMQTT\\001e0636e527\\WIMDA.json', lines = True)
 
    date_time_pht.append(df_json['dateTime'][0])

    press.append(df_json['barrometricPressureMercury'][0])
    temp.append(df_json['airTemperature'][0])
    hum.append(df_json['relativeHumidity'][0])
    

    trace0 = go.Scatter(
                x= list(date_time_pht),
                y= list(press),
                name='Press',
                mode= 'lines+markers'
             )
    trace1 = go.Scatter(
                x= list(date_time_pht),
                y= list(temp),
                name='Temp',
                mode= 'lines+markers'
             )
    trace2 = go.Scatter(
                x= list(date_time_pht),
                y= list(hum),
                name='Hum',
                mode= 'lines+markers'
             )
    data = [trace0,trace1,trace2]
    layout = go.Layout(xaxis = dict(range = [min(date_time_pht),max(date_time_pht)]),yaxis = dict(range = [0,100]))

    fig2=go.Figure(data,layout)
    fig2.update_layout(
                        xaxis_title="Date Time ",
                        yaxis_title="Pressure Temperature and Humidity",
                        plot_bgcolor=app_color["graph_bg"],
                        paper_bgcolor=app_color["graph_bg"],
                        font_color="white",
                        legend_title="PTH",
                        font=dict(
                        color="white"
                            ))
    return fig2

@app.callback(Output('pm-live-graph', 'figure'),[ Input('pm-graph-update', 'n_intervals') ])
def update_graph_pm(n):
    df_json = pd.read_json('mintsData\\rawMQTT\\001e0636e527\\OPCN3.json', lines = True)
 
    date_time_pm.append(df_json['dateTime'][0])

    pm1.append(df_json['pm1'][0])
    pm2_5.append(df_json['pm2_5'][0])
    pm10.append(df_json['pm10'][0])
    

    trace0 = go.Scatter(
                x= list(date_time_pm),
                y= list(pm1),
                name='PM 1',
                mode= 'lines+markers'
             )
    trace1 = go.Scatter(
                x= list(date_time_pm),
                y= list(pm2_5),
                name='PM 2.5',
                mode= 'lines+markers'
             )
    trace2 = go.Scatter(
                x= list(date_time_pm),
                y= list(pm10),
                name='PM 10',
                mode= 'lines+markers'
             )
    data = [trace0,trace1,trace2]
    layout = go.Layout(xaxis = dict(range = [min(date_time_pm),max(date_time_pm)]),yaxis = dict(range = [0,1]))

    fig3=go.Figure(data,layout)
    fig3.update_layout(
                        xaxis_title="Date Time ",
                        yaxis_title="Particulate Matter",
                        plot_bgcolor=app_color["graph_bg"],
                        paper_bgcolor=app_color["graph_bg"],
                        font_color="white",
                        legend_title="PM",
                        font=dict(
                        color="white"
                            ))
    return fig3



@app.callback(Output('co-live-graph', 'figure'),[ Input('co-graph-update', 'n_intervals') ])
def update_graph_co(n):
    df_json = pd.read_json('mintsData\\rawMQTT\\001e0636e527\\MGS001.json', lines = True)
 
    date_time_co.append(df_json['dateTime'][0])

    co.append(df_json['co'][0])

    data = go.Scatter(
        x= list(date_time_co),
        y= list(co),
        name='CO',
        mode= 'lines+markers'
        )
    layout = go.Layout(xaxis = dict(range = [min(date_time_co),max(date_time_co)]),yaxis = dict(range = [min(co),max(co)]))

    fig4=go.Figure(data,layout)
    fig4.update_layout(
                        xaxis_title="Date Time ",
                        yaxis_title="CO",
                        plot_bgcolor=app_color["graph_bg"],
                        paper_bgcolor=app_color["graph_bg"],
                        font_color="white",
                        legend_title="Wind Speed",
                        font=dict(
                        color="white"
                            ))
    return fig4

@app.callback(Output('no2-live-graph', 'figure'),[ Input('no2-graph-update', 'n_intervals') ])
def update_graph_no2(n):
    df_json = pd.read_json('mintsData\\rawMQTT\\001e0636e527\\MGS001.json', lines = True)
 
    date_time_no2.append(df_json['dateTime'][0])

    no2.append(df_json['no2'][0])

    data = go.Scatter(
        x= list(date_time_no2),
        y= list(no2),
        name='NO2',
        mode= 'lines+markers'
        )
    layout = go.Layout(xaxis = dict(range = [min(date_time_no2),max(date_time_no2)]),yaxis = dict(range = [min(no2),max(no2)]))

    fig5=go.Figure(data,layout)
    fig5.update_layout(
                        xaxis_title="Date Time ",
                        yaxis_title="NO2",
                        plot_bgcolor=app_color["graph_bg"],
                        paper_bgcolor=app_color["graph_bg"],
                        font_color="white",
                        legend_title="NO2",
                        font=dict(
                        color="white"
                            ))
    return fig5

@app.callback(Output('c4h10-live-graph', 'figure'),[ Input('c4h10-graph-update', 'n_intervals') ])
def update_graph_c4h10(n):
    df_json = pd.read_json('mintsData\\rawMQTT\\001e0636e527\\MGS001.json', lines = True)
 
    date_time_c4h10.append(df_json['dateTime'][0])

    c4h10.append(df_json['c4h10'][0])

    data = go.Scatter(
        x= list(date_time_c4h10),
        y= list(c4h10),
        name='C4H10',
        mode= 'lines+markers'
        )
    layout = go.Layout(xaxis = dict(range = [min(date_time_c4h10),max(date_time_c4h10)]),yaxis = dict(range = [min(c4h10),max(c4h10)]))

    fig6=go.Figure(data,layout)
    fig6.update_layout(
                        xaxis_title="Date Time ",
                        yaxis_title="C4H10",
                        plot_bgcolor=app_color["graph_bg"],
                        paper_bgcolor=app_color["graph_bg"],
                        font_color="white",
                        legend_title="Wind Speed",
                        font=dict(
                        color="white"
                            ))
    return fig6
    

# @app.callback(Output('map-live-graph', 'figure'),[ Input('map-graph-update', 'n_intervals') ])
# def update_graph_map(n):
#     df_json = pd.read_json('mintsData\\rawMQTT\\001e0636e527\\GPGGA.json', lines = True)
 

#     lat.append(df_json['latitude'][0])
#     lon.append(df_json['longitude'][0])

#     fig7 = px.scatter_mapbox( lat=lat, lon=lon, #hover_name="City", hover_data=["State", "Population"],
#                         color_discrete_sequence=["fuchsia"], zoom=3, height=300)
#     return fig7

if __name__ == '__main__':
	app.run_server()