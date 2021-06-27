import numpy as np
import matplotlib.pyplot as plt
import math 
import enum

class oscilloscope():
	"""docstring for oscilloscope"""
	toBeCalibDate = "12102021" #in DD-MM-YYYY format


	def __init__(self, instanceID):
		self.instanceID = instanceID

	def getInstanceID(self):
		return self.instanceID

	def getToBeCalibDate(self):
		return self.toBeCalibDate

	def doSelfCheck(self):
		return np.random.choice(["Pass", "Fail"],  p=[0.985, 0.015])
 
class conveyorBelt():
	"""docstring for conveyorBelt"""
	RUN  = 0
	HALT = 1
	STOP = 2

	def __init__(self, instanceID):
		self.instanceID = instanceID
		self.setState(self.STOP)
	
	def getInstanceID(self):
		return self.instanceID	

	def setState(self, state):

		if(state <= self.STOP and state >= self.RUN):
			self.state = state
		else :
			self.state = self.STOP

	def getState(self):
		return self.state


class testBench(object):
	"""docstring for testBench"""
	VOLT_CURR_MIN = False
	VOLT_CURR_MAX = True

	VOLT_VAR = 0.13 #Pass is 0.1
	CURR_VAR = 0.08 #Pass is 0.05

	MAX_MEAN_VOLT = 5 #5V
	MIN_MEAN_VOLT = 0 #0V

	MAX_MEAN_CURR = 20 #20mA
	MIN_MEAN_CURR = 4  #4mA

	toBeCalibDate = "12092021" #in DD-MM-YYYY format


	def __init__(self, instanceID):
		self.instanceID = instanceID
		
	def getInstanceID(self):
		return self.instanceID

	def getVoltage(self, minMax):

		if(minMax == self.VOLT_CURR_MAX):
			mean = self.MAX_MEAN_VOLT
		else :
			mean = self.MIN_MEAN_VOLT

		return mean + np.random.normal(0, self.VOLT_VAR)

	def getCurrent(self, minMax):

		if(minMax == self.VOLT_CURR_MAX):
			mean = self.MAX_MEAN_CURR
		else :
			mean = self.MIN_MEAN_CURR

		return mean + np.random.normal(0, self.CURR_VAR)

	def getToBeCalibDate(self):
		return self.toBeCalibDate

	def doSelfCheck(self):

		result = ''
		#check min range of voltage channel
		value  = self.getVoltage(self.VOLT_CURR_MIN)
		if (self.VOLT_VAR - 0.00000001) > abs(value - self.MIN_MEAN_VOLT):
			result += 'P'
		else:
			result += 'F'


		#check max range of voltage channel
		value  = self.getVoltage(self.VOLT_CURR_MAX)
		if (self.VOLT_VAR - 0.00000001) > abs(value - self.MAX_MEAN_VOLT):
			result += 'P'
		else:
			result += 'F'


		#check min value of current channel
		value  = self.getCurrent(self.VOLT_CURR_MIN)
		if (self.CURR_VAR - 0.00000001) > abs(value - self.MIN_MEAN_CURR):
			result += 'P'
		else:
			result += 'F'

		#check max value of current channel
		value  = self.getCurrent(self.VOLT_CURR_MAX)
		if (self.CURR_VAR - 0.00000001) > abs(value - self.MAX_MEAN_CURR):
			result += 'P'
		else:
			result += 'F'

		return result

# osc1 = oscilloscope(1)
# print(osc1.getToBeCalibDate() )
# print(osc1.doSelfCheck())

# conv1 =conveyorBelt(2)
# print(conv1.getState())
# print(conv1.setState(conv1.RUN))
# print(conv1.getState())

tb1 = testBench(3)
# print(tb1.getToBeCalibDate())
#print(tb1.doSelfCheck())
# print(tb1.getVoltage(tb1.VOLT_CURR_MAX))
# print(tb1.getVoltage(tb1.VOLT_CURR_MIN))

# print(tb1.getCurrent(tb1.VOLT_CURR_MAX))
# print(tb1.getCurrent(tb1.VOLT_CURR_MIN))
count =0
# for i in range(0,10000):
# 	if(tb1.doSelfCheck() == 'PPPP'):
# 		count+=1

# print(count/10000)

# x1 = []
# x2 = []

# for i in range(0,10000):
# 	x1.append(tb1.getVoltage(tb1.VOLT_CURR_MAX))
# 	x2.append(tb1.getVoltage(tb1.VOLT_CURR_MIN))

# plt.plot(x)
# plt.axhline(y=tb1.VOLT_CURR_MIN, color='r', linestyle='-')
# plt.axhline(y=sensor1.maxVal, color='g', linestyle='-')
# plt.title('My graph')
# plt.show()