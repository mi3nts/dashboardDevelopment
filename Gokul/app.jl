using CSV, DataFrames, Dates, PlotlyBase
using Dash, DashHtmlComponents, DashCoreComponents


df = CSV.read("47cb5580002e004a_2021-06-17.csv",DataFrame)
df.dateTime = DateTime.(df.dateTime,"yyyy-mm-dd HH:MM:SS")
hs = [Plot(df.dateTime, df[:,i], title=names(df)[i]) for i in 3:ncol(df)]
ncols = 5 # set how many columns you want in the plot
nrows = cld(length(hs), ncols)
blankplot = Plot(legend=false,grid=false,foreground_color_subplot=:white)
for i = (length(hs)+1):(nrows*ncols)
    push!(hs, deepcopy(blankplot))
end
p1 = Plot(hs..., layout=(nrows, ncols), legend=false, size=(3000,1500))


app = dash()

app.layout = html_div() do
    html_h4("Iris Sepal Length vs Sepal Width")
    dcc_graph(figure=plot(rand(10)))
end

run_server(app, "0.0.0.0",8080)


#dcc_graph(
#    id = "example-graph-3",
#    figure = (p1),
#)