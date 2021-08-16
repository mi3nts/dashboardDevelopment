# -*- coding: utf-8 -*-
"""
Created on Sun Aug 15 19:08:41 2021

@author: balag
"""

import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go # or plotly.express as px
import pandas as pd
import sys
sys.path.insert(0,'C:\\Users\\balag\\AppData\\Local\\Packages\\CanonicalGroupLimited.UbuntuonWindows_79rhkp1fndgsc\\LocalState\\rootfs\\home\\gokulbalagopal\\mqttSubscribers\\firmware')
#from mintsXU4 import mintsDefinitions as mD
#from mintsXU4 import mintsLatest as mL
import plotly.figure_factory as ff
import plotly.express as px
from dash.dependencies import Input, Output

tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}

df = pd.read_csv('47cb5580002e004a_2021-06-17.csv')
cols = list(df.columns)
pm_cols = ['P1_conc','P2_conc']
gas_cols = cols[2:10]+['CO2']
pht_cols = ['Pressure','Humidity','Temperature']



app = dash.Dash(__name__)
app_color = {"graph_bg": "#082255", "graph_line": "#007ACE"}
app.layout = html.Div([
        html.Div(
        [
            html.Div(
                [
                    html.H4("LORA DASHBOARD", className="app__header__title"),
                    html.P(
                        "This app continually monitors wind speed, pollutant concentration.",
                        className="app__header__title--grey",
                    ),
                ],
                className="app__header__desc",
            ),

        ],
        className="app__header",
    ),
    dcc.Tabs(
        id="tabs-with-classes",
        value='day',
        parent_className='custom-tabs',
        className='custom-tabs-container',
        children=[
            dcc.Tab(
                label='Daily',
                value='day',
                style=tab_style, selected_style=tab_selected_style
            ),
            dcc.Tab(
                label='Weekly',
                value='week',
                style=tab_style, selected_style=tab_selected_style
            ),
            dcc.Tab(
                label='Monthly',
                value='month', style=tab_style, selected_style=tab_selected_style
            ),
            dcc.Tab(
                label='Yearly',
                value='year',
                style=tab_style, selected_style=tab_selected_style
            ),
        ]),
    html.Div(id='tabs-content-classes')
])


@app.callback(Output('tabs-content-classes', 'children'),
              Input('tabs-with-classes', 'value'))
