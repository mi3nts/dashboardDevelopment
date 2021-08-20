using JSON
using Dates


dateformat = DateFormat("yyyy-mm-dd HH:MM:SS")
Npoints = 1000
basepath = "/home/teamlary/mintsData/rawMQTT/001e06318c91"



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


AS7262.json  TMG3993.json  VEML6075.json
  GL001.json   LIBRAD.json  TB108L.json  TSL2591.json
