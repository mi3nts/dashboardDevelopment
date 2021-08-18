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
import plotly.express as px


l=1000

date_time_pht= deque(maxlen=l)#date time for pressure temperature and humidity
date_time_pm = deque(maxlen=l)# date time for pm
date_time_co = deque(maxlen=l)#date time for co
date_time_no2 = deque(maxlen=l)#date time for no2
date_time_c4h10 = deque(maxlen=l)#date time for c4h10
date_time_bin = deque(maxlen=l)
date_time_contour = deque(maxlen=l)

ws = deque(maxlen=l)#wind speed
wa = deque(maxlen=l)#wind angle
press = deque(maxlen=l)# pressure
temp = deque(maxlen=l)# temperature
hum = deque(maxlen=l)# humidity
pm1 = deque(maxlen=l)#pm 1
pm2_5 = deque(maxlen=l)# pm 2.5
pm10 = deque(maxlen=l)# pm 10
co = deque(maxlen=l)#co
no2 = deque(maxlen=l)# no2
c4h10 = deque(maxlen=l)# c4h10
lat = deque(maxlen=l)# lat
lon = deque(maxlen=l)# lon
#bin_len = deque(maxlen=l)# lon

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
                    [html.H6("Wind Direction", className="graph__title")]
                ),
        		dcc.Graph(id = 'wind-live-graph', animate = True),
        		dcc.Interval(
        			id = 'wind-graph-update',
        			interval = 1000,
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
    ##################### Bin ############################
    html.Div([
        html.Div([
                html.Div(
                    [html.H6("Bin Distribution", className="graph__title")]
                ),
        		dcc.Graph(id = 'bin-live-graph', animate = True),
        		dcc.Interval(
        			id = 'bin-graph-update',
        			interval = 5000,
        			n_intervals = 0
        		),
            ],
                className="one-third column graph__container first" #wind__speed__container,
            ),
    ######################## Contour #########################    
                html.Div([
                html.Div(
                    [html.H6("Contour Distribution", className="graph__title")]
                ),
        		dcc.Graph(id = 'contour-live-graph', animate = True),
        		dcc.Interval(
        			id = 'contour-graph-update',
        			interval = 1000,
        			n_intervals = 0
        		),
            ],
                className="one-third column graph__container first" #wind__speed__container,
            ),
                
            html.Div([
                        html.Div(
                            [html.H6("Location of the Nodes", className="graph__title")]
                        ),
                		dcc.Graph(id = 'map-live-graph', animate = True),
                		# dcc.Interval(
                 	# 		id = 'map-graph-update',
                 	# 		interval = 5000,
                 	# 		n_intervals = 0
                		# ),
                    ],
                        className="one-third column graph__container first" #wind__speed__container,
                    ),
                ]),


                
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
	]
)

@app.callback(Output('wind-live-graph', 'figure'),[ Input('wind-graph-update', 'n_intervals') ])
def update_graph_wind(n):
    df_json = pd.read_json('mintsData\\rawMQTT\\001e0636e527\\WIMWV.json', lines = True)
 

    ws.append(df_json['windSpeed'][0])
    wa.append(df_json['windAngle'][0])   
    data = go.Barpolar(
        r= list(ws),
        theta= list(wa),
        name='Wind',
        #mode= 'lines+markers'
        )
    layout = go.Layout(xaxis = dict(range = [min(ws),max(ws)]),yaxis = dict(range = [min(wa),max(wa)]))

    fig1=go.Figure(data,layout)
    fig1.update_layout( 
                        #xaxis_title="Date Time ",
                        #yaxis_title="Wind Speed (m/s)",
                        plot_bgcolor=app_color["graph_bg"],
                        paper_bgcolor=app_color["graph_bg"],
                        font_color="white",
                        #legend_title="Wind Speed",
                        font=dict(
                        color="white"
                            ))
    fig1.update_polars(bgcolor="#2596be")
    #fig1.update_xaxes(rangeslider_visible=True)
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
    layout = go.Layout(xaxis = dict(range = [min(date_time_pht),max(date_time_pht)]),)#yaxis = dict(range = [0,100]))

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
    #fig2.update_xaxes(rangeslider_visible=True)
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
                mode= 'lines+markers'#,marginal_y="histogram"
             )
    trace1 = go.Scatter(
                x= list(date_time_pm),
                y= list(pm2_5),
                name='PM 2.5',
                mode= 'lines+markers'#,marginal_y="histogram"
             )
    trace2 = go.Scatter(
                x= list(date_time_pm),
                y= list(pm10),
                name='PM 10',
                mode= 'lines+markers'#,marginal_y="histogram"
             )
    data = [trace0,trace1,trace2]
    layout = go.Layout(xaxis = dict(range = [min(date_time_pm),max(date_time_pm)]),)#yaxis = dict(range = [0,1]))

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
    #fig3.update_xaxes(rangeslider_visible=True)
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
    layout = go.Layout(xaxis = dict(range = [min(date_time_co),max(date_time_co)]),)#yaxis = dict(range = [min(co),max(co)]))

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
    #fig4.update_xaxes(rangeslider_visible=True)
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
    layout = go.Layout(xaxis = dict(range = [min(date_time_no2),max(date_time_no2)]),)#yaxis = dict(range = [min(no2),max(no2)]))

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
    #fig5.update_xaxes(rangeslider_visible=True)
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
    layout = go.Layout(xaxis = dict(range = [min(date_time_c4h10),max(date_time_c4h10)]),)#yaxis = dict(range = [min(c4h10),max(c4h10)]))

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
    #fig6.update_xaxes(rangeslider_visible=True)
    return fig6
    
