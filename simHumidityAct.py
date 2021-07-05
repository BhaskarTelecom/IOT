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
  client.subscribe(topicDict["HS"]+"#",qos=QOS)
  time.sleep(0.2)
  

def on_message(client, userdata, msg):
    m_decode=str(msg.payload.decode("utf-8","ignore"))
    dataReceived=json.loads(m_decode) #decode json data

    userdata.humidityAct.updateValue(dataReceived)
    dataSend  = {userdata.humidityAct.getInstanceID() : userdata.humidityAct.getState()}
    publisher_data(topicDict["HA"]+"State",dataSend, client)


class simHumidityAct():
    """docstring for simHumidityAct"""

    #LineNum in int
    #passed as simTime in unit minutes, stored as seconds


    def __init__(self, lineNum, simTime = 5):
        super(simHumidityAct, self).__init__()
        self.lineNum = lineNum
        self.simTime = simTime*60 + 5 
        self.pause = False

        #create instances of room temperature actuator

        id = createInstanceID(self.lineNum, 'A', ABV_DICT["humidityActuator"], 0)
        self.humidityAct = humidityAction(instanceID = id)
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


            time.sleep(0.1)
            currTime = datetime.datetime.now()
            timeDiff  = (currTime - startTime).total_seconds()
        

    def stopSim(self):
        self.simTime = 0 

    def pauseSim(self):
        self.pause = True


def main() :
    simHumidityActClient   = mqtt.Client(clientDict["simHumActClient"], clean_session =False)

    simHumidityActClient.on_connect = on_connect 
    simHumidityActClient.on_message = on_message

    simHumidityActClient.connect(brokerHost, brokerPort,brokerKeepAlive)
    time.sleep(0.1)

    test = simHumidityAct(1)

    userdata = test

    simHumidityActClient.user_data_set(userdata)

    simHumidityActClient.loop_start()
    test.startSim(simHumidityActClient)
    simHumidityActClient.loop_stop()

    simHumidityActClient.disconnect()

if __name__ == "__main__":
    main()