from TempAndHumidity import *
from equipment import *
from act_TempAndHumidity import *

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
#########################

ABV_DICT  = { "humidity":'HS',
			   "roomTemp":'RT', 
			   "solderingStation": 'ST', 
			   "oscilloscope" : 'OS',
			   "testBentch": 'TB',
			   "convyor" :'CB',
			   "roomtempActuator":'RA' ,
			   "humidityActuator":'HA'}


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

class prodLine:
	"""docstring for prodLine"""
	# hCount : humidity sensor count
	# rTcount : room temperature sensor count
	# sCount  : soldring station count
	# oCount : oscilloscope count -room feature
	# tCount: test bench count  - room feature
	# cBcount : conveyor belt count
		

	def __init__(self, lineNumber, hCount = 3, rTcount = 4, sCount = 3, cBcount=2):

		super(prodLine, self).__init__()
		self.lineNumber = lineNumber
		self.hCount     = hCount
		self.rTcount    = rTcount
		self.sCount     = sCount
		self.cBcount	= cBcount

		
		#create instances of humidity sensor
		self.humiditySensList = [ ]
		for i in range (0,hCount):
			id = createInstanceID(self.lineNumber, 'S', ABV_DICT["humidity"], i)
			self.humiditySensList.append(HumiditySensor(id))
			print(id)

		#create instances of room temperature sensor
		self.roomTempSensList =[]
		for i in range (0,rTcount):
			id = createInstanceID(self.lineNumber, 'S', ABV_DICT["roomTemp"], i)
			self.roomTempSensList.append(TemperatureSensor(instanceID = id,  tempSensorType = TEMP_ROOM))
			print(id)

		#create instances of soldering temperature sensor
		self.solderSensList =[]
		for i in range (0,sCount):
			id = createInstanceID(self.lineNumber, 'S', ABV_DICT["oscilloscope"], i)
			self.solderSensList.append(TemperatureSensor(instanceID = id,  tempSensorType = TEMP_SOLDERING))
			print(id)	

		#create instances of soldering temperature sensor
		self.convBeltList =[]
		for i in range (0,cBcount):
			id = createInstanceID(self.lineNumber, 'E', ABV_DICT["convyor"], i)
			self.convBeltList.append(conveyorBelt(instanceID = id))
			print(id)	



	def getLineNumber(self):
		return self.lineNumber





		
