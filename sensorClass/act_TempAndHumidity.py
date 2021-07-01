import numpy as np
import matplotlib.pyplot as plt
import math 


class tempAction:
	OFF = "OFF"
	ON =  "ON"

	def __init__(self, instanceID):
		self.status = self.OFF 
		self.instanceID = instanceID
		self.setpoint = 23

	def changeState(self, state):
		self.status = state

	def getState(self):
		return self.status 

	def updateValue(self, dataReceived):

		dataReceived = [*dataReceived.values()]
		avgValue = sum(dataReceived)/float(len(dataReceived))
		if avgValue > self.setpoint:
			self.changeState(self.ON)
		else :
			self.changeState(self.OFF)

	def getInstanceID(self):
		return self.instanceID

class humidityAction:
	OFF = "OFF"
	ON =  "ON"

	def __init__(self, instanceID):
		self.status = self.OFF 
		self.instanceID = instanceID
		self.setpoint = 56


	def changeState(self, state):
		self.status = state

	def getState(self):
		return self.status 

	def updateValue(self, dataReceived):
		dataReceived = [*dataReceived.values()]
		avgValue = sum(dataReceived)/float(len(dataReceived))
		if avgValue > self.setpoint:
			self.changeState(self.ON)
		else :
			self.changeState(self.OFF)

	def getInstanceID(self):
		return self.instanceID

