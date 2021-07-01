import paho.mqtt.client as mqtt
import time
import datetime  
import json 

# awshost = "a1etmfjjj6j48x-ats.iot.us-west-2.amazonaws.com"  
# awsport = 8883
# caPath = "/home/ashwini/Desktop/IOT/Certificates/root-ca.pem.txt"
# certPath = "/home/ashwini/Desktop/IOT/Certificates/certificate.pem.crt"
# keyPath = "/home/ashwini/Desktop/IOT/Certificates/private.pem.key"

brokerHost =  "broker.emqx.io" #"localhost"
brokerPort = 1883
brokerKeepAlive = 60

QOS = 1 #0



clientDict = {  "simLineClient" : "ProdLine",
				"simTempActClient" : "TemperatureActuator",
				"simHumActClient" : "HumidityActuator",
				"simProdServerClient" : "ProductionServer",
				"simRoomTempClient"  : "RoomTemperatureSensor",
				"simHumiditySensorClient" : "HumiditySensor",
				"simEquOscClient" : "OscEquipment",
				"simEquTbClient" : "tbEquipment",
				}

topicDict ={    "ST" : "room/room1/prodLine1/sensor/solderingStation/",
 			    "HS" : "room/room1/sensor/humidity/" ,
 				"RT" : "room/room1/sensor/roomTemp/",
 				"OS" : "room/room1/equipment/oscilloscope/",
 				"TB" : "room/room1/equipment/testBentch/",
 				"CB" : "room/room1/prodLine1/equipment/convyor/",
 				"RA" : "room/room1/actuator/roomtempActuator/",
 				"HA" : "room/room1/actuator/humidityActuator/",
 				"IR" : "room/room1/prodLine1/sensor/irSensor/",
 				"ES" : "room/room1/prodLine1/sensor/ESD/",
 				"PS" : "room/room1/prodLine1/sensor/pressure/",
 				"PEO": "server/equipment/osc/",
 				"PET": "server/equipment/tb/"}

##########################
# Instance ID format -of len 7
#  instance ID =  S/A/E | Abbrevation |Line Number | instance number
#   S/A -> 'S' (sensor) or 'A' (actuator ) or 'E' (equipment)  - 1 char
#   Line number  -> 01 - 99 -> 2char
#   instance number -> 00 - 99 -> 2 char
#    Abbrevation -> 2char
#        list of abbrevation
#                HS : HUMIDITY SENSOR
#                RT : ROOM TEMPERATUR SENSOR
#                ST : SOLDERING STATION SENSOR
#                OS : OSCILLOSCOPE 
#                TB : TESTBENTCH
#                CB : CONVYOR BELT
#				 RA : ROOM ACTUATOR
#				 HA : HUMIDITY ACTUATOR
# 				 IR : IR SENSOR
#########################

ABV_DICT  = { "humidity":		    'HS',
			   "roomTemp":			'RT', 
			   "solderingStation":  'ST', 
			   "oscilloscope" :     'OS',
			   "testBentch":        'TB',
			   "convyor" :          'CB',
			   "roomtempActuator":  'RA' ,
			   "humidityActuator":  'HA',
			   "irSensor" :         "IR",
			   "ESD" :              "ES",
			   "pressure" :         "PS"}

def createInstanceID(lineNum, s_a, abv, instanceNumber):
	createdID = s_a
	createdID = createdID + abv

	if lineNum < 10 :
	    createdID += '0'

	createdID += str(lineNum)

	if instanceNumber < 10 :
	    createdID += '0'

	createdID += str(instanceNumber)

	return createdID
