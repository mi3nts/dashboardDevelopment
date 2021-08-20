using Dash, DashHtmlComponents, DashCoreComponents
#using Plots
using PlotlyJS
using JSON
using Dates
include("json_read.jl")



binBoundariesHigh = [.46,.66,1,1.3,1.7,2.3,3.0,4.0,5.2,6.5,8,10,12,14,16,18,20,22,25,28,31,34,37,40];
binBoundariesLow  = [0.35,.46,.66,1,1.3,1.7,2.3,3.0,4.0,5.2,6.5,8,10,12,14,16,18,20,22,25,28,31,34,37];
binCenters = 0.5 .* (binBoundariesHigh .+ binBoundariesLow)


# load in some test data to play with
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



    layout = Layout(;
                    title = "PM Levels",
                    xaxis_title = "time",
                    yaxis_title = "PM [μg/m³]",
                    plot_bgcolor = :transparent,
                    paper_bgcolor = :transparent,
                    )
    plot([pm1, pm2_5, pm10], layout)
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
                    title = "Particle Size Distribution",
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



#app_color = Dict("graph_bg"=>"#082255", "graph_line"=>"#007ACE")

app = dash()

app.layout = html_div() do
    html_h1(
        "MINTS Live Dashboards: AV Air Package",
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





run_server(app, "0.0.0.0", debug=true)
