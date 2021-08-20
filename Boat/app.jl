using Dash, DashHtmlComponents, DashCoreComponents
#using Plots
using PlotlyJS
using JSON
using Dates
include("json_read.jl")

# load in some test data to play with
BME280()
GUV001()
MGS001()
OPCN3()
SI114X()


function plotTest()
    # NOTE: we must use the semicolon in beginning of plotly commands as everything works via kwargs

    trace = scatter(;
                    x = sensors[:MGS001][:dt],
                    y = sensors[:MGS001][:c2h5oh],
                    mode = "lines+markers",
                    marker_color = :red,
                    marker_size = 8,
                    )
    layout = Layout(;
                    title = "Test Plot",
                    xaxis_title = "time",
                    yaxis_title = "c2h5oh",
                    plot_bgcolor = :transparent,
                    paper_bgcolor = :transparent, 
                    )
    plot(trace, layout)
end


# function plotTest()
#     p = plot(sensors[:MGS001][:dt],
#              sensors[:MGS001][:c2h5oh],
#              xlabel="time",
#              ylabel="y value",
#              showaxeslabels=true,
#              color=:red,
#              autosize=true,
#              seriestype=:line,
#              label="",
#              animate=true,
#              background_color=:transparent,
#              # foreground_color=:black,
#              )
#     fig =(data = Plots.plotly_series(p), layout = Plots.plotly_layout(p))
# end


function update_graph()
    # load in some test data to play with
    BME280()
    GUV001()
    MGS001()
    OPCN3()
    SI114X()

    plotTest()
end



app_color = Dict("graph_bg"=>"#082255", "graph_line"=>"#007ACE")

app = dash()

app.layout = html_div() do
    html_h1(
        "Test plot",
        style=Dict("color"=>:white),
    ),
    html_div(
        children = [
            dcc_graph(
                id="live-graph",
                figure = plotTest()
            ),
            dcc_interval(
                id="interval-component",
                interval = 250, # 250 miliseconds
                n_intervals=0
            ),
        ],
        className = "two-thrids column wind__speed__container",
    )
end


callback!(app, Output("live-graph", "figure"), Input("interval-component", "n_intervals")) do n
    update_graph()
end




run_server(app, "0.0.0.0", debug=true)
