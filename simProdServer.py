from sensorClass.client_broker_data import *
from sensorClass.act_TempAndHumidity import *
from dataBase.dbHandler import *
from plannerAI.plannerAI import *

listOfEquID = []

# Function to call publisher to send data
def publisher_data(input_topic_name,payload_data, myclient):
    publish_data = json.dumps(payload_data,indent=4)
    myclient.publish(input_topic_name,publish_data,QOS)
    #print(publish_data)
    time.sleep(0.1)

def on_connect(client, userdata, flags, rc):
  #print("Connected with result code "+str(rc))
  client.subscribe("room/#",qos=QOS)
  time.sleep(0.2)
  

def on_message(client, userdata, msg):

    m_decode=str(msg.payload.decode("utf-8","ignore"))
    dataReceived=json.loads(m_decode) #decode json data


    aiPlanner(dataReceived, msg.topic)
    defineProblemFile()

    if 'equipment' in msg.topic :
        if 'convyor' not in msg.topic :

            for item in list(dataReceived.keys()):
                if item not in listOfEquID :
                    listOfEquID.append(item)
            #print(listOfEquID)

    if 'getCalibDate' not in msg.topic :
        
        handleData(dataReceived)



class simProdServer():
    """docstring for simProdServer"""

    #LineNum in int
    #passed as simTime in unit minutes, stored as seconds


    def __init__(self, simTime = 5):
        super(simProdServer, self).__init__()

        self.simTime = simTime*60 + 5 
        self.pause = False


        


    def startSim(self, clientName):

        startTime = datetime.datetime.now()
        timeDiff = 0
        sec15Count = 15


        while self.simTime > 0 and not(self.pause) :

            if(int(timeDiff) == 1):

                startTime = currTime
                self.simTime -= 1
                sec15Count  -= 1

            #get calibration date of equipments - 15 sec
                # get list of osc and tb in network - from master db

            if(sec15Count == 0):
                sec15Count = 15

                if listOfEquID :
                    print('---in server 15 sec ---') 

                    for item in listOfEquID :

                        if item[1:3] == 'OS' :
                            #ask for calibration date
                            topic = topicDict['PEO'] 
                        else :
                            topic = topicDict['PET']

                        topic +=  item + "/getCalibDate"
                        publisher_data(topic, "getCalibDate" , clientName)

                        if item[1:3] == 'TB' :
                            topic = topicDict['PET']+item + "/doCheck"
                            publisher_data(topic, "doCheck", clientName)







            time.sleep(0.1)
            currTime = datetime.datetime.now()
            timeDiff  = (currTime - startTime).total_seconds()
        

    def stopSim(self):
        self.simTime = 0 

    def pauseSim(self):
        self.pause = True


def main() :
    simProdServerClient   = mqtt.Client(clientDict["simProdServerClient"], clean_session =False)

    simProdServerClient.on_connect = on_connect 
    simProdServerClient.on_message = on_message 

    simProdServerClient.connect(brokerHost, brokerPort,brokerKeepAlive)
    time.sleep(0.1)

    test = simProdServer(25 )
    userdata = test

    simProdServerClient.user_data_set(userdata)

    simProdServerClient.loop_start()
    test.startSim(simProdServerClient)
    simProdServerClient.loop_stop()

    simProdServerClient.disconnect()

if __name__ == "__main__":
    main()