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

x = deque(maxlen=20)

y = deque(maxlen=20)


app = dash.Dash(__name__)

app.layout = html.Div(
	[
		dcc.Graph(id = 'live-graph', animate = True),
		dcc.Interval(
			id = 'graph-update',
			interval = 5000,
			n_intervals = 0
		),
	]
)

@app.callback(
	Output('live-graph', 'figure'),
	[ Input('graph-update', 'n_intervals') ]
)

def update_graph_scatter(n):
    df_json = pd.read_json('mintsData\\rawMQTT\\001e0636e527\\WIMWV.json', lines = True)
    # if df_json.empty:
    #print("chumma",df_json['dateTime'][0])    
    #time.sleep(5)
    #display()
 
    x.append(df_json['dateTime'][0])
    #X = list(OrderedDict.fromkeys(x)) 
    #print (X)
    #X=set(x)
    #if(x[0] == 0):

    y.append(df_json['windSpeed'][0])
    #Y = list(OrderedDict.fromkeys(y)) 
    #print (Y)
    #Y = set(y)
    #if(y[0] == 0):
    #    y.pop(0)
    data = plotly.graph_objs.Scatter(
        x= list(x),
        y= list(y),
        name='Scatter',
        mode= 'lines+markers'
        )
    
    return {'data': [data],
            'layout' : go.Layout(xaxis = dict(range = [min(x),max(x)]),yaxis = dict(range = [min(y),max(y)]))}

if __name__ == '__main__':
	app.run_server()
