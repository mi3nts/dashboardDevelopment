

import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
from plotly import tools
import plotly.graph_objs as go
from collections import deque
import numpy as np
import pandas as pd
import time
from collections import OrderedDict
import plotly.express as px
import os
import time
import json

ground_vehicle_path = "mintsData\\referenceMQTT\\001e0610c2e7\\"
df_updated = pd.DataFrame()
l=1000
inter = 5000
date_time_pht= deque(maxlen=l)#date time for pressure temperature and humidity
date_time_pm = deque(maxlen=l)# date time for pm
date_time_o3 = deque(maxlen=l)#date time for o3
date_time_no2 = deque(maxlen=l)#date time for no2
date_time_no = deque(maxlen=l)#date time for no
date_time_nox = deque(maxlen=l)#date time for nox
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
o3 = deque(maxlen=l)#co
no2 = deque(maxlen=l)# no2
no = deque(maxlen=l)# no
nox = deque(maxlen=l)# nox
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
                        html.H4("CAR DASHBOARD", className="app__header__title"),
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
            ############### PM #################### 
            html.Div([
                html.Div(
                    [html.H6("Particulate Matter", className="graph__title")]
                ),
        		dcc.Graph(id = 'pm-live-graph', animate = True),
        		dcc.Interval(
        			id = 'pm-graph-update',
        			interval = inter,
        			n_intervals = 0
        		),
            ],
                className="one-third column graph__container first" #wind__speed__container,
            ),
            
           ############### Bin #################### 
            html.Div([
                    html.Div(
                        [html.H6("Size Distribution", className="graph__title")]
                    ),
            		dcc.Graph(id = 'bin-live-graph', animate = True),
            		dcc.Interval(
            			id = 'bin-graph-update',
            			interval = inter,
            			n_intervals = 0
            		),
                ],
                    className="one-third column graph__container first" #wind__speed__container,
                ),

            
        ############### Contour #################### 
            
            html.Div([
                html.Div(
                    [html.H6("Contour Distribution", className="graph__title")]
                ),
        		dcc.Graph(id = 'contour-live-graph',),# animate = True),
        		dcc.Interval(
        			id = 'contour-graph-update',
        			interval = inter,
        			n_intervals = 0
        		),
            ],
                className="one-third column graph__container first" #wind__speed__container,
            ),
    ]),
    html.Div([   
            ############### NO #################### 
            html.Div([
              html.Div(
                  [html.H6("NO", className="graph__title")]
              ),
      		dcc.Graph(id = 'no-live-graph', animate = True),
      		dcc.Interval(
      			id = 'no-graph-update',
      			interval = inter,
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
      			interval = inter,
      			n_intervals = 0
      		),
          ],
              className="one-third column graph__container first" #wind__speed__container,
          ),
            
########################### NOX #######################             
            html.Div([
                html.Div(
                    [html.H6("NOX", className="graph__title")]
                ),
        		dcc.Graph(id = 'nox-live-graph', animate = True),
        		dcc.Interval(
        			id = 'nox-graph-update',
        			interval = inter,
        			n_intervals = 0
        		),
            ],
                className="one-third column graph__container first" #wind__speed__container,
            ),
                                    
          ]),

     html.Div([
    ##################### Ozone ############################
            html.Div([
                html.Div(
                    [html.H6("O3", className="graph__title")]
                ),
        		dcc.Graph(id = 'o3-live-graph', animate = True),
        		dcc.Interval(
        			id = 'o3-graph-update',
        			interval = inter,
        			n_intervals = 0
        		),
            ],
                className="one-third column graph__container first" #wind__speed__container,
            ),
     ######################## Pressure Temperature Humidity#########################
     
            html.Div([
                html.Div(
                    [html.H6("Pressure Temperature Humidity", className="graph__title")]
                ),
        		dcc.Graph(id = 'pht-live-graph', animate = True),
        		dcc.Interval(
        			id = 'pht-graph-update',
        			interval = inter,
        			n_intervals = 0
        		),
            ],
                className="one-third column graph__container first" #wind__speed__container,
            ),

       ################### Map #########################         
            html.Div([
                        html.Div(
                            [html.H6("Location of the Nodes", className="graph__title")]
                        ),
                		dcc.Graph(id = 'map-live-graph',),# animate = True),
                 		 dcc.Interval(
                  	 		id = 'map-graph-update',
                  	 		interval = inter,
                  	 		n_intervals = 0,

                 		 ),
                    ],
                        className="one-third column graph__container first" #wind__speed__container,
                    ),
                ]),




        ])
	]
)



