using CSV
using DataFrames
using Plots
using Statistics
plotly()


pathToCSVs = "../data/sampleNode"
csvs = [joinpath(pathToCSVs, f) for f ∈ readdir(pathToCSVs) if endswith(f, ".csv")]

sensor_id = ""
sensors = Dict()

i = 1
for csv ∈ csvs
    fname = splitext(basename(csv))[1]
    splitname = split(fname, "_")
    if i == 1
        sensor_id = splitname[2]
        i = 0
    end
    sensors[splitname[3]] = DataFrame(CSV.File(csv))
end


for (sensorname, df) ∈ sensors
    println(names(df))
    println("\n")
end

