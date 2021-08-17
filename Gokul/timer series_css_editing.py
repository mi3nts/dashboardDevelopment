import plotly.graph_objects as go # or plotly.express as px
import pandas as pd
import sys
sys.path.insert(0,'C:\\Users\\balag\\AppData\\Local\\Packages\\CanonicalGroupLimited.UbuntuonWindows_79rhkp1fndgsc\\LocalState\\rootfs\\home\\gokulbalagopal\\mqttSubscribers\\firmware')
from mintsXU4 import mintsDefinitions as mD
from mintsXU4 import mintsLatest as mL
import plotly.figure_factory as ff
import plotly.express as px
#data_new = mL.readJSONLatestAllMQTT("001e0636e527","YXXDR")[0]
#import carRoofDataRead

df_json = pd.read_json('mintsData\\rawMQTT\\001e0636e527\\BME280.json', lines = True)
df = pd.read_csv('47cb5580002e004a_2021-06-17.csv')
print(df)
cols = list(df.columns)
pm_cols = ['P1_conc','P2_conc']
gas_cols = cols[2:10]+['CO2']
pht_cols = ['Pressure','Humidity','Temperature']


#@app.callback(
#    Output("timeseries-plots", "figure"))

data = [go.Scatter(x = df.dateTime, 
                   y = df[c],
                   mode = 'lines',
                   name = c)for c in pm_cols]


fig1 = go.Figure(data=data)
fig1.update_xaxes(rangeslider_visible=True)
#fig.add_trace(go.Scatter(x=df.P1_conc, y=df.dateTime,
#                    mode='markers', name='markers'))



##################### Distribution Plots ########################

fig2 = ff.create_distplot([df['P1_conc'],df['P2_conc']],pm_cols)
fig2.update_layout(
title= "PM Concentrtion Distribution",
hovermode ='closest')

##################### Ammonia  ####################
data = [go.Scatter(x = df.dateTime, 
                   y = df["NH3"],
                   mode = 'lines',
                   name = "Ammonia")]


fig3 = go.Figure(data=data)
fig3.update_xaxes(rangeslider_visible=True)

################### CO2 ##########################
data = [go.Scatter(x = df.dateTime, 
                   y = df["CO2"],
                   mode = 'lines',
                   name = "CO2")]


fig4 = go.Figure(data=data)
fig4.update_xaxes(rangeslider_visible=True)

################### CO ###########################
data = [go.Scatter(x = df.dateTime, 
                   y = df["CO"],
                   mode = 'lines',
                   name = "CO")]


fig5 = go.Figure(data=data)
fig5.update_xaxes(rangeslider_visible=True)

################### Pressure Humidity Temperature ###########################
data = [go.Scatter(x = df.dateTime, 
                   y = df[c],
                   mode = 'lines',
                   name = c)for c in pht_cols]


fig6 = go.Figure(data=data)
fig6.update_xaxes(rangeslider_visible=True)

######################### map ########################
fig7 = px.scatter_mapbox(df, lat="Latitude", lon="Longitude", #hover_name="City", hover_data=["State", "Population"],
                        color_discrete_sequence=["fuchsia"], zoom=3, height=300)
#fig7.update_layout(mapbox_style="open-street-map",margin={"r":0,"t":0,"l":0,"b":0})


import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash(__name__
                #,
                #meta_tags=[{"name": "viewport", 
                 #           "content": "width=device-width, initial-scale=1"}],
               )
app_color = {"graph_bg": "#082255", "graph_line": "#007ACE"}
app.title = 'LoRa DashBoard'

