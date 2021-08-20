using JSON
using Dates


dateformat = DateFormat("yyyy-mm-dd HH:MM:SS")
Npoints = 1000
basepath = "/home/teamlary/mintsData/rawMQTT/001e0610c2ed"




sensors = Dict(:APDS9002 => Dict(:path => joinpath(basepath, "APDS9002.json"),
                                 :luminance => Float64[],
                                 :dt => DateTime[],
                                 ),
               :BME280 => Dict(:path => joinpath(basepath, "BME280.json"),
                               :pressure => Float64[],
                               :humidity => Float64[],
                               :temperature => Float64[],
                               :dt => DateTime[],
                               ),
               :GUV001 => Dict(:path => joinpath(basepath, "GUV001.json"),
                               :uvLevel => Float64[],
                               :dt => DateTime[],
                               ),
               :MGS001 => Dict(:path => joinpath(basepath, "MGS001.json"),
                               :c2h5oh => Float64[],
                               :nh3 => Float64[],
                               :c4h10 => Float64[],
                               :c3h8 => Float64[],
                               :ch4 => Float64[],
                               :co => Float64[],
                               :h2 => Float64[],
                               :no2 => Float64[],
                               :dt => DateTime[],
                               ),
               :OPCN3 => Dict(:path => joinpath(basepath, "OPCN3.json"),
                              :pm1 => Float64[],
                              :pm2_5 => Float64[],
                              :pm10 => Float64[],
                              :bins => Vector{Float64}[],
                              :dt => DateTime[],
                              ),
               :SI114X => Dict(:path =>joinpath(basepath, "SI114X.json"),
                               :visible => Float64[],
                               :uv => Float64[],
                               :ir => Float64[],
                               :proximity1 => Float64[],
                               :proximity2 => Float64[],
                               :proximity3 => Float64[],
                               :dt => DateTime[],
                               ),
              )


function APDS9002()
    res = JSON.parsefile(sensors[:APDS9002][:path])

    datetime = res["dateTime"]
    dt = split(datetime, ".")[1]
    dt = DateTime(dt, dateformat)

    if length(sensors[:APDS9002][:dt]) > 0 &&  dt == sensors[:APDS9002][:dt][end]
        return -1
    end



    if length(sensors[:APDS9002][:luminance]) < Npoints
        push!(sensors[:APDS9002][:luminance], parse(Float64, res["luminance"]))
    else
        sensors[:APDS9002][:luminance] .= circshift(sensors[:APDS9002][:luminance], -1)
        sensors[:APDS9002][:luminance][end] = parse(Float64, res["luminance"])
    end

    if length(sensors[:APDS9002][:dt]) < Npoints
        push!(sensors[:APDS9002][:dt], dt)
    else
        sensors[:APDS9002][:dt] .= circshift(sensors[:APDS9002][:dt], -1)
        sensors[:APDS9002][:dt][end] = dt
    end
end


function BME280()
    res = JSON.parsefile(sensors[:BME280][:path])
    datetime = res["dateTime"]
    dt = split(datetime, ".")[1]
    dt = DateTime(dt, dateformat)

    if length(sensors[:BME280][:dt]) > 0 dt == sensors[:BME280][:dt][end]
        return -1
    end




    if length(sensors[:BME280][:pressure]) < Npoints
        push!(sensors[:BME280][:pressure], parse(Float64, res["pressure"]))
    else
        sensors[:BME280][:pressure] .= circshift(sensors[:BME280][:pressure], -1)
        sensors[:BME280][:pressure][end] = parse(Float64, res["pressure"])
    end


    if length(sensors[:BME280][:humidity]) < Npoints
        push!(sensors[:BME280][:humidity], parse(Float64, res["humidity"]))
    else
        sensors[:BME280][:humidity] .= circshift(sensors[:BME280][:humidity], -1)
        sensors[:BME280][:humidity][end] = parse(Float64, res["humidity"])
    end


    if length(sensors[:BME280][:temperature]) < Npoints
        push!(sensors[:BME280][:temperature], parse(Float64, res["temperature"]))
    else
        sensors[:BME280][:temperature] .= circshift(sensors[:BME280][:temperature], -1)
        sensors[:BME280][:temperature][end] = parse(Float64, res["temperature"])
    end



    if length(sensors[:BME280][:dt]) < Npoints
        push!(sensors[:BME280][:dt], dt)
    else
        sensors[:BME280][:dt] .= circshift(sensors[:BME280][:dt], -1)
        sensors[:BME280][:dt][end] = dt
    end

end


