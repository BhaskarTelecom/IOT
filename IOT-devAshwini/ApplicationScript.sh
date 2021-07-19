#!/usr/bin/env bash

gnome-terminal --tab --title="Room Temp" --command="bash -c 'python3 simRoomTemp.py'"
gnome-terminal --tab --title="Humidity Sensor" --command="bash -c 'python3 simHumiditySensor.py'"
gnome-terminal --tab --title="Osc" --command="bash -c 'python3 simEquOsc.py'" 
gnome-terminal --tab --title="tb" --command="bash -c 'python3 simEquTb.py'"
gnome-terminal --tab --title="Line" --command="bash -c 'python3 simLine.py'"
gnome-terminal --tab --title="Humidity Act" --command="bash -c 'python3 simHumidityAct.py'"
gnome-terminal --tab --title="Room Temp act" --command="bash -c 'python3 simTempAct.py'"
gnome-terminal --tab --title="Prod Server" --command="bash -c 'python3 simProdServer.py'"
gnome-terminal --tab --title="Dash App" --command="bash -c 'python3 /home/bhaskar/IOT/IOT/dash_trial/app.py'"

