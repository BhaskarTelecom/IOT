import paho.mqtt.client as mqtt 
from random import randrange, uniform
import ssl
import time


""" userdata= "Sensor_Data_Receiver"
awshost = "a1etmfjjj6j48x-ats.iot.us-west-2.amazonaws.com"  
awsport = 8883

caPath = "/home/bhaskar/IOT_Certificates/Certificates/root-ca.pem.txt"
certPath = "/home/bhaskar/IOT_Certificates/Certificates/certificate.pem.crt"
keyPath = "/home/bhaskar/IOT_Certificates/Certificates/private.pem.key"

clientId = "myThingName"
thingName = "SMS_RaspberryPi"

def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc) )
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("temperature" , 1 )

def on_message(client, userdata, msg):
    print("topic: "+msg.topic)
    print("payload: "+str(msg.payload))

#def on_log(client, userdata, level, msg):
#    print(msg.topic+" "+str(msg.payload))

mqttc = mqtt.Client('client')
mqttc.on_connect = on_connect
mqttc.on_message = on_message
#mqttc.on_log = on_log


mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)

mqttc.connect(awshost, awsport, keepalive=60)

mqttc.loop_forever() """

# This is the Subscriber

def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe("topic/test")

def on_message(client, userdata, msg):
  if msg.payload.decode() == "Hello world!":
    print("Yes!")
    # client.disconnect()
    
client = mqtt.Client()
client.connect("broker.emqx.io",1883,60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()