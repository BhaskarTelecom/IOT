import ssl
import paho.mqtt.client as mqtt
import time
import numpy as np


# AWS IOT certificates       
""" userdata= "Sensor_Data_Receiver"
awshost = "a1etmfjjj6j48x-ats.iot.us-west-2.amazonaws.com"  
awsport = 8883

clientId = "myThingName"
thingName = "SMS_RaspberryPi"

caPath = "/home/bhaskar/IOT_Certificates/Certificates/root-ca.pem.txt"
certPath = "/home/bhaskar/IOT_Certificates/Certificates/certificate.pem.crt"
keyPath = "/home/bhaskar/IOT_Certificates/Certificates/private.pem.key"

connflag = False

def on_connect(client,userdata, msg,flags,rc):
    print("Connection Status: {}".format(rc))


def on_message(client, userdata, msg):
    print(msg.topic+str(msg.payload))


receiver = mqtt.Client("reciever")
receiver.on_connect = on_connect 
receiver.on_message = on_message

receiver.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
receiver.connect(awshost, awsport, keepalive=60)

receiver.loop_start()

while 1==1:
    time.sleep(0.5)
    
    tempreading = np.random.uniform(20.0,25.0)
    receiver.publish("temperature", tempreading, qos=1)
    print("msg sent: temperature " + "%.2f" % tempreading ) """
    

client = mqtt.Client()
client.connect("broker.emqx.io",1883,60)
count = 0
while count<50:
    client.publish("topic/test", "Hello world!");
    time.sleep(1)
    count += 1
client.disconnect();