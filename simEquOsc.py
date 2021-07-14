from sensorClass.client_broker_data import *
from sensorClass.equipment import *


# Function to call publisher to send data
def publisher_data(input_topic_name,payload_data, myclient):
    publish_data = json.dumps(payload_data,indent=4)
    myclient.publish(input_topic_name,publish_data,QOS)
    #print(publish_data)
    time.sleep(0.1)

def on_connect(client, userdata, flags, rc):
  #print("Connected with result code "+str(rc))

  id = userdata.osc.getInstanceID()
  client.subscribe(topicDict["PEO"]+id+"/#", QOS )
  time.sleep(0.1)
  

def on_message(client, userdata, msg):

    m_decode=str(msg.payload.decode("utf-8","ignore"))
    dataReceived=json.loads(m_decode) #decode json data

    print("date received in OSC")
    if dataReceived == userdata.topicListSend[0]:
        newTopic = topicDict["OS"]+userdata.osc.getInstanceID()+"/"+dataReceived
        data = {userdata.osc.getInstanceID(): userdata.osc.getToBeCalibDate()}
        publisher_data(newTopic, data, client)

    elif  dataReceived == userdata.topicListSend[1] :
        newTopic = topicDict["OS"]+userdata.osc.getInstanceID()+"/"+dataReceived
        data = {userdata.osc.getInstanceID(): userdata.osc.doSelfCheck()}
        publisher_data(newTopic, data, client)



class simEquOsc():
    """docstring for simEquOsc"""

    #LineNum in int
    #passed as simTime in unit minutes, stored as seconds


    def __init__(self, lineNum, simTime = 5):
        super(simEquOsc, self).__init__()
        self.lineNum = lineNum
        self.simTime = simTime*60 + 5 
        self.pause = False

        self.topicListSend =["getCalibDate","doCheck" ]


        #create instances of room temperature actuator

        id = createInstanceID(self.lineNum, 'E', ABV_DICT["oscilloscope"], 0)
        self.osc = oscilloscope(instanceID = id)
        print(id)


    def startSim(self, clientName):

        startTime = datetime.datetime.now()
        timeDiff = 0
        sec15Count = 15


        while self.simTime > 0 and not(self.pause) :

            if(int(timeDiff) == 1):

                startTime = currTime
                self.simTime -= 1
                sec15Count  -= 1

            if sec15Count == 0:
                sec15Count = 15

                newTopic = topicDict["OS"]+self.osc.getInstanceID()+"/"+self.topicListSend[1]
                data = {self.osc.getInstanceID(): self.osc.doSelfCheck()}
                publisher_data(newTopic, data, clientName)


            time.sleep(0.1)
            currTime = datetime.datetime.now()
            timeDiff  = (currTime - startTime).total_seconds()
        

    def stopSim(self):
        self.simTime = 0 

    def pauseSim(self):
        self.pause = True


def main() :
    simEquOscClient   = mqtt.Client(clientDict["simEquOscClient"], clean_session =False)

    simEquOscClient.on_connect = on_connect 
    simEquOscClient.on_message = on_message

    simEquOscClient.connect(brokerHost, brokerPort,brokerKeepAlive)
    time.sleep(0.1)

    test = simEquOsc(1,25)

    userdata = test

    simEquOscClient.user_data_set(userdata)

    simEquOscClient.loop_start()
    test.startSim(simEquOscClient)
    simEquOscClient.loop_stop()

    simEquOscClient.disconnect()

if __name__ == "__main__":
    main()