# @app.callback(Output('wind-live-graph', 'figure'),[ Input('wind-graph-update', 'n_intervals') ])
# def update_graph_wind(n):
#     df_json = pd.read_json('mintsData\\rawMQTT\\001e0636e527\\WIMWV.json', lines = True)
 

#     ws.append(df_json['windSpeed'][0])
#     wa.append(df_json['windAngle'][0])   
#     data = go.Barpolar(
#         r= list(ws),
#         theta= list(wa),
#         name='Wind',
#         #mode= 'lines+markers'
#         )
#     layout = go.Layout(xaxis = dict(range = [min(ws),max(ws)]),yaxis = dict(range = [min(wa),max(wa)]))

#     fig1=go.Figure(data,layout)
#     fig1.update_layout( 
#                         #xaxis_title="Date Time ",
#                         #yaxis_title="Wind Speed (m/s)",
#                         plot_bgcolor=app_color["graph_bg"],
#                         paper_bgcolor=app_color["graph_bg"],
#                         font_color="white",
#                         #legend_title="Wind Speed",
#                         font=dict(
#                         color="white"
#                             ))
#     fig1.update_polars(bgcolor="#2596be")
#     #fig1.update_xaxes(rangeslider_visible=True)
#     return fig1

@app.callback(Output('pht-live-graph', 'figure'),[ Input('pht-graph-update', 'n_intervals') ])
def update_graph_pht(n):
    df_json = pd.read_json(ground_vehicle_path + '2B-BC.json', lines = True)
 
    date_time_pht.append(df_json['dateTime'][0])

    press.append(df_json['pressure'][0])
    temp.append(df_json['temperature'][0]+273)
    hum.append(df_json['humidity'][0])
    fig2 = tools.make_subplots(specs=[[{"secondary_y": True}]])

    fig2.add_trace( go.Scatter(
                x= list(date_time_pht),
                y= list(press),
                name='Pressure',
                mode= 'lines+markers',
                 
             ),secondary_y=True,
        )
    fig2.add_trace( go.Scatter(
                x= list(date_time_pht),
                y= list(temp),
                name='Temperature',
                mode= 'lines+markers'
             ),secondary_y=False,
        )
    fig2.add_trace(go.Scatter(
                x= list(date_time_pht),
                y= list(hum),
                name='Humidity',
                mode= 'lines+markers'
             ),secondary_y=False,
        )
    # data = [trace0,trace1,trace2]
    # layout = go.Layout(xaxis = dict(range = [min(date_time_pht),max(date_time_pht)]),)#yaxis = dict(range = [0,100]))

    # fig2=go.Figure(data,layout)
    fig2.update_layout(
                        xaxis_title="Date Time ",
                        plot_bgcolor=app_color["graph_bg"],
                        paper_bgcolor=app_color["graph_bg"],
                        font_color="white",
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="right",
                            x=1
                            ),
                        font=dict(
                        color="white"
                            ))
    
    fig2.update_yaxes(title_text="Temperature (K) and Humidity (%)",gridcolor='#1B2AAA', secondary_y=False,)#showgrid=False)
    fig2.update_yaxes(title_text="Pressure (hPa)", secondary_y=True,gridcolor='#1B2AAA')#showgrid=False)
    fig2["layout"]["yaxis2"]["showgrid"] = False
    fig2.update_xaxes(tickangle=45,gridcolor='#1B2AAA',showline=True, linecolor= '#1B2AAA', mirror=True)
    return fig2

