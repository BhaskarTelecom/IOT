import numpy as np


class TemperatureSensor():
	"""docstring for TemperatureSensor"""
	sensorType = "temperature"
	unit = "celsius"

	def __init__(self, tempSensorType, instanceID):
		self.instanceID = instanceID
		self.mean = 90
		self.variance = 4
		self.value = 0.0

	def sense(self):
		# self.value = self.value + self.simpleRandom()
		self.value = np.random.Generator.normal(self.mean, self.variance)

		return self.value

sensor = TemperatureSensor(1,3)
print(sensor.sense())