@app.callback(Output('bin-live-graph', 'figure'),[ Input('bin-graph-update', 'n_intervals') ])
def update_graph_bin(n):
    df_json = pd.read_json('mintsData\\rawMQTT\\001e0636e527\\OPCN3.json', lines = True)
    df_json = df_json.iloc[:,2:26]
    bin_len = list(df_json.iloc[0])
    bin_boundries_high = [.46,.66,1,1.3,1.7,2.3,3.0,4.0,5.2,6.5,8,10,12,14,16,18,20,22,25,28,31,34,37,40]
    bin_boundries_low  = [0.35,.46,.66,1,1.3,1.7,2.3,3.0,4.0,5.2,6.5,8,10,12,14,16,18,20,22,25,28,31,34,37]
    bin_boundries_avg = list((np.add(bin_boundries_high , bin_boundries_low))/2)  
    data = go.Bar(
        x = bin_boundries_avg,
        y = bin_len,
        name='Distribution',
        #mode= 'lines+markers'
        )
    layout = go.Layout(xaxis = dict(range = [0,5]),)#yaxis = dict(range = [min(ws),max(ws)]))

    fig7=go.Figure(data,layout)
    fig7.update_layout( 
                        #xaxis_title="Date Time ",
                        #yaxis_title="Wind Speed (m/s)",
                        plot_bgcolor=app_color["graph_bg"],
                        paper_bgcolor=app_color["graph_bg"],
                        font_color="white",
                        legend_title="OPCN3",
                        font=dict(
                        color="white"
                            ),bargap=0,
                            bargroupgap = 0)
    #fig7.update_polars(bgcolor="#2596be")
    #fig1.update_xaxes(rangeslider_visible=True)
    return fig7

@app.callback(Output('contour-live-graph', 'figure'),[ Input('contour-graph-update', 'n_intervals') ])
def update_graph_contour(n):
    df_json = pd.read_json('mintsData\\rawMQTT\\001e0636e527\\OPCN3.json', lines = True)
    date_time_contour.append(df_json['dateTime'][0])
    df_json = df_json.iloc[:,2:26]
    bin_len = list(df_json.iloc[0])
    bin_len_new = [np.finfo(float).eps if x==0 else x for x in bin_len]
    bin_len_log = list(np.log10(bin_len_new))
    bin_boundries_high = [.46,.66,1,1.3,1.7,2.3,3.0,4.0,5.2,6.5,8,10,12,14,16,18,20,22,25,28,31,34,37,40]
    bin_boundries_low  = [0.35,.46,.66,1,1.3,1.7,2.3,3.0,4.0,5.2,6.5,8,10,12,14,16,18,20,22,25,28,31,34,37]
    bin_boundries_avg_size = list((np.add(bin_boundries_high , bin_boundries_low))/2)  
    data = go.Contour(
        z = bin_len_log,
        x = list(date_time_contour),
        y = bin_boundries_avg_size,
        #name='Distribution',
        colorscale = 'Electric',
                colorbar=dict(
            title="Count"
        )
        #mode= 'lines+markers'
        ),
    
    layout = go.Layout(xaxis = dict(range = [min(date_time_contour),max(date_time_contour)]),)#yaxis = dict(range = [min(c4h10),max(c4h10)]))

    fig8=go.Figure(data,layout)#,layout)
    fig8.update_layout( 
                        xaxis_title="Date Time ",
                        yaxis_title="Size",
                        #plot_bgcolor=app_color["graph_bg"],
                        paper_bgcolor=app_color["graph_bg"],
                        font_color="white",
                        font=dict(
                        color="white"
                        )
                      )

    return fig8
# @app.callback(Output('map-live-graph', 'figure'),[ Input('map-graph-update', 'n_intervals') ])
# def update_graph_map(n):
# df_json = pd.read_json('mintsData\\rawMQTT\\001e0636e527\\GPGGA.json', lines = True)


# lat.append(df_json['latitude'][0])
# lon.append(df_json['longitude'][0])

# fig9 = px.scatter_mapbox( df , lat=[lat[0]], lon=[lon[0]], #hover_name="City", hover_data=["State", "Population"],
#                     color_discrete_sequence=["fuchsia"], zoom=3, height=300)
# fig9.update_layout(mapbox_style="open-street-map", margin={"r":0,"t":0,"l":0,"b":0})
     # return fig9

if __name__ == '__main__':
	app.run_server()