function GUV001()
    res = JSON.parsefile(sensors[:GUV001][:path])
    datetime = res["dateTime"]
    dt = split(datetime, ".")[1]
    dt = DateTime(dt, dateformat)

    if length(sensors[:GUV001][:dt]) > 0 && dt == sensors[:GUV001][:dt][end]
        return -1
    end



    if length(sensors[:GUV001][:uvLevel]) < Npoints
        push!(sensors[:GUV001][:uvLevel], parse(Float64, res["uvLevel"]))
    else
        sensors[:GUV001][:uvLevel] .= circshift(sensors[:GUV001][:uvLevel], -1)
        sensors[:GUV001][:uvLevel][end] = parse(Float64, res["uvLevel"])
    end

    if length(sensors[:GUV001][:dt]) < Npoints
        push!(sensors[:GUV001][:dt], dt)
    else
        sensors[:GUV001][:dt] .= circshift(sensors[:GUV001][:dt], -1)
        sensors[:GUV001][:dt][end] = dt
    end
end


function MGS001()
    res = JSON.parsefile(sensors[:MGS001][:path])
    datetime = res["dateTime"]
    dt = split(datetime, ".")[1]
    dt = DateTime(dt, dateformat)

    if length(sensors[:MGS001][:dt]) > 0 && dt == sensors[:MGS001][:dt][end]
        return -1
    end



    if length(sensors[:MGS001][:dt]) < Npoints
        push!(sensors[:MGS001][:dt], dt)
    else
        sensors[:MGS001][:dt] .= circshift(sensors[:MGS001][:dt], -1)
        sensors[:MGS001][:dt][end] = dt
    end

    if length(sensors[:MGS001][:c2h5oh]) < Npoints
        push!(sensors[:MGS001][:c2h5oh], parse(Float64, res["c2h5oh  "]))
    else
        sensors[:MGS001][:c2h5oh] .= circshift(sensors[:MGS001][:c2h5oh], -1)
        sensors[:MGS001][:c2h5oh][end] = parse(Float64, res["c2h5oh  "])
    end


    if length(sensors[:MGS001][:nh3]) < Npoints
        push!(sensors[:MGS001][:nh3], parse(Float64, res["nh3"]))
    else
        sensors[:MGS001][:nh3] .= circshift(sensors[:MGS001][:nh3], -1)
        sensors[:MGS001][:nh3][end] = parse(Float64, res["nh3"])
    end


    if length(sensors[:MGS001][:c4h10]) < Npoints
        push!(sensors[:MGS001][:c4h10], parse(Float64, res["c4h10"]))
    else
        sensors[:MGS001][:c4h10] .= circshift(sensors[:MGS001][:c4h10], -1)
        sensors[:MGS001][:c4h10][end] = parse(Float64, res["c4h10"])
    end


    if length(sensors[:MGS001][:c3h8]) < Npoints
        push!(sensors[:MGS001][:c3h8], parse(Float64, res["c3h8"]))
    else
        sensors[:MGS001][:c3h8] .= circshift(sensors[:MGS001][:c3h8], -1)
        sensors[:MGS001][:c3h8][end] = parse(Float64, res["c3h8"])
    end


    if length(sensors[:MGS001][:ch4]) < Npoints
        push!(sensors[:MGS001][:ch4], parse(Float64, res["ch4"]))
    else
        sensors[:MGS001][:ch4] .= circshift(sensors[:MGS001][:ch4], -1)
        sensors[:MGS001][:ch4][end] = parse(Float64, res["ch4"])
    end


    if length(sensors[:MGS001][:co]) < Npoints
        push!(sensors[:MGS001][:co], parse(Float64, res["co"]))
    else
        sensors[:MGS001][:co] .= circshift(sensors[:MGS001][:co], -1)
        sensors[:MGS001][:co][end] = parse(Float64, res["co"])
    end


    if length(sensors[:MGS001][:no2]) < Npoints
        push!(sensors[:MGS001][:no2], parse(Float64, res["no2"]))
    else
        sensors[:MGS001][:no2] .= circshift(sensors[:MGS001][:no2], -1)
        sensors[:MGS001][:no2][end] = parse(Float64, res["no2"])
    end
end


