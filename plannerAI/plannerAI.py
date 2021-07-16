#from sensorClass.client_broker_data import *
import csv 
import pandas as pd
import datetime
import requests
import ast


plannerNewInitState = {}
file = '/home/ashwini/Desktop/IOT/dataBase/room01DB.csv'

listOfPerson = ['PPLLOGISTICS1','PPQQUALITY1', 'PPMMAINTENANCE1']
dictAllTypesPeople = {}

objectList =listOfPerson.copy()
updatedInitStateList = []

abvDictObect  = {  'HS':'humitdity',
			   'RT':'roomTemp', 
			   'ST':'solderingTemp', 
			   'OS':'oscilloscope',
			   'TB':'testbentch',
			   'CB':'convyor',
			   'RA': 'tempActuator',
			   'HA': 'humidityAcutator',
			   'IR':'InfraRed',
			   'ES':'esdProtection',
			   'PS':'pressure',
			   'PL':'logistics',
			   'PM':'maintainence',
			   'PQ':'quality',
			   }




def isHigh(newVal, threshold):
	
	if newVal > threshold :
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
			return True
		else :
			return False

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

def isOutputDone(data) :

	if data > 80 :
		return True
	else :
		return False

def isBad(data, str) :

	if str == 'IR':
		
		trueCount = data["True"]
		total = sum(list(data.values()))

		if (float(trueCount)/total) >= 0.60:
			return False
		else :
			return True


	elif str == 'ESD' :
		return not(data)

	elif str == 'SS':
		
		if ( 218.8 >= data >= 215.2 ):
			return False
		else:
			return True

def updateListOfPeople(identity, l_m_q,string):

	#check if already in dict 
	if identity not in dictAllTypesPeople.values() :
		dictAllTypesPeople[ string +' '+ l_m_q +' '+ identity ] = False



def aiPlanner( data, topic ):
	#data.pop(["date", ])

	if 'actuator' in topic :
		for item in data :
			value = data[item]
			plannerNewInitState['isOn ' + item] = isOn(value)
			#print(plannerNewInitState['isOn ' + item])
			#updateListOfPeople(item, listOfPerson[2])

	elif 'sensor' in topic :
		#df = pd.read_csv (file,header = 0, index_col=[0])
		for item in  data :
			value = data[item]

			try :
				
				if 'roomTemp' in topic :
					
					plannerNewInitState['isHigh '+item] = isHigh(value,23.0)
					#updateListOfPeople(item, listOfPerson[2])

				elif 'humidity' in topic :

					plannerNewInitState['isHigh '+item] = isHigh(value,55.0)

				elif 'pressure' in topic :
					plannerNewInitState['isOutputDone ' + item] = isOutputDone(value)
					updateListOfPeople(item, listOfPerson[0],'isInformedLogistics')

				elif ('irSensor' in topic) :
					plannerNewInitState['isBad '+item] = isBad(value, 'IR' )
					updateListOfPeople(item, listOfPerson[1], 'isInformedQuality')

				elif ('ESD' in topic) :
					plannerNewInitState['isBad ' + item] = isBad(value, 'ESD')
					updateListOfPeople(item, listOfPerson[1], 'isInformedQuality')

				elif ('solderingStation' in topic): 
					plannerNewInitState['isBad ' + item] = isBad(value, 'SS' )
					updateListOfPeople(item, listOfPerson[1], 'isInformedQuality')

			except Exception as e :
				#plannerNewInitState[item] = True
				print("-----error in creating init state-----------")
				print(item)
				print(topic)
				print(e)
				print("-----error in creating init state-----------")

			

	elif 'equipment' in topic:
		
		if 'osc'  in topic :
			if 'doCheck' in topic :
				for item in data :
					status = data[item]
					plannerNewInitState['isBadEqu '+item]	= isBadEqu(status, 'osc')
					updateListOfPeople(item, listOfPerson[2], 'isInformedBadEqu')

			elif 'getCalibDate' in topic :
				for item in data :
					date = data[item]
					plannerNewInitState['isDateNear '+item] = isDateNear(date)
					updateListOfPeople(item, listOfPerson[2],'isInformedDate')

		elif 'convyor' in topic :
			for item in data :
				state = data[item] 
				plannerNewInitState['isBadEqu '+item] = isBadEqu(state, 'cb')
				updateListOfPeople(item, listOfPerson[2],'isInformedBadEqu')

		elif 'testBentch'  in topic :
			if 'doCheck' in topic :
				for item in data :
					status = data[item]
					plannerNewInitState['isBadEqu '+item]	= isBadEqu(status,'tb')
					updateListOfPeople(item, listOfPerson[2], 'isInformedBadEqu')

			elif 'getCalibDate' in topic :
				for item in data :
					date = data[item]
					plannerNewInitState['isDateNear '+item] = isDateNear(date)
					updateListOfPeople(item, listOfPerson[2], 'isInformedDate')

	else :
		pass

	#get state info about pepople to be informed.



	# print(plannerNewInitState)
	# print(dictAllTypesPeople)
	