@app.callback(Output('pm-live-graph', 'figure'),[ Input('pm-graph-update', 'n_intervals') ])
def update_graph_pm(n):
    df_json = pd.read_json('mintsData\\referenceMQTT\\0001c0231d43\\FRG001.json', lines = True)
 
    date_time_pm.append(df_json['dateTime'][0])

    pm1.append(df_json['pm1'][0])
    pm2_5.append(df_json['pm2_5'][0])
    pm10.append(df_json['pm10'][0])
    # df_wide = pd.DataFrame([list(date_time_pm),list(pm1),list(pm2_5),list(pm10)]).transpose()
    # df_wide.columns = ["dateTime","pm1","pm2_5","pm10"]
    # df_long=pd.melt(df_wide, id_vars=['dateTime'], value_vars=['pm1', 'pm2_5', 'pm10'])
    # fig3 = px.scatter(df_long, x='dateTime', y='value', color='variable',marginal_y="histogram")
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
    trace3 = go.Histogram(y=list(pm1),name='PM 1',marker_color='rgb(99,110,250)',)
    trace4 = go.Histogram(y=list(pm2_5),name='PM 2.5',marker_color='rgb(239,85,59)')
    trace5 = go.Histogram(y=list(pm10),name='PM 10',marker_color='rgb(0,204,150)')
    
    fig3 = tools.make_subplots(rows = 2, cols =3,
                                specs=[[{"rowspan":2,"colspan":2}, None,{"rowspan":2} ],
                                       [None, None,None]],
                               horizontal_spacing = 0.2 )
    fig3.append_trace(trace0, 1, 1)
    fig3.append_trace(trace1, 1, 1)
    fig3.append_trace(trace2, 1, 1)
    
    #data = [trace0,trace1,trace2]
    #layout = go.Layout(,)#yaxis = dict(range = [0,1]))

    #fig3=go.Figure(data)
    fig3.append_trace(trace3, 1, 3)
    fig3.append_trace(trace4, 1, 3)
    fig3.append_trace(trace5, 1, 3)
    fig3.update_layout(xaxis = dict(range = [min(date_time_pm),max(date_time_pm)]),
                        xaxis_title="Date Time ",
                        yaxis_title="Particulate Matter (\u03BC"+"g/"+ "m"+"\u00b3"+")",
                        plot_bgcolor=app_color["graph_bg"],
                        paper_bgcolor=app_color["graph_bg"],
                        font_color="white",
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="right",
                            x=1
                            ),
                        bargap = 0.01)
    #fig3.update_xaxes(rangeslider_visible=True)
    fig3.update_xaxes(tickangle=45,gridcolor='#1B2AAA',showline=True, linecolor= '#1B2AAA', mirror=True)
    fig3.update_yaxes(gridcolor='#1B2AAA',showline=True, linecolor= '#1B2AAA', mirror=True)
    return fig3



@app.callback(Output('o3-live-graph', 'figure'),[ Input('o3-graph-update', 'n_intervals') ])
def update_graph_o3(n):
    df_json = pd.read_json(ground_vehicle_path + '2B-O3.json', lines = True)
 
    date_time_o3.append(df_json['dateTime'][0])

    o3.append(df_json['ozone'][0])

    data = go.Scatter(
        x= list(date_time_o3),
        y= list(o3),
        name='O3',
        mode= 'lines+markers'
        )
    layout = go.Layout(xaxis = dict(range = [min(date_time_o3),max(date_time_o3)]),)#yaxis = dict(range = [min(co),max(co)]))

    fig4=go.Figure(data,layout)
    fig4.update_layout(
                        xaxis_title="Date Time ",
                        yaxis_title="O3 (PPB)",
                        plot_bgcolor=app_color["graph_bg"],
                        paper_bgcolor=app_color["graph_bg"],
                        font_color="white",
                     )
    #fig4.update_xaxes(rangeslider_visible=True)
    fig4.update_xaxes(tickangle=45,gridcolor='#1B2AAA',showline=True, linecolor= '#1B2AAA', mirror=True)
    fig4.update_yaxes(gridcolor='#1B2AAA',showline=True, linecolor= '#1B2AAA', mirror=True)
    return fig4

