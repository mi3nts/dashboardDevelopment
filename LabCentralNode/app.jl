using Dash, DashHtmlComponents, DashCoreComponents
#using Plots
using PlotlyJS
using JSON
using Dates
include("json_read.jl")



binBoundariesHigh = [.46,.66,1,1.3,1.7,2.3,3.0,4.0,5.2,6.5,8,10,12,14,16,18,20,22,25,28,31,34,37,40];
binBoundariesLow  = [0.35,.46,.66,1,1.3,1.7,2.3,3.0,4.0,5.2,6.5,8,10,12,14,16,18,20,22,25,28,31,34,37];
binCenters = 0.5 .* (binBoundariesHigh .+ binBoundariesLow)


binBoundariesHigh2 = [0.1, 0.3, 0.5, 1.0, 2.5, 5.0, 10.0];
binBoundariesLow2  = [0.0, 0.1, 0.3, 0.5, 1.0, 2.5, 5.0];
binCenters2 = 0.5 .* (binBoundariesHigh2 .+ binBoundariesLow2)


# load in some test data to play with
IPS7100()
APDS9002()
BME280()
GUV001()
MGS001()
OPCN3()
SI114X()


function plotPM()
    # NOTE: we must use the semicolon in beginning of plotly commands as everything works via kwargs

    pm1 = scatter(;
                  x = sensors[:OPCN3][:dt],
                  y = sensors[:OPCN3][:pm1],
                  mode = "lines+markers",
                  name = "PM 1",
                  marker_color = :red,
                  marker_size = 5,
                  )

    pm2_5 = scatter(;
                  x = sensors[:OPCN3][:dt],
                  y = sensors[:OPCN3][:pm2_5],
                    mode = "lines+markers",
                    name = "PM 2.5",
                  marker_color = :blue,
                  marker_size = 5,
                  )

    pm10 = scatter(;
                  x = sensors[:OPCN3][:dt],
                  y = sensors[:OPCN3][:pm10],
                   mode = "lines+markers",
                   name = "PM 10",
                  marker_color = :green,
                  marker_size = 5,
                  )

    pm1_ips = scatter(;
                    x = sensors[:IPS7100][:dt],
                    y = sensors[:IPS7100][:pm1_0],
                    mode = "lines+markers",
                    name = "PM 1 IPS",
                    marker_color = :cyan,
                    marker_size = 5,
                  )

    pm2_5_ips = scatter(;
                        x = sensors[:IPS7100][:dt],
                        y = sensors[:IPS7100][:pm2_5],
                        mode = "lines+markers",
                        name = "PM 2.5 IPS",
                        marker_color = :black,
                        marker_size = 5,
                    )

    pm10_ips = scatter(;
                       x = sensors[:IPS7100][:dt],
                       y = sensors[:IPS7100][:pm10_0],
                   mode = "lines+markers",
                   name = "PM 10 IPS",
                   marker_color = :purple,
                   marker_size = 5,
                   )



    layout = Layout(;
                    title = "PM Levels",
                    xaxis_title = "time",
                    yaxis_title = "PM [μg/m³]",
                    plot_bgcolor = :transparent,
                    paper_bgcolor = :transparent,
                    )
    plot([pm1, pm2_5, pm10, pm1_ips, pm2_5_ips, pm10_ips], layout)
end


function plotContour()
    # data = [(
    #     type="contour",
    #     x = sensors[:OPCN3][:dt],
    #     y = binCenters,
    #     z = log.(hcat(sensors[:OPCN3][:bins]...) .+ 1.0 ),  # add 1 to each count so we don't have issues with log(0)
    #     colorscale = "Viridis",
    # )]

    # layout=(
    #     title = "Particle Size Distribution",
    #     xaxis_title = "time",
    #     yaxis_title = "bin centers"
    # )

    # return (data=data, layout=layout)

    data = contour(;
                   x = sensors[:OPCN3][:dt],
                   y = binCenters,
                   z = log10.(hcat(sensors[:OPCN3][:bins]...) .+ 1.0 ),  # add 1 to each count so we don't have issues with log(0)
                   colorscale = "Jet",
                   ncontours = 100,
                   contours_showlines = false,
                   )

    layout = Layout(;
                    title = "Particle Size Distribution (OPCN3)",
                    xaxis_title = "time",
                    yaxis_title = "Particle Radius [μm]",
                    yaxis_type = "log",
                    plot_bgcolor = :transparent,
                    paper_bgcolor = :transparent,
                    )
    plot(data, layout)
end



function plotContour2()
    data = contour(;
                   x = sensors[:IPS7100][:dt],
                   y = binCenters2,
                   z = log10.(hcat(sensors[:IPS7100][:bins]...) .+ 1.0 ),  # add 1 to each count so we don't have issues with log(0)
                   colorscale = "Jet",
                   ncontours = 100,
                   contours_showlines = false,
                   )

    layout = Layout(;
                    title = "Particle Size Distribution (IPS7100 sensor)",
                    xaxis_title = "time",
                    yaxis_title = "Particle Radius [μm]",
                    yaxis_type = "log",
                    plot_bgcolor = :transparent,
                    paper_bgcolor = :transparent,
                    )
    plot(data, layout)

end



function update_pm()
    # load in some test data to play with
    IPS7100()
    APDS9002()
    BME280()
    GUV001()
    MGS001()
    OPCN3()
    SI114X()

    plotPM()
end


function update_contour()
    plotContour()
end


function update_contour2()
    plotContour2()
end



#app_color = Dict("graph_bg"=>"#082255", "graph_line"=>"#007ACE")

app = dash()

app.layout = html_div() do
    html_h1(
        "MINTS Live Dashboards: Central Node Air Package",
        style=Dict("color"=>:black, "textAlign"=>"center"),
    ),
    html_div(
        children = [
            dcc_graph(
                id="pm-graph",
                figure = plotPM()
            ),
            dcc_graph(
                id="size-contour",
                figure = plotContour()
            ),
            dcc_graph(
                id="size-contour2",
                figure = plotContour2()
            ),
            dcc_interval(
                id="interval-component",
                interval = 250, # 250 miliseconds
                n_intervals=0
            ),
        ],
#        className = "two-thirds column wind__speed__container",
    )
end


callback!(app,
          Output("pm-graph", "figure"),
          Input("interval-component", "n_intervals")) do n
    update_pm()
end

callback!(app, Output("size-contour", "figure"), Input("interval-component", "n_intervals")) do n
    update_contour()
end


callback!(app, Output("size-contour2", "figure"), Input("interval-component", "n_intervals")) do n
    update_contour2()
end





run_server(app, "0.0.0.0", debug=true)
