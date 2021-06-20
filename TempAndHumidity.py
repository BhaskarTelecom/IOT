import numpy as np
import matplotlib.pyplot as plt
import math 
##########################################################################
# Class : TemperatureSensor
# feature : sense(), getInstanceID(), 
##########################################################################

#index 0 row: for HumanBody 
TEMP_HUMAN_BODY = 0 #this is not a body temp but rather a location temp where the individual is working
TEMP_ROOM       = TEMP_HUMAN_BODY+1
TEMP_SOLDERING  = TEMP_ROOM+1
HUMIDITY_RH     = TEMP_SOLDERING+1



MEAN_INDEX = 0
VAR_INDEX  = MEAN_INDEX+1
RATE_INDEX = VAR_INDEX+1


#mean, variance 
#https://medlineplus.gov/ency/article/001982.htm
#https://www.digikey.com/en/maker/blogs/rohs-vs-non-rohs-soldering
const__SensorType_Data__ = []

const__SensorType_Data__.append([37.00, 0.4, 0.2]) #36.6 to 37.4 C - Body Temp
const__SensorType_Data__.append([22.5, 4.5,0.035 ]) #Room Temp: mean 22.5 C, var =4.5 C min 68 F, max 77 F 
const__SensorType_Data__.append([217.0, 2 ,0.09])   # Soldering Iron temp
const__SensorType_Data__.append([55.0, 5 , 0.015])   # RH 


class TemperatureSensor():
	"""docstring for TemperatureSensor"""
	sensorType = "temperature"
	unit = "celsius"

	def _pvt_CheckRange(self,value):

		value = min(value, self.maxVal)
		value = max(value, self.minVal)

		return value

	##########################################################################
	# tempSensroType : Human Body, Soldering Station, Room Temperature
	# instanceID : provided by the user/system
	##########################################################################
	def __init__(self, tempSensorType, instanceID):
		self.tempSensorType = tempSensorType
		self.instanceID = instanceID

		self.mean = const__SensorType_Data__[tempSensorType][MEAN_INDEX]
		self.variance = const__SensorType_Data__[tempSensorType][VAR_INDEX]
		self.rate = const__SensorType_Data__[tempSensorType][RATE_INDEX]

		self.maxVal = self.mean + self.variance
		self.minVal = self.mean - self.variance

		self.value = self.mean + self.variance*self.rate 
		self.value +=  self.rate*math.sin(np.random.normal(self.mean, self.variance))	

		
	def sense(self):
		# get a value using normal distribution for temperature
		if(self.tempSensorType == TEMP_ROOM):
			self.value +=   self.rate*np.random.normal( (self.value - self.mean)/self.value, (self.variance)/self.value)

		elif self.tempSensorType == TEMP_SOLDERING :
			self.value +=   self.rate*self.variance*math.sin(np.random.uniform(math.pi/2, -math.pi/2))

		else :
			self.value = np.random.normal(self.mean , self.variance)

		#check for out of range values of sensor.	
		self.value = self._pvt_CheckRange(self.value)

		return self.value


		#Provide instance ID of the sensor being read.
	def getInstanceID(self):
		return self.instanceID

	
class HumiditySensor():
	"""docstring for HumiditySensor"""
	sensorType = "humidity"
	unit ="Percentage_RH"

	def _pvt_CheckRange(self,value):

		value = min(value, self.maxVal)
		value = max(value, self.minVal)

		return value

	def __init__(self,instanceID):
		
		self.instanceID = instanceID

		self.mean = const__SensorType_Data__[HUMIDITY_RH][MEAN_INDEX]
		self.variance = const__SensorType_Data__[HUMIDITY_RH][VAR_INDEX]
		self.rate = const__SensorType_Data__[HUMIDITY_RH][RATE_INDEX]

		self.maxVal = self.mean + self.variance
		self.minVal = self.mean - self.variance

		self.value = np.random.uniform(self.minVal, self.maxVal)

	def sense(self): 
		
		self.value += self.rate*self.variance*math.sin(np.random.uniform(-math.pi/2, math.pi/2))
		self.value = self._pvt_CheckRange(self.value)
		return self.value

	#Provide instance ID of the sensor being read.
	def getInstanceID(self):
		return self.instanceID

		
sensor1 = HumiditySensor(5)#TemperatureSensor(TEMP_SOLDERING, 5)
x = []

for i in range(0,10000):
	x.append(sensor1.sense())

plt.plot(x)
plt.axhline(y=sensor1.minVal, color='r', linestyle='-')
plt.axhline(y=sensor1.maxVal, color='g', linestyle='-')
plt.title('My graph')
plt.show()


