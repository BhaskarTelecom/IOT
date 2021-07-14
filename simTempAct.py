from sensorClass.client_broker_data import *
from sensorClass.act_TempAndHumidity import *


# Function to call publisher to send data
def publisher_data(input_topic_name,payload_data, myclient):
    publish_data = json.dumps(payload_data,indent=4)
    myclient.publish(input_topic_name,publish_data,QOS)
    #print(publish_data)
    time.sleep(0.1)

def on_connect(client, userdata, flags, rc):
  #print("Connected with result code "+str(rc))
  client.subscribe("room/+/sensor/roomTemp/#",qos=QOS)
  time.sleep(0.2)
  

def on_message(client, userdata, msg):

    m_decode=str(msg.payload.decode("utf-8","ignore"))
    dataReceived=json.loads(m_decode) #decode json data

    userdata.roomTempAct.updateValue(dataReceived)



class simTempAct():
    """docstring for simTempAct"""

    #LineNum in int
    #passed as simTime in unit minutes, stored as seconds


    def __init__(self, lineNum, simTime = 5):
        super(simTempAct, self).__init__()
        self.lineNum = lineNum
        self.simTime = simTime*60 + 5 
        self.pause = False


        #create instances of room temperature actuator

        id = createInstanceID(self.lineNum, 'A', ABV_DICT["roomtempActuator"], 0)
        self.roomTempAct = tempAction(instanceID = id)
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

                dataSend = {self.roomTempAct.getInstanceID() : self.roomTempAct.getState()}
                publisher_data(topicDict["RA"]+"State", dataSend, clientName)




            time.sleep(0.1)
            currTime = datetime.datetime.now()
            timeDiff  = (currTime - startTime).total_seconds()
        

    def stopSim(self):
        self.simTime = 0 

    def pauseSim(self):
        self.pause = True


def main() :
    simTempActClient   = mqtt.Client(clientDict["simTempActClient"], clean_session =False)

    simTempActClient.on_connect = on_connect 
    simTempActClient.on_message = on_message

    simTempActClient.connect(brokerHost, brokerPort,brokerKeepAlive)
    time.sleep(0.1)

    test = simTempAct(1,25)

    userdata = test

    simTempActClient.user_data_set(userdata)

    simTempActClient.loop_start()
    test.startSim(simTempActClient)
    simTempActClient.loop_stop()

    simTempActClient.disconnect()

if __name__ == "__main__":
    main()