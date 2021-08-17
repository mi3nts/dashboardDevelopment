import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
from collections import deque
import pandas as pd


X = deque(maxlen = 20)
X.append(1)

Y = deque(maxlen = 20)
Y.append(1)

app = dash.Dash(__name__)

app.layout = html.Div(
	[
		dcc.Graph(id = 'live-graph', animate = True),
		dcc.Interval(
			id = 'graph-update',
			interval = 1000,
			n_intervals = 0
		),
	]
)

@app.callback(
	Output('live-graph', 'figure'),
	[ Input('graph-update', 'n_intervals') ]
)

def update_graph_scatter(n):
    df_json = pd.read_json('mintsData\\rawMQTT\\001e0636e527\\BME280.json', lines = True)
    #df_json['dateTime'] = pd.to_datetime(df_json['dateTime']).floor('D')
    X.append(df_json['dateTime'][0].to_pydatetime())
    Y.append(df_json['pressure'][0])
    
    data = plotly.graph_objs.Scatter(
        x=list(X),
        y=list(Y),
        name='Scatter',
        mode= 'lines+markers'
        )
    
    return {'data': [data],
            'layout' : go.Layout(xaxis=dict(range=[min(X),max(X)]),yaxis = dict(range = [min(Y),max(Y)]),)}

if __name__ == '__main__':
	app.run_server()