app.layout = html.Div(
    [
        # header
        html.Div(
            [
                html.Div(
                    [
                        html.H4("LORA DASHBOARD", className="app__header__title"),
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
#### from#####
        html.Div(
            [
                # wind speed
                html.Div(
                    [
                        html.Div(
                            [html.H6("Particulate Matter", className="graph__title")]
                        ),
                        dcc.Graph(
                            id="PM-timeseries",
                            figure=fig1.update_layout(
                                    xaxis_title="Date Time ",
                                    yaxis_title="PM",
                                    plot_bgcolor=app_color["graph_bg"],
                                    paper_bgcolor=app_color["graph_bg"],
                                    font_color="white",
                                    legend_title="PM Concentrations",
                                    font=dict(
                                    color="white"
                                )),
                        ),
                        # dcc.Interval(
                        #     id="wind-speed-update",
                        #     interval=int(GRAPH_INTERVAL),
                        #     n_intervals=0,
                        # ),
                    ],
                    className="one-third column graph__container first" #wind__speed__container,
                ),

                        # histogram
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6(
                                            "PM HISTOGRAM",
                                            className="graph__title",
                                        )
                                    ]
                                ),

                                dcc.Graph(
                                        id="PM-histogram",
                                        figure=fig2.update_layout(
                                                    xaxis_title="Date Time ",
                                                    yaxis_title="PM",
                                                    plot_bgcolor=app_color["graph_bg"],
                                                    paper_bgcolor=app_color["graph_bg"],
                                                    font_color="white",
                                                    legend_title="PM Concentrations",
                                                    font=dict(
                                                        color="white"
                                                    )
                                        )
                                ),
                            ],
                            className="one-third column graph__container first",
                        ),
                        # wind direction
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6(
                                            "Ammonia", className="graph__title",
                                            
                                        )
                                    ]
                                ),
                                dcc.Graph(
                                    id="Ammonia-timeseries",
                                    figure=fig3.update_layout(
                                            xaxis_title="Date Time ",
                                            yaxis_title="Ammonia Concentration",
                                            plot_bgcolor=app_color["graph_bg"],
                                            paper_bgcolor=app_color["graph_bg"],
                                            font_color="white",
                                            legend_title="Ammonia ",
                                            font=dict(
                                            color="white"
                                        )),
                                ),
                            ],
                            className="one-third column graph__container first",

                ),
                
            ],
            #className="app__content",
        ),
        html.Div(
            [
                # wind speed
                html.Div(
                    [
                        html.Div(
                            [html.H6("CO2 Time Series", className="graph__title")]
                        ),
                        dcc.Graph(
                            id="CO2-timeseries",
                            figure=fig4.update_layout(
                                    xaxis_title="Date Time ",
                                    yaxis_title="CO2",
                                    plot_bgcolor=app_color["graph_bg"],
                                    paper_bgcolor=app_color["graph_bg"],
                                    font_color="white",
                                    legend_title="CO2 Concentrations",
                                    font=dict(
                                    color="white"
                                )),
                        ),
                        # dcc.Interval(
                        #     id="wind-speed-update",
                        #     interval=int(GRAPH_INTERVAL),
                        #     n_intervals=0,
                        # ),
                    ],
                    className="one-third column graph__container first" #wind__speed__container,
                ),

                        # histogram
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6(
                                            "CO Time Series",
                                            className="graph__title",
                                        )
                                    ]
                                ),

                                dcc.Graph(
                                        id="CO-timeseries",
                                        figure=fig5.update_layout(
                                                    xaxis_title="Date Time ",
                                                    yaxis_title="CO",
                                                    plot_bgcolor=app_color["graph_bg"],
                                                    paper_bgcolor=app_color["graph_bg"],
                                                    font_color="white",
                                                    legend_title="CO Concentration",
                                                    font=dict(
                                                        color="white"
                                                    )
                                        )
                                ),
                            ],
                            className="one-third column graph__container first",
                        ),
                        # wind direction
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6(
                                            "PHT", className="graph__title",
                                            
                                        )
                                    ]
                                ),
                                dcc.Graph(
                                    id="PHT-timeseries",
                                    figure=fig6.update_layout(
                                            xaxis_title="Date Time ",
                                            yaxis_title="PHT Concentration",
                                            plot_bgcolor=app_color["graph_bg"],
                                            paper_bgcolor=app_color["graph_bg"],
                                            font_color="white",
                                            legend_title="PHT ",
                                            font=dict(
                                            color="white"
                                        )),
                                ),
                            ],
                            className="one-third column graph__container first",

                ),
                
            ],
            #className="app__content",
        ),
                html.Div(
            [
                # wind speed
                html.Div(
                    [
                        html.Div(
                            [html.H6("CO2 Time Series", className="graph__title")]
                        ),
                        dcc.Graph(
                            id="CO2-timeseries 1",
                            figure=fig4.update_layout(
                                    xaxis_title="Date Time ",
                                    yaxis_title="CO2",
                                    plot_bgcolor=app_color["graph_bg"],
                                    paper_bgcolor=app_color["graph_bg"],
                                    font_color="white",
                                    legend_title="CO2 Concentrations",
                                    font=dict(
                                    color="white"
                                )),
                        ),
                        # dcc.Interval(
                        #     id="wind-speed-update",
                        #     interval=int(GRAPH_INTERVAL),
                        #     n_intervals=0,
                        # ),
                    ],
                    className="one-third column graph__container first" #wind__speed__container,
                ),

                        # histogram
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6(
                                            "CO Time Series",
                                            className="graph__title",
                                        )
                                    ]
                                ),

                                dcc.Graph(
                                        id="CO-timeseries 1 ",
                                        figure=fig5.update_layout(
                                                    xaxis_title="Date Time ",
                                                    yaxis_title="CO",
                                                    plot_bgcolor=app_color["graph_bg"],
                                                    paper_bgcolor=app_color["graph_bg"],
                                                    font_color="white",
                                                    legend_title="CO Concentration",
                                                    font=dict(
                                                        color="white"
                                                    )
                                        )
                                ),
                            ],
                            className="one-third column graph__container first",
                        ),
                        # wind direction
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6(
                                            "Location of Nodes", className="graph__title"
                                        )
                                    ]
                                ),
                                dcc.Graph(
                                    id="node-location",
                                    figure=fig7.update_layout(mapbox_style="open-street-map", margin={"r":0,"t":0,"l":0,"b":0}),
                                ),
                            ],
                            className="one-third column graph__container first",
                        ),
                
            ],
            #className="app__content",
        ),
####### tooo
####### tooo        

    ],
    #className="app__container",
)


app.run_server(debug=False)
    