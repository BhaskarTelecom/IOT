import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient



myMQTTClient = AWSIoTMQTTClient("WhoEverClientID") #random key, if another connection using the same key is opened the previous one is auto closed by AWS IOT
myMQTTClient.configureEndpoint("a1etmfjjj6j48x-ats.iot.us-west-2.amazonaws.com", 8883) 

myMQTTClient.configureCredentials(  "/home/bhaskar/IOT_Certificates/Certificates/root-ca.pem.txt", 
                                    "/home/bhaskar/IOT_Certificates/Certificates/private.pem.key", 
                                    "/home/bhaskar/IOT_Certificates/Certificates/certificate.pem.crt") # AWS IOT Certificates in directory of Raspberry PI

myMQTTClient.configureOfflinePublishQueueing(-1) # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2) # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10) # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5) # 5 sec
print ('Initiating Realtime Data Transfer From Raspberry Pi...')
myMQTTClient.connect()

#To publish readings to AWS IOT Server

def customCallback(client,userdata,message):
    print('received message')
    print(message.payload)

print("Receiving Messages from Raspberry Pi")
while True:
    myMQTTClient.subscribe(
        topic="SMS/Temp",
        QoS=1,
        callback=customCallback
        # Message and values will be shown on AWS IOT
        #payload='{" Sensor Type = " + sensorType }'
    )
    #time.sleep(5)

# sensor1 = HumiditySensor(5) #TemperatureSensor(TEMP_SOLDERING, 5)
# x = []

# for i in range(0,10000):
# 	x.append(sensor1.sense())

# plt.plot(x)
# plt.axhline(y=sensor1.minVal, color='r', linestyle='-')
# plt.axhline(y=sensor1.maxVal, color='g', linestyle='-')
# plt.title('My graph')
# plt.show()
    

