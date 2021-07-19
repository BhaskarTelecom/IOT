from sensorClass.client_broker_data import *
from sensorClass.act_TempAndHumidity import *
from dataBase.dbHandler import *
from plannerAI.plannerAI import *

import smtplib,ssl
from email.message import EmailMessage


listOfEquID = []

# Function to call publisher to send data
def publisher_data(input_topic_name,payload_data, myclient):
    publish_data = json.dumps(payload_data,indent=4)
    myclient.publish(input_topic_name,publish_data,QOS)
    print("Publishing to :" + input_topic_name )
    time.sleep(0.1)

def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))

  client.subscribe("room/#",qos=QOS)
  print("--Subscribed to :"+"room/#")
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
        min1Count = 60


        while self.simTime > 0 and not(self.pause) :

            if(int(timeDiff) >= 1):

                startTime = currTime
                self.simTime -= 1
                sec15Count  -= 1
                min1Count -= 1

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

                GetAIPlan(clientName)


            time.sleep(0.1)
            currTime = datetime.datetime.now()
            timeDiff  = (currTime - startTime).total_seconds()

        self.stopSim()
        

    def stopSim(self):
        self.simTime = 0 
        print("----Simulation endded----")

    def pauseSim(self):
        self.pause = True


def main() :
    simProdServerClient   = mqtt.Client(clientDict["simProdServerClient"], clean_session =False)

    simProdServerClient.on_connect = on_connect 
    simProdServerClient.on_message = on_message 

    simProdServerClient.connect(brokerHost, brokerPort,brokerKeepAlive)
    time.sleep(0.1)

    test = simProdServer(SIMULATION_TIME )
    userdata = test

    simProdServerClient.user_data_set(userdata)

    simProdServerClient.loop_start()
    test.startSim(simProdServerClient)
    simProdServerClient.loop_stop()

    simProdServerClient.disconnect()




#--------------AI planner action decoding---------------------

def GetAIPlan(clientName):
    data = {'domain': open("/home/bhaskar/IOT/IOT/IOT-devAshwini/plannerAI/Domain.pddl", 'r').read(),
    'problem' : open("/home/bhaskar/IOT/IOT/IOT-devAshwini/plannerAI/Problem_generated.pddl", 'r').read()}
    response = requests.post('http://solver.planning.domains/solve', json = data).json()

    with open('/home/bhaskar/IOT/IOT/IOT-devAshwini/plannerAI/AIPlan.txt', "w") as f:
      f.truncate()
      f.write(str(response))

    if response['status'] == 'ok' :

      for act in response['result']['plan'] :
          action , param1, param2 = act['name'][1:-1].split()
          try :
            callActions(action , param1.upper(), param2.upper(),clientName)
          except Exception as e :
            print(act['name'][1:-1])
            print("Error - More than 3 parameters to pass in call action")
            print(e)

    else:

        if 'The empty plan solves it' in response['result']['output'] :
            print('No action needed')
        else :
            print("Cannot Find plan!!")
            print(response['status'])
            print(response['result']['output'])



    # with open("/home/ashwini/Desktop/IOT/plannerAI/Problem_generated.txt", 'r') as f:

    #     text = f.read()
    #     item = ast.literal_eval(text)
    #     #['status', 'result']

    #     for act in item['result']['plan'] :
    #         action , param1, param2 = act['name'][1:-1].split()
    #         callActions(action, param1.upper(), param2.upper(),clientName )


def callActions(actionName, firstParameter, secondParameter,clientName ):

    if actionName == 'turnon':
        actionTurnOn(firstParameter,secondParameter,clientName)
    elif actionName == 'turnoff':
        actionTurnOff(firstParameter,secondParameter,clientName)
    elif actionName == 'aleartmaintainancebadequ':
        actionAleartMaintainanceBadEqu(firstParameter,secondParameter,clientName)
    elif actionName == 'aleartquality':
        actionAleartQuality(firstParameter,secondParameter,clientName)
    elif actionName == 'aleartmaintainancedate':
        actionAleartMaintainanceDate(firstParameter,secondParameter,clientName)
    elif actionName == 'aleartlogistics':
        actionAleartLogistics(firstParameter,secondParameter,clientName)
    else :
        print('unknown action parsed')
        print(actionName)


