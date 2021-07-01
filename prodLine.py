from TempAndHumidity import *
from equipment import *
from PressureAndIR import *
from client_broker_data import *


class prodLine:
	"""docstring for prodLine"""
	# hCount : humidity sensor count
	# rTcount : room temperature sensor count
	# sCount  : soldring station count
	# oCount : oscilloscope count -room feature
	# tCount: test bench count  - room feature
	# cBcount : conveyor belt count
	# iCount   : IR sensors count 
	# pCount  : Pressure sensor
		

	def __init__(self, lineNumber, hCount = 3, rTcount = 4, sCount = 3, cBcount=2, iCount = 1, pCount=2):

		super(prodLine, self).__init__()
		self.lineNumber = lineNumber
		self.hCount     = hCount
		self.rTcount    = rTcount
		self.sCount     = sCount
		self.cBcount	= cBcount
		self.iCount     = iCount
		self.ESDcount   = self.sCount #number of ESD protection sensor is equal to number of soldering station
		self.pCount 	= pCount

		

		#create instances of soldering temperature sensor
		self.solderSensList =[]
		for i in range (0,self.sCount):
			id = createInstanceID(self.lineNumber, 'S', ABV_DICT["solderingStation"], i)
			self.solderSensList.append(TemperatureSensor(instanceID = id,  tempSensorType = TEMP_SOLDERING))
			print(id)	

		#create instances of soldering temperature sensor
		self.convBeltList =[]
		for i in range (0,self.cBcount):
			id = createInstanceID(self.lineNumber, 'E', ABV_DICT["convyor"], i)
			self.convBeltList.append(conveyorBelt(instanceID = id))
			print(id)	

		#create instances of IR sensor
		self.irSensorList =[]
		for i in range (0,self.iCount):
			id = createInstanceID(self.lineNumber, 'S', ABV_DICT["irSensor"], i)
			self.irSensorList.append(IrSensor(instanceID = id))
			print(id)

		#create instances of ESD sensor
		self.esdSensorList =[]
		for i in range (0,self.ESDcount):
			id = createInstanceID(self.lineNumber, 'S', ABV_DICT["ESD"], i)
			self.esdSensorList.append(EsdProtectionSensor(instanceID = id))
			print(id)

		#create instances of pressure sensor
		self.pressureSensorList =[]
		for i in range (0,self.ESDcount):
			id = createInstanceID(self.lineNumber, 'S', ABV_DICT["pressure"], i)
			self.pressureSensorList.append(PressureSensor(instanceID = id))
			print(id)

	def getLineNumber(self):
		return self.lineNumber





		