@app.callback(Output('no-live-graph', 'figure'),[ Input('no-graph-update', 'n_intervals') ])
def update_graph_no(n):
    df_json = pd.read_json(ground_vehicle_path + '2B-NOX.json', lines = True)
 
    date_time_no.append(df_json['dateTime'][0])

    no.append(df_json['NO'][0])

    data = go.Scatter(
        x= list(date_time_no),
        y= list(no),
        name='NO',
        mode= 'lines+markers'
        )
    layout = go.Layout(xaxis = dict(range = [min(date_time_no),max(date_time_no)]),)#yaxis = dict(range = [min(c4h10),max(c4h10)]))

    fig5=go.Figure(data,layout)
    fig5.update_layout(
                        xaxis_title="Date Time ",
                        yaxis_title="NO (PPM)",
                        plot_bgcolor=app_color["graph_bg"],
                        paper_bgcolor=app_color["graph_bg"],
                        font_color="white",)
    #fig6.update_xaxes(rangeslider_visible=True)
    fig5.update_xaxes(gridcolor='#1B2AAA',tickangle=45,showline=True, linecolor= '#1B2AAA', mirror=True)
    fig5.update_yaxes(gridcolor='#1B2AAA',showline=True, linecolor= '#1B2AAA', mirror=True)
    return fig5
@app.callback(Output('no2-live-graph', 'figure'),[ Input('no2-graph-update', 'n_intervals') ])
def update_graph_no2(n):
    df_json = pd.read_json(ground_vehicle_path + '2B-NOX.json', lines = True)
 
    date_time_no2.append(df_json['dateTime'][0])

    no2.append(df_json['NO2'][0])

    data = go.Scatter(
        x= list(date_time_no2),
        y= list(no2),
        name='NO2',
        mode= 'lines+markers'
        )
    layout = go.Layout(xaxis = dict(range = [min(date_time_no2),max(date_time_no2)]),)#yaxis = dict(range = [min(no2),max(no2)]))

    fig6=go.Figure(data,layout)
    fig6.update_layout(
                        xaxis_title="Date Time ",
                        yaxis_title="NO2 (PPM)",
                        plot_bgcolor=app_color["graph_bg"],
                        paper_bgcolor=app_color["graph_bg"],
                        font_color="white",
                        legend_title="NO2",
                        font=dict(
                        color="white"
                            ))
    fig6.update_xaxes(gridcolor='#1B2AAA',tickangle=45,showline=True, linecolor= '#1B2AAA', mirror=True)
    fig6.update_yaxes(gridcolor='#1B2AAA',showline=True, linecolor= '#1B2AAA', mirror=True)
    #fig5.update_xaxes(rangeslider_visible=True)

    return fig6