function OPCN3()
    res = JSON.parsefile(sensors[:OPCN3][:path])
    datetime = res["dateTime"]
    dt = split(datetime, ".")[1]
    dt = DateTime(dt, dateformat)

    if length(sensors[:OPCN3][:dt]) > 0 && dt == sensors[:OPCN3][:dt][end]
        return -1
    end


    if length(sensors[:OPCN3][:dt]) < Npoints
        push!(sensors[:OPCN3][:dt], dt)
    else
        sensors[:OPCN3][:dt] .= circshift(sensors[:OPCN3][:dt], -1)
        sensors[:OPCN3][:dt][end] = dt
    end

    if length(sensors[:OPCN3][:pm1]) < Npoints
        push!(sensors[:OPCN3][:pm1], parse(Float64, res["pm1"]))
    else
        sensors[:OPCN3][:pm1] .= circshift(sensors[:OPCN3][:pm1], -1)
        sensors[:OPCN3][:pm1][end] = parse(Float64, res["pm1"])
    end


    if length(sensors[:OPCN3][:pm2_5]) < Npoints
        push!(sensors[:OPCN3][:pm2_5], parse(Float64, res["pm2_5"]))
    else
        sensors[:OPCN3][:pm2_5] .= circshift(sensors[:OPCN3][:pm2_5], -1)
        sensors[:OPCN3][:pm2_5][end] = parse(Float64, res["pm2_5"])
    end


    if length(sensors[:OPCN3][:pm10]) < Npoints
        push!(sensors[:OPCN3][:pm10], parse(Float64, res["pm10"]))
    else
        sensors[:OPCN3][:pm10] .= circshift(sensors[:OPCN3][:pm10], -1)
        sensors[:OPCN3][:pm10][end] = parse(Float64, res["pm10"])
    end


    bins = parse.(Float64,[
                            res["pm1"],
                            res["pm2_5"],
                            res["pm10"],
                            res["binCount0"],
                            res["binCount1"],
                            res["binCount2"],
                            res["binCount3"],
                            res["binCount4"],
                            res["binCount5"],
                            res["binCount6"],
                            res["binCount7"],
                            res["binCount8"],
                            res["binCount9"],
                            res["binCount10"],
                            res["binCount11"],
                            res["binCount12"],
                            res["binCount13"],
                            res["binCount14"],
                            res["binCount15"],
                            res["binCount16"],
                            res["binCount17"],
                            res["binCount18"],
                            res["binCount19"],
                            res["binCount20"],
                            res["binCount21"],
                            res["binCount22"],
                            res["binCount23"],
    ])


    if length(sensors[:OPCN3][:bins]) < Npoints
        push!(sensors[:OPCN3][:bins], bins)
    else
        sensors[:OPCN3][:bins] .= circshift(sensors[:OPCN3][:bins], -1)
        sensors[:OPCN3][:bins][end] = bins
    end

end



function SI114X()
    res = JSON.parsefile(sensors[:SI114X][:path])
    datetime = res["dateTime"]
    dt = split(datetime, ".")[1]
    dt = DateTime(dt, dateformat)

    if length(sensors[:SI114X][:dt]) > 0 && dt == sensors[:SI114X][:dt][end]
        return -1
    end



    if length(sensors[:SI114X][:dt]) < Npoints
        push!(sensors[:SI114X][:dt], dt)
    else
        sensors[:SI114X][:dt] .= circshift(sensors[:SI114X][:dt], -1)
        sensors[:SI114X][:dt][end] = dt
    end

    if length(sensors[:SI114X][:visible]) < Npoints
        push!(sensors[:SI114X][:visible], parse(Float64, res["visible"]))
    else
        sensors[:SI114X][:visible] .= circshift(sensors[:SI114X][:visible], -1)
        sensors[:SI114X][:visible][end] = parse(Float64, res["visible"])
    end

    if length(sensors[:SI114X][:uv]) < Npoints
        push!(sensors[:SI114X][:uv], parse(Float64, res["uv"]))
    else
        sensors[:SI114X][:uv] .= circshift(sensors[:SI114X][:uv], -1)
        sensors[:SI114X][:uv][end] = parse(Float64, res["uv"])
    end

    if length(sensors[:SI114X][:ir]) < Npoints
        push!(sensors[:SI114X][:ir], parse(Float64, res["ir"]))
    else
        sensors[:SI114X][:ir] .= circshift(sensors[:SI114X][:ir], -1)
        sensors[:SI114X][:ir][end] = parse(Float64, res["ir"])
    end

    if length(sensors[:SI114X][:proximity1]) < Npoints
        push!(sensors[:SI114X][:proximity1], parse(Float64, res["proximity1"]))
    else
        sensors[:SI114X][:proximity1] .= circshift(sensors[:SI114X][:proximity1], -1)
        sensors[:SI114X][:proximity1][end] = parse(Float64, res["proximity1"])
    end

    if length(sensors[:SI114X][:proximity2]) < Npoints
        push!(sensors[:SI114X][:proximity2], parse(Float64, res["proximity2"]))
    else
        sensors[:SI114X][:proximity2] .= circshift(sensors[:SI114X][:proximity2], -1)
        sensors[:SI114X][:proximity2][end] = parse(Float64, res["proximity2"])
    end

    if length(sensors[:SI114X][:proximity3]) < Npoints
        push!(sensors[:SI114X][:proximity3], parse(Float64, res["proximity3"]))
    else
        sensors[:SI114X][:proximity3] .= circshift(sensors[:SI114X][:proximity3], -1)
        sensors[:SI114X][:proximity3][end] = parse(Float64, res["proximity3"])
    end
end

