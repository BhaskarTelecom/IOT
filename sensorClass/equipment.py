import numpy as np
import math 
import random

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
	RUN  = "RUN"
	HALT = "HALT"
	STOP = "STOP"

	def __init__(self, instanceID):
		self.instanceID = instanceID
		self.setState(self.RUN)
	
	def getInstanceID(self):
		return self.instanceID	

	def setState(self, state):

		if state in [self.RUN,self.HALT,self.STOP]:
			self.state = state
		else :
			self.state = self.STOP

	def getState(self):

		[self.state] = random.choices([self.state,self.RUN,self.HALT,self.STOP], weights = [.8,0.1,0.098,0.002], k=1)
		return self.state


class testBench:
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

		variance = random.choices( [self.VOLT_VAR-0.03, self.VOLT_VAR-0.01,self.VOLT_VAR],weights=[0.98,0.019,0.001], k=1)

		return   np.random.normal(mean, variance )

	def getCurrent(self, minMax):

		if(minMax == self.VOLT_CURR_MAX):
			mean = self.MAX_MEAN_CURR
		else :
			mean = self.MIN_MEAN_CURR

		variance = random.choices( [self.CURR_VAR-0.03, self.CURR_VAR-0.01, self.CURR_VAR],weights=[0.98,0.019,0.001],k=1)
		return  np.random.normal(mean , variance)

	def getToBeCalibDate(self):
		return self.toBeCalibDate

	def doSelfCheck(self):

		error = 0.000000001
		result = ''
		#check min range of voltage channel
		value  = self.getVoltage(self.VOLT_CURR_MIN)
		if (self.VOLT_VAR - error) > abs(value - self.MIN_MEAN_VOLT):
			result += 'P'
		else:
			result += 'F'


		#check max range of voltage channel
		value  = self.getVoltage(self.VOLT_CURR_MAX)
		if (self.VOLT_VAR - error) > abs(value - self.MAX_MEAN_VOLT):
			result += 'P'
		else:
			result += 'F'


		#check min value of current channel
		value  = self.getCurrent(self.VOLT_CURR_MIN)
		if (self.CURR_VAR - error) > abs(value - self.MIN_MEAN_CURR):
			result += 'P'
		else:
			result += 'F'

		#check max value of current channel
		value  = self.getCurrent(self.VOLT_CURR_MAX)
		if (self.CURR_VAR -error) > abs(value - self.MAX_MEAN_CURR):
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

# tb1 = testBench(3)
# print(tb1.getToBeCalibDate())
#print(tb1.doSelfCheck())
# print(tb1.getVoltage(tb1.VOLT_CURR_MAX))
# print(tb1.getVoltage(tb1.VOLT_CURR_MIN))

# print(tb1.getCurrent(tb1.VOLT_CURR_MAX))
# print(tb1.getCurrent(tb1.VOLT_CURR_MIN))