def render_content(tab):
    if tab == 'day':
        data = [go.Scatter(x = df.dateTime, 
                   y = df[c],
                   mode = 'lines',
                   name = c)for c in pm_cols]
    
    
        fig1 = go.Figure(data=data)
        fig1.update_xaxes(rangeslider_visible=True)
        
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
        return html.Div([
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
                    className="one-third column" #wind__speed__container,
                ),
                html.Div(
                    [
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
                            className="graph__container first",
                        ),
                        # wind direction
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6(
                                            "Ammonia", className="graph__title"
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
                            className="graph__container second",
                        ),
                    ],
                    className="one-third column", #histogram__direction",
                ),
            ],
            className="app__content",
        ),
        
                html.Div(
            [
                # wind speed
                html.Div(
                    [
                        html.Div(
                            [html.H6("CO2", className="graph__title")]
                        ),
                        dcc.Graph(
                            id="CO2-timeseries",
                            figure=fig4.update_layout(
                                    xaxis_title="Date Time ",
                                    yaxis_title="CO2",
                                    plot_bgcolor=app_color["graph_bg"],
                                    paper_bgcolor=app_color["graph_bg"],
                                    font_color="white",
                                    legend_title="CO2",
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
                    className="one-third column" #wind__speed__container,
                ),
                html.Div(
                    [
                        # histogram
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6(
                                            "CO",
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
                                                    legend_title="CO",
                                                    font=dict(
                                                        color="white"
                                                    )
                                        )
                                ),
                            ],
                            className="graph__container first",
                        ),
                        # wind direction
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6(
                                            "Pressure Humidity Temperature", className="graph__title"
                                        )
                                    ]
                                ),
                                dcc.Graph(
                                    id="pht-timeseries",
                                        figure=fig6.update_layout(
                                                    xaxis_title="Date Time ",
                                                    yaxis_title="PHT",
                                                    plot_bgcolor=app_color["graph_bg"],
                                                    paper_bgcolor=app_color["graph_bg"],
                                                    font_color="white",
                                                    legend_title="Parameters",
                                                    font=dict(
                                                        color="white"
                                                    )
                                        ),
                                ),
                            ],
                            className="graph__container second",
                        ),
                    ],
                    className="one-third column histogram__direction",
                ),
            ],
            className="app__content",
        ),
        html.Div(
            [
                # wind speed
                html.Div(
                    [
                        html.Div(
                            [html.H6("Particulate Matter", className="graph__title")]
                        ),
                        dcc.Graph(
                            id="PM-timeseries new new",
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
                    className="one-third column" #wind__speed__container,
                ),
                html.Div(
                    [
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
                                        id="PM-histogram new new",
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
                            className="graph__container first",
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
                            className="graph__container second",
                        ),
                    ],
                    className="one-third column histogram__direction",
                ),
            ],
            className="app__content",
        ),
        ])
    elif tab == 'week':
        data = [go.Scatter(x = df.dateTime, 
           y = df[c],
           mode = 'lines',
           name = c)for c in pm_cols]


        fig1 = go.Figure(data=data)
        fig1.update_xaxes(rangeslider_visible=True)
        
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
        return html.Div([
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
                    className="one-third column" #wind__speed__container,
                ),
                html.Div(
                    [
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
                            className="graph__container first",
                        ),
                        # wind direction
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6(
                                            "Ammonia", className="graph__title"
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
                            className="graph__container second",
                        ),
                    ],
                    className="one-third column", #histogram__direction",
                ),
            ],
            className="app__content",
        ),
        
                html.Div(
            [
                # wind speed
                html.Div(
                    [
                        html.Div(
                            [html.H6("CO2", className="graph__title")]
                        ),
                        dcc.Graph(
                            id="CO2-timeseries",
                            figure=fig4.update_layout(
                                    xaxis_title="Date Time ",
                                    yaxis_title="CO2",
                                    plot_bgcolor=app_color["graph_bg"],
                                    paper_bgcolor=app_color["graph_bg"],
                                    font_color="white",
                                    legend_title="CO2",
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
                    className="one-third column" #wind__speed__container,
                ),
                html.Div(
                    [
                        # histogram
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6(
                                            "CO",
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
                                                    legend_title="CO",
                                                    font=dict(
                                                        color="white"
                                                    )
                                        )
                                ),
                            ],
                            className="graph__container first",
                        ),
                        # wind direction
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6(
                                            "Pressure Humidity Temperature", className="graph__title"
                                        )
                                    ]
                                ),
                                dcc.Graph(
                                    id="pht-timeseries",
                                        figure=fig6.update_layout(
                                                    xaxis_title="Date Time ",
                                                    yaxis_title="PHT",
                                                    plot_bgcolor=app_color["graph_bg"],
                                                    paper_bgcolor=app_color["graph_bg"],
                                                    font_color="white",
                                                    legend_title="Parameters",
                                                    font=dict(
                                                        color="white"
                                                    )
                                        ),
                                ),
                            ],
                            className="graph__container second",
                        ),
                    ],
                    className="one-third column histogram__direction",
                ),
            ],
            className="app__content",
        ),
        html.Div(
            [
                # wind speed
                html.Div(
                    [
                        html.Div(
                            [html.H6("Particulate Matter", className="graph__title")]
                        ),
                        dcc.Graph(
                            id="PM-timeseries new new",
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
                    className="one-third column" #wind__speed__container,
                ),
                html.Div(
                    [
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
                                        id="PM-histogram new new",
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
                            className="graph__container first",
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
                            className="graph__container second",
                        ),
                    ],
                    className="one-third column histogram__direction",
                ),
            ],
            className="app__content",
        ),
        ])
    elif tab == 'month':
        data = [go.Scatter(x = df.dateTime, 
           y = df[c],
           mode = 'lines',
           name = c)for c in pm_cols]


        fig1 = go.Figure(data=data)
        fig1.update_xaxes(rangeslider_visible=True)
        
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
        return html.Div([
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
                    className="one-third column" #wind__speed__container,
                ),
                html.Div(
                    [
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
                            className="graph__container first",
                        ),
                        # wind direction
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6(
                                            "Ammonia", className="graph__title"
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
                            className="graph__container second",
                        ),
                    ],
                    className="one-third column", #histogram__direction",
                ),
            ],
            className="app__content",
        ),
        
                html.Div(
            [
                # wind speed
                html.Div(
                    [
                        html.Div(
                            [html.H6("CO2", className="graph__title")]
                        ),
                        dcc.Graph(
                            id="CO2-timeseries",
                            figure=fig4.update_layout(
                                    xaxis_title="Date Time ",
                                    yaxis_title="CO2",
                                    plot_bgcolor=app_color["graph_bg"],
                                    paper_bgcolor=app_color["graph_bg"],
                                    font_color="white",
                                    legend_title="CO2",
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
                    className="one-third column" #wind__speed__container,
                ),
                html.Div(
                    [
                        # histogram
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6(
                                            "CO",
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
                                                    legend_title="CO",
                                                    font=dict(
                                                        color="white"
                                                    )
                                        )
                                ),
                            ],
                            className="graph__container first",
                        ),
                        # wind direction
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6(
                                            "Pressure Humidity Temperature", className="graph__title"
                                        )
                                    ]
                                ),
                                dcc.Graph(
                                    id="pht-timeseries",
                                        figure=fig6.update_layout(
                                                    xaxis_title="Date Time ",
                                                    yaxis_title="PHT",
                                                    plot_bgcolor=app_color["graph_bg"],
                                                    paper_bgcolor=app_color["graph_bg"],
                                                    font_color="white",
                                                    legend_title="Parameters",
                                                    font=dict(
                                                        color="white"
                                                    )
                                        ),
                                ),
                            ],
                            className="graph__container second",
                        ),
                    ],
                    className="one-third column histogram__direction",
                ),
            ],
            className="app__content",
        ),
        html.Div(
            [
                # wind speed
                html.Div(
                    [
                        html.Div(
                            [html.H6("Particulate Matter", className="graph__title")]
                        ),
                        dcc.Graph(
                            id="PM-timeseries new new",
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
                    className="one-third column" #wind__speed__container,
                ),
                html.Div(
                    [
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
                                        id="PM-histogram new new",
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
                            className="graph__container first",
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
                            className="graph__container second",
                        ),
                    ],
                    className="one-third column histogram__direction",
                ),
            ],
            className="app__content",
        ),
        ])
    elif tab == 'year':
        data = [go.Scatter(x = df.dateTime, 
           y = df[c],
           mode = 'lines',
           name = c)for c in pm_cols]


        fig1 = go.Figure(data=data)
        fig1.update_xaxes(rangeslider_visible=True)
        
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
        return html.Div([
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
                    className="one-third column" #wind__speed__container,
                ),
                html.Div(
                    [
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
                            className="graph__container first",
                        ),
                        # wind direction
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6(
                                            "Ammonia", className="graph__title"
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
                            className="graph__container second",
                        ),
                    ],
                    className="one-third column", #histogram__direction",
                ),
            ],
            className="app__content",
        ),
        
                html.Div(
            [
                # wind speed
                html.Div(
                    [
                        html.Div(
                            [html.H6("CO2", className="graph__title")]
                        ),
                        dcc.Graph(
                            id="CO2-timeseries",
                            figure=fig4.update_layout(
                                    xaxis_title="Date Time ",
                                    yaxis_title="CO2",
                                    plot_bgcolor=app_color["graph_bg"],
                                    paper_bgcolor=app_color["graph_bg"],
                                    font_color="white",
                                    legend_title="CO2",
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
                    className="one-third column" #wind__speed__container,
                ),
                html.Div(
                    [
                        # histogram
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6(
                                            "CO",
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
                                                    legend_title="CO",
                                                    font=dict(
                                                        color="white"
                                                    )
                                        )
                                ),
                            ],
                            className="graph__container first",
                        ),
                        # wind direction
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6(
                                            "Pressure Humidity Temperature", className="graph__title"
                                        )
                                    ]
                                ),
                                dcc.Graph(
                                    id="pht-timeseries",
                                        figure=fig6.update_layout(
                                                    xaxis_title="Date Time ",
                                                    yaxis_title="PHT",
                                                    plot_bgcolor=app_color["graph_bg"],
                                                    paper_bgcolor=app_color["graph_bg"],
                                                    font_color="white",
                                                    legend_title="Parameters",
                                                    font=dict(
                                                        color="white"
                                                    )
                                        ),
                                ),
                            ],
                            className="graph__container second",
                        ),
                    ],
                    className="one-third column histogram__direction",
                ),
            ],
            className="app__content",
        ),
        html.Div(
            [
                # wind speed
                html.Div(
                    [
                        html.Div(
                            [html.H6("Particulate Matter", className="graph__title")]
                        ),
                        dcc.Graph(
                            id="PM-timeseries new new",
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
                    className="one-third column" #wind__speed__container,
                ),
                html.Div(
                    [
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
                                        id="PM-histogram new new",
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
                            className="graph__container first",
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
                            className="graph__container second",
                        ),
                    ],
                    className="one-third column histogram__direction",
                ),
            ],
            className="app__content",
        ),
        ])


if __name__ == '__main__':
    app.run_server(debug=False)