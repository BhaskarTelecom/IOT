from sensorClass.client_broker_data import * 
from sensorClass.prodLine import *

# Function to call publisher to send data
def publisher_data(input_topic_name,payload_data, myclient):
    publish_data = json.dumps(payload_data,indent=4)
    myclient.publish(input_topic_name,publish_data,qos = QOS)
    print("Publishing to :" + input_topic_name )
    time.sleep(0.1)

def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))


	for item in userdata.prodline.pressureSensorList :
		identity = item.getInstanceID()
		client.subscribe(topicDict["PRL"]+identity+"/#")
		print("--Subscribed to :"+topicDict["PRL"]+identity+"/#")
  
def on_message(client, userdata, msg):
	m_decode=str(msg.payload.decode("utf-8","ignore"))
	dataReceived=json.loads(m_decode) #decode json data

	print("Server msg received :"+msg.topic)

	if "pressure" in msg.topic and "clear" in msg.topic :
		for item in userdata.prodline.pressureSensorList:
			if item.getInstanceID() == dataReceived:
				item.clearPressure()
 

class simLine():
	"""docstring for simLine"""

	#LineNum in int
	#passed as simTime in unit minutes, stored as seconds

    # ------- Publish timeline -----------
	# room temp + humidity sensor : every 15 sec
	# solder sensor : every 5 sec
	# convyor belt - will check every 1 Sec 
	# IR sensor - every 5 min - but will sense every 5 sec, will send "false" and "true" count only in the interval of 5 min
	# esd sensor  will check every 1 sec
	# pressure sensor - every 5 sec 

	def __init__(self, lineNum, simTime = 5):
		super(simLine, self).__init__()
		self.lineNum = lineNum
		self.simTime = simTime*60 + 5 

		self.pause = False

		#create the prodLine instance
		self.prodline = prodLine(self.lineNum)

		self.solderIron = {}
		self.convBelt = {}
		self.irSensor = {}
		self.esdSensor ={}
		self.pressure = {}

		self.topicFinal = ""

	def startSim(self, clientName):

		startTime = datetime.datetime.now()
		timeDiff = 0
		sec5Count = 5
		min1Count = 60 



		while self.simTime > 0 and not(self.pause) :

			if(int(timeDiff) == 1):

				startTime = currTime
				self.simTime -= 1
				sec5Count -= 1
				min1Count  -= 1

				#sense IR sensor counts
				for x in range(self.prodline.iCount):
					 self.prodline.irSensorList[x].objectDetected()


			# check 5 seconds have passed  or not
			if(sec5Count == 0) :
				sec5Count = 5 

				#sense esd sensor status
				for x in range(self.prodline.ESDcount):
					key = self.prodline.esdSensorList[x].getInstanceID()
					self.esdSensor[key]  = self.prodline.esdSensorList[x].getStatus()
					self.topicFinal += "_"+key

				publisher_data(topicDict["ES"] +self.topicFinal ,self.esdSensor,clientName)
				self.topicFinal=""	

				#sense convyor belt status
				for x in range(self.prodline.cBcount):
					key = self.prodline.convBeltList[x].getInstanceID()
					self.convBelt[key]  = self.prodline.convBeltList[x].getState()
					self.topicFinal += "_"+key

				publisher_data(topicDict["CB"] +self.topicFinal,self.convBelt,clientName)
				self.topicFinal=""

				#sense soldering station temperature values
				for x in range(self.prodline.sCount):
					key = self.prodline.solderSensList[x].getInstanceID()
					self.solderIron[key] =  self.prodline.solderSensList[x].sense()
					self.topicFinal += "_"+ key

				publisher_data(topicDict["ST"] +self.topicFinal,self.solderIron,clientName)
				self.topicFinal=""
				#print(self.solderIron)

				#sense pressure/weight values
				for x in range(self.prodline.pCount):
					key = self.prodline.pressureSensorList[x].getInstanceID()
					self.pressure[key] =  self.prodline.pressureSensorList[x].measure()
					self.topicFinal += "_"+key

				publisher_data(topicDict["PS"]+self.topicFinal ,self.pressure,clientName)
				self.topicFinal=""
				#print(self.pressure)

				


			#check if 1 min have passed or not
			if(min1Count == 0):
				min1Count = 60


				#send IR sensor counts
				for x in range(self.prodline.iCount):
					key =  self.prodline.irSensorList[x].getInstanceID()
					self.irSensor[key] =  self.prodline.irSensorList[x].getCount()
					self.prodline.irSensorList[x].clearCount()
					self.topicFinal += "_"+key

				publisher_data(topicDict["IR"]+self.topicFinal ,self.irSensor,clientName)
				self.topicFinal=""
				#print(self.irSensor)

				print("-----Line : 1 min over----")





			currTime = datetime.datetime.now()
			timeDiff  = (currTime - startTime).total_seconds()
		
		self.stopSim()

		
	def stopSim(self):
		self.simTime = 0 
		print("----Simulation endded----")

	def pauseSim(self):
		self.pause = True

def main() :
	simLineClient   = mqtt.Client(clientDict["simLineClient"], clean_session =False)

	simLineClient.on_connect = on_connect 
	simLineClient.on_message = on_message

	simLineClient.connect(brokerHost, brokerPort,brokerKeepAlive)
	time.sleep(0.2)

	test = simLine(1,SIMULATION_TIME)

	userdata = test
	simLineClient.user_data_set(userdata)

	simLineClient.loop_start()
	test.startSim(simLineClient)
	simLineClient.loop_stop()

	simLineClient.disconnect()

if __name__ == "__main__":
    main()