def actionTurnOn(sensor, actuator,clientName):
    updateStateAsperPlan(actuator,4 )

    publisher_data(topicDict["P"+actuator[1:3]]+actuator, "ON", clientName)
    
    

def actionTurnOff(sensor, actuator,clientName):
    updateStateAsperPlan(actuator,3 )

    publisher_data(topicDict["P"+actuator[1:3]]+actuator, "OFF", clientName)
    
        

def actionAleartMaintainanceDate(equ, maintainance,clientName):
    updateStateAsperPlan(equ,4 )
    updateStateAsperPlan(maintainance+' '+equ,6)
    sendEmail('Dear '+maintainance+',\n\nCalibration date of '+equ+'is near, please perform the task.\n\n\nRegards\nProduction team\n',maintainance,'Do calibration of '+equ )

def actionAleartMaintainanceBadEqu(equ, maintainance,clientName):
    #make equipment good and alert maintaniance

    updateStateAsperPlan(equ,5 )
    updateStateAsperPlan(maintainance+' '+equ,7)
    sendEmail('Dear '+maintainance+',\n\nThe '+equ+'is not working effectively, please perform maintainence of the same.\n\n\nRegards\nProduction team\n',maintainance,'Do maintainence of '+equ )


def actionAleartLogistics(pressureSensor, logistics,clientName):

    updateStateAsperPlan(pressureSensor,2 )
    publisher_data(topicDict["PRL"]+pressureSensor+"/clear",pressureSensor ,clientName)

    updateStateAsperPlan(logistics+' '+pressureSensor,9)
    sendEmail('Dear '+logistics+',\n\nThe '+pressureSensor+' is showing product is ready to be dispatch, kindly  transfer the produced goods to mentioned location.\n\n\nRegards\nProduction team\n',logistics,'Goods ready for transport :'+pressureSensor )

def actionAleartQuality(qualitySensor, quality,clientName):
    

    updateStateAsperPlan(qualitySensor,1 )
    updateStateAsperPlan(quality+' '+qualitySensor,8)
    sendEmail('Dear '+quality+',\n\nThe '+qualitySensor+'is not working as per our quality standards, please look into the incident and take neccessary actions.\n\n\nRegards\nProduction team\n',quality,'Bad Quality issue Observed in : '+qualitySensor )

# d = {'IRcount1' :{"True" : 45, "False" : 5} }
# t = "room/room1/prodLine1/sensor/irSensor/IRcount1"
# aiPlanner(d,t)

def updateStateAsperPlan(identity,number):

    initState = {**plannerNewInitState, **dictAllTypesPeople}

    stringList = ['isHigh', 'isBad', 'isOutputDone', 'isOn', 'isDateNear', 
                'isBadEqu','isInformedDate', 'isInformedBadEqu',
                 'isInformedQuality', 'isInformedLogistics' ]


    string = stringList[number] + ' ' + identity 


    if string in initState :
        if initState[string] == True :
            initState[string] = False
    else :
        print("not found")
        print(string)

def sendEmail(data, to, subject):
    
    msg = EmailMessage()
    msg.set_content(data)

    msg['Subject'] = subject
    msg['From'] = listOfEmailID['server']
    msg['To'] = listOfEmailID[to]

    username = 'linuxgupta.test@gmail.com'
    password = 'linuxTest1'

    smtp_server = 'smtp.gmail.com'
    port = 587


    context = ssl.create_default_context()

    # Try to log in to server and send email
    try:
        server = smtplib.SMTP(smtp_server,port)
        server.ehlo() # Can be omitted
        server.starttls(context=context) # Secure the connection
        server.ehlo() # Can be omitted
        server.login(username, password)
        server.send_message( msg)
    # TODO: Send email here
    except Exception as e:
    # Print any error messages to stdout
        print(e)
    finally:
        server.quit() 

if __name__ == "__main__":

    main()