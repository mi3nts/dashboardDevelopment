# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.read_csv('47cb5580002e004a_2021-06-17.csv')




app.layout = html.Div(children=[
    html.H1(children = 'LoRa DashBoard' , style = {'textAlign':'center'}),
    html.H4(children = 'Daily updates on LoRa' , style = {'textAlign':'center'}),
    html.Div('Select from list'),
    
    dcc.Dropdown(id = 'pollutant-dropdown',
                 options = [{'label':c,'value':c} for c in df.columns[2:]],
                 value = df.columns[2],
                 clearable = 'True',
                 style = {'width':'50%'}),
   
    dcc.Graph(
        id='timeseries-plots',style = {'width':'50%'}
    )
])
             
@app.callback(
    Output("timeseries-plots", "figure"), 
    [Input("pollutant-dropdown", "value")])

def display_timeseries(pollutant_dropdown):
             fig = px.line(df, x="dateTime", y=pollutant_dropdown,
                           labels={"dateTime": " Date (Month day, Year and time)"})
             fig.update_xaxes(rangeslider_visible=True)
             return fig
# @app.callback(
#      Output(component_id='timeseries-plots', component_property='figure'),
#      Input(component_id='pollutant-dropdown', component_property='value')
# )


# def update_graph(dpdn_val):
#     if len(dpdn_val) > 0:
#         fig = px.xline(df, dimensions=dpdn_val,
#                                 hover_data={'State':True, 'population':':,'})
#         fig.update_traces(diagonal_visible=False, showupperhalf=True, showlowerhalf=True)
#         fig.update_layout(yaxis1={'title':{'font':{'size':3}}}, yaxis2={'title':{'font':{'size':3}}},
#                           yaxis3={'title':{'font':{'size':3}}}, yaxis4={'title':{'font':{'size':3}}},
#                           yaxis5={'title':{'font':{'size':3}}}, yaxis6={'title':{'font':{'size':3}}},
#                           yaxis7={'title':{'font':{'size':3}}}, yaxis8={'title':{'font':{'size':3}}}
#                           )
#         fig.update_layout(xaxis1={'title':{'font':{'size':3}}}, xaxis2={'title':{'font':{'size':3}}},
#                           xaxis3={'title':{'font':{'size':3}}}, xaxis4={'title':{'font':{'size':3}}},
#                           xaxis5={'title':{'font':{'size':3}}}, xaxis6={'title':{'font':{'size':3}}},
#                           xaxis7={'title':{'font':{'size':3}}}, xaxis8={'title':{'font':{'size':3}}}
#                           )
#         return False, fig

#     if len(dpdn_val)==0:
#         return True, dash.no_update

             
if __name__ == '__main__':
    app.run_server(debug=False)