def getObjectType(string):

	resultString = abvDictObect[string[1:3]]

	return resultString

def updateInitState(stateDict_TF):


	initStateString = ''
	#make list of true only elements
	for item in stateDict_TF:
		if stateDict_TF[item] == True:

			#updatedInitStateList.append(item)
			initStateString += '\t\t(' + item +')\n'

	return initStateString


def defineProblemFile():

	
	objectString =''
	goalString = ''

	for item in objectList:
		typeObject  = getObjectType(item)
		objectString += '\t\t ' +item+ ' - '+ typeObject + '\n'

		goal =  getGoalForObeject(item,typeObject) 
		if goal != None :
			goalString += goal + '\n'


	#rint(goalString)
	#print(objectString)


	initState = {**plannerNewInitState, **dictAllTypesPeople}
	stateString = updateInitState(initState)
	#print('*'+stateString)
	
	generateProblemFile( objectString, stateString , goalString)


def updateObjects(idList):
	#to be called if new thing is added to the network

	try:
		for item in  ["date", "time"] :
			idList.remove(item)
	except ValueError:
		pass

	objectList.extend(idList)



def getGoalForObeject(id, ofType):


	if ofType == abvDictObect['HS'] or ofType == abvDictObect['RT']:

		goalstring = '\t\t\t(or\n\t\t\t\t(and (isHigh roomTemp1) (not(isOn tempAct1)) )\n\t\t\t\t(and (not(isHigh roomTemp1)) (isOn tempAct1) ) \n\t\t\t) ;or roomTemp1 tempAct1\n'
		goalstring = goalstring.replace('roomTemp1', id)
		#actuator id 
		actID = 'A' + id[1] + 'A' + id[3:]
		goalstring =goalstring.replace('tempAct1',actID)

	elif  ofType == abvDictObect['TB'] or ofType == abvDictObect['OS'] :
		goalstring = '\t\t\t(not(isDateNear tb1)) ; tb1\n'
		goalstring = goalstring.replace('tb1', id)

		goalstring2 = goalstring
		goalstring2 = goalstring2.replace('isDateNear', 'isBadEqu')

		goalstring = goalstring + goalstring2

	elif ofType == abvDictObect['CB'] :
		goalstring = '\t\t\t(not(isBadEqu tb1)) ;tb1\n'
		goalstring = goalstring.replace('tb1', id)

	elif ofType == abvDictObect['ST'] or ofType == abvDictObect['ES'] or ofType == abvDictObect['IR']:
		goalstring = '\t\t\t(not(isBad ESD1) ); ESD1 quality1 \n'
		goalstring = goalstring.replace('ESD1', id)

	elif ofType == abvDictObect['PS'] :
		goalstring = '\t\t\t(not(isOutputDone tb1)); tb1\n'
		goalstring= goalstring.replace('tb1', id)

	else :
		goalstring = None

	return goalstring


def generateProblemFile( objectTypes, init, goal):
	with open('/home/ashwini/Desktop/IOT/plannerAI/problem_template_empty.txt') as f:
		newText=f.read()

		newText = newText.replace( 'OBJECTS_HERE' ,objectTypes)
		newText = newText.replace('STATE_HERE',init)
		newText = newText.replace('GOAL_HERE', goal)

	with open('/home/ashwini/Desktop/IOT/plannerAI/Problem_generated.pddl', "w") as f:
		f.truncate()
		f.write(newText)

	



