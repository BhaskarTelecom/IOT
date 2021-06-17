
class sensorClass(object):
	"""docstring for sensorClass"""
	def __init__(self, arg):
		
	def __call__(self)
		

class TemperatureSensor:
	sensorType = “temperature"
	instanceID = “32kd403ks"
	unit = “celsius"

	def __init__(self, averageTemperature, temperatureVariation, minTemperature, maxTemperature):
	self.averageTemperature = averageTemperature
	self.temperatureVariation = temperatureVariation
	self.minTemperature = minTemperature
	self.maxTemperature = maxTemperature
	self.value = 0.0
	def sense(self):
	# self.value = self.value + self.simpleRandom()
	self.value = self.complexRandom()
	return self.value
	def simpleRandom(self):
	value = self.minTemperature + (random() * ((self.maxTemperature - self.minTemperature)))
	return value
	def complexRandom(self):
	value = self.averageTemperature * (1 + ((self.temperatureVariation / 100) * (3 * random() - 1)))
	value = max(value, self.minTemperature)
	value = min(value, self.maxTemperature)
	return value 