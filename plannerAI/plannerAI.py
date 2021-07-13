#from sensorClass.client_broker_data import *
import csv 
import pandas as pd
import datetime


plannerNewInitState = {}
file = '/home/ashwini/Desktop/IOT/dataBase/room01DB.csv'

def isHigh(newVal, oldVal):
	
	if newVal > oldVal :
		return True
	else :
		return False

def isOn(sensorData):

	if sensorData == 'ON':
		return True
	else:
		return False

def isBadEqu(sensorData,isTb_osc_cb):

	if isTb_osc_cb == 'osc' :
		if sensorData == "Pass" :
			return False
		else :
			return True

	elif isTb_osc_cb == 'cb':
		if sensorData == 'STOP' :
			return False
		else :
			return True

	elif isTb_osc_cb == 'tb':
		if 'F' in sensorData :
			return True
		else:
			return False


def isDateNear(data):
	date = datetime.datetime.strptime(data, '%d/%m/%Y')
	diff = (date-datetime.datetime.now()).days 

	if  diff > 10 :
		return False
	else :
		return True


def aiPlanner( data, topic ):
	#data.pop(["date", ])

	if 'actuator' in topic :
		for item in data :
			value = data[item]
			plannerNewInitState[item] = isOn(value)

	elif 'sensor' in topic:
		df = pd.read_csv (file,header = 0, index_col=[0])
		for item in  data :
			value = data[item]

			try :
				df = df[item]
				df = df.dropna()
				prevVal = df.iloc[-1]
				plannerNewInitState[item] = isHigh(value , prevVal)
			except :
				plannerNewInitState[item] = True

			

	elif 'equipment' in topic:
		
		if 'osc'  in topic :
			if 'doCheck' in topic :
				for item in data :
					status = data[item]
					plannerNewInitState[item+'BadEqu']	= isBadEqu(status, 'osc')

			elif 'getCalibDate' in topic :
				for item in data :
					date = data[item]
					plannerNewInitState[item+'Date'] = isDateNear(date)

		elif 'convyor' in topic :
			for item in data :
				state = data[item] 
				plannerNewInitState[item+'BadEqu'] = isBadEqu(sensorData, 'cb')

		elif 'testBentch'  in topic :
			if 'doCheck' in topic :
				for item in data :
					status = data[item]
					plannerNewInitState[item+'BadEqu']	= isBadEqu(status,'tb')

			elif 'getCalibDate' in topic :
				for item in data :
					date = data[item]
					plannerNewInitState[item+'Date'] = isDateNear(date)

	else :
		pass

	print(plannerNewInitState)
	

# d = {"keyName" : 'ON', "keyTwo" : "OFF"}
# t = "actuator"
# aiPlanner(d,t)