@app.callback(Output('nox-live-graph', 'figure'),[ Input('nox-graph-update', 'n_intervals') ])
def update_graph_nox(n):
    df_json = pd.read_json(ground_vehicle_path + '2B-NOX.json', lines = True)
 
    date_time_nox.append(df_json['dateTime'][0])

    nox.append(df_json['NOX'][0])

    data = go.Scatter(
        x= list(date_time_no2),
        y= list(nox),
        name='NOX',
        mode= 'lines+markers'
        )
    layout = go.Layout(xaxis = dict(range = [min(date_time_nox),max(date_time_nox)]),)#yaxis = dict(range = [min(no2),max(no2)]))

    fig7=go.Figure(data,layout)
    fig7.update_layout(
                        xaxis_title="Date Time ",
                        yaxis_title="NOX (PPM)",
                        plot_bgcolor=app_color["graph_bg"],
                        paper_bgcolor=app_color["graph_bg"],
                        font_color="white",
                        legend_title="NOX",
                        font=dict(
                        color="white"
                            ))
    fig7.update_xaxes(gridcolor='#1B2AAA',tickangle=45,showline=True, linecolor= '#1B2AAA', mirror=True)
    fig7.update_yaxes(gridcolor='#1B2AAA',showline=True, linecolor= '#1B2AAA', mirror=True)
    #fig5.update_xaxes(rangeslider_visible=True)

    return fig7
    
@app.callback(Output('bin-live-graph', 'figure'),[ Input('bin-graph-update', 'n_intervals') ])
def update_graph_bin(n):
    df_json = pd.read_json('mintsData\\referenceMQTT\\0001c0231d43\\FRG001.json', lines = True)
    df_json = df_json.iloc[:,7:101]
    bin_ls = list(df_json.iloc[0])
    
    df_frg_lt = pd.read_csv('frg_limits.csv',delim_whitespace=True,header = None)
    df_frg_lt.drop([0,3],axis = 1)
    bin_boundries_low = list(df_frg_lt[1])+list(df_frg_lt[4])
    bin_boundries_high = list(df_frg_lt[2])+list(df_frg_lt[5])
    bin_boundries_avg = list((np.add(bin_boundries_high , bin_boundries_low))/2)
    #bin_boundries_high = [.46,.66,1,1.3,1.7,2.3,3.0,4.0,5.2,6.5,8,10,12,14,16,18,20,22,25,28,31,34,37,40]
    #bin_boundries_low  = [0.35,.46,.66,1,1.3,1.7,2.3,3.0,4.0,5.2,6.5,8,10,12,14,16,18,20,22,25,28,31,34,37]
    #bin_boundries_avg = list((np.add(bin_boundries_high , bin_boundries_low))/2)  
    #bin_ls = list(range(0,94))
    bin_len = [i if i != -1 else 0 for i in bin_ls]
    if (set(bin_len) == {0}):
       x_limit = 5
    else:    
        x_range = [i for i, e in enumerate(bin_len) if e != 0]
        x_limit = bin_boundries_avg[max(x_range)] 
    data = go.Bar(
        x = bin_boundries_avg,
        y = bin_len,
        name='Distribution',
        #mode= 'lines+markers'
        )
    layout = go.Layout(xaxis = dict(range = [0,x_limit]),)#yaxis = dict(range = [min(ws),max(ws)]))

    fig1=go.Figure(data,layout)
    fig1.update_layout( 
                        xaxis_title="Bins",
                        yaxis_title="Size (\u03BC"+ "m) ",
                        plot_bgcolor=app_color["graph_bg"],
                        paper_bgcolor=app_color["graph_bg"],
                        font_color="white",
                        legend_title="OPCN3",
                        font=dict(
                        color="white"
                            ),bargap=0,
                            bargroupgap = 0)
    fig1.update_xaxes(gridcolor='#1B2AAA',showline=True, linecolor= '#1B2AAA', mirror=True)
    fig1.update_yaxes(gridcolor='#1B2AAA',showline=True, linecolor= '#1B2AAA', mirror=True)
    return fig1

