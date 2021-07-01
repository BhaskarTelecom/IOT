import numpy as np
import matplotlib.pyplot as plt
import math 


class tempAction:
	OFF = 0
	ON =  1

	def __init__(self, instanceID):
		self.status = self.OFF 
		self.instanceID = instanceID

	def changeState(self, state):
		self.status = state

	def getState(self):
		return self.state 

	def getInstanceID(self):
		return self.instanceID

class humidityAction:
	OFF = 0
	ON =  1

	def __init__(self, instanceID):
		self.status = self.OFF 
		self.instanceID = instanceID

	def changeState(self, state):
		self.status = state

	def getState(self):
		return self.state 

	def getInstanceID(self):
		return self.instanceID

