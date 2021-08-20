#!/bin/bash


source env/bin/activate
cd mqttSubscribers/firmware
python groundVehicleDataRead.py & 
sleep 5 
python otterDataRead.py