@app.callback(Output('contour-live-graph', 'figure'),[ Input('contour-graph-update', 'n_intervals') ])
def update_graph_contour(n):
    # if file does not exist write header
    # time.sleep(5)
    
    df_json = pd.read_json('mintsData\\referenceMQTT\\0001c0231d43\\FRG001.json', lines = True)    #print(df_json)
    global df_updated
    df_updated = df_updated.append(df_json,ignore_index = True)
    df_updated = df_updated.drop_duplicates()
    #print("SDASDAD",df_updated)
    if(len(df_updated)>1):
        date_time_contour=list(df_updated['dateTime'])
    
        df_bins = df_updated.iloc[:,7:101].T
        df_bins_log = np.log10(df_bins).replace(-np.inf, np.finfo(float).eps)
        list_bins = df_bins_log.values.tolist()
        
        df_frg_lt = pd.read_csv('frg_limits.csv',delim_whitespace=True,header = None)
        df_frg_lt.drop([0,3],axis = 1)
        bin_boundries_low = list(df_frg_lt[1])+list(df_frg_lt[4])
        bin_boundries_high = list(df_frg_lt[2])+list(df_frg_lt[5])
        bin_boundries_avg_size = list((np.add(bin_boundries_high , bin_boundries_low))/2)
        print("z",list_bins[0][0:5], len(list_bins[0]))
        print("date",date_time_contour[0:5])
        #print("avg",bin_boundries_avg_size[0:2])
        data = go.Figure(data =
            go.Contour(
                z=list_bins,
                x=date_time_contour,
                y=bin_boundries_avg_size, # vertical axis
                contours_showlines=False,
                colorscale = "Jet",
                        colorbar=dict(
                                     title='Log(Count)')
                ))
        
        #layout = go.Layout(yaxis = dict(range = [min(bin_boundries_avg_size),max(bin_boundries_avg_size)]),)#yaxis = dict(range = [min(ws),max(ws)]))

        fig8=go.Figure(data,)#layout)
        fig8.update_layout( 
                            yaxis = dict(
                                    #tickmode = 'array',
                                    tickvals = [bin_boundries_avg_size[i] for i in range(0,len(bin_boundries_avg_size),15)],

                            ),
                            yaxis_type ="log",
                            xaxis_title="Date Time ",
                            yaxis_title="Size (\u03BC"+ "m)",
                            plot_bgcolor=app_color["graph_bg"],
                            paper_bgcolor=app_color["graph_bg"],
                            font_color="white",
                            #line = list(width = 0),
                            # font=dict(
                            # color="white"
                            # )
                          )
        fig8.update_xaxes(gridcolor='#1B2AAA',tickangle = 45,showline=True, linecolor= '#1B2AAA', mirror=True)
        fig8.update_yaxes(gridcolor='#1B2AAA',showline=True, linecolor= '#1B2AAA', mirror=True,rangemode="tozero")

        return fig8

@app.callback(Output('map-live-graph', 'figure'),[ Input('map-graph-update', 'n_intervals') ])
def update_graph_map(n):
    df_json = pd.read_json('mintsData\\referenceMQTT\\001e0610c2e7\\GPSGPGGA1.json', lines = True)
    if(df_json['latitudeDirection'][0] == 'S'):
        lat.append(-1*(np.ceil(df_json['latitude'][0]/100) + np.remainder(df_json['latitude'][0],100)/60)) 
    else:
          lat.append((np.ceil(df_json['latitude'][0]/100) + np.remainder(df_json['latitude'][0],100)/60)) 
    
        
    if(df_json['longitudeDirection'][0] == 'S'):
        lon.append(-1*(np.ceil(df_json['longitude'][0]/100) + np.remainder(df_json['longitude'][0],100)/60)) 
    else:
          lon.append(-1*(np.ceil(df_json['longitude'][0]/100) + np.remainder(df_json['longitude'][0],100)/60)) 
    
    fig9 = px.scatter_mapbox(lat=list(lat), lon=list(lon), #hover_name="City", hover_data=["State", "Population"],
                        color_discrete_sequence=["fuchsia"], zoom=3, height=300)
    fig9.update_layout(mapbox_style="open-street-map", margin={"r":0,"t":0,"l":0,"b":0})
    return fig9

if __name__ == '__main__':
	app.run_server()