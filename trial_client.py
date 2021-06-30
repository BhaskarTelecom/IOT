# import paho.mqtt.client as mqtt
# import time

# client_name = "trailClient"




# myclient = mqtt.Client(client_name)
# myclient.on_connect = on_connect
# myclient.on_message = on_message
# myclient.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
# myclient.connect(awshost, awsport, keepalive=60)
# myclient.loop_start()



# time.sleep(0.1)

import ssl
import paho.mqtt.client as mqtt
import time
import numpy as np


# AWS IOT certificates       
userdata= "Sensor_Data_Receiver"
awshost = "a1etmfjjj6j48x-ats.iot.us-west-2.amazonaws.com"  
awsport = 8883

# awshost = "a1etmfjjj6j48x-ats.iot.us-west-2.amazonaws.com"
# awsport = 8883
caPath = "/home/ashwini/Desktop/IOT/Certificates/root-ca.pem.txt"
certPath = "/home/ashwini/Desktop/IOT/Certificates/certificate.pem.crt"
keyPath = "/home/ashwini/Desktop/IOT/Certificates/private.pem.key"


connflag = False

def on_connect(client,userdata, msg,flags,rc):
    global connflag 
    connflag = True
   
    print("Connection Status: {}".format(rc))


def on_message(client, userdata, msg):
    print(msg.topic+str(msg.payload))


receiver = mqtt.Client("receiver")
receiver.on_connect = on_connect 
receiver.on_message = on_message




receiver.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
receiver.connect(awshost, awsport, keepalive=60)

time.sleep(1)

receiver.loop_start()

while 1==1:
    time.sleep(0.5)
    if connflag == True:
        tempreading = np.random.uniform(20.0,25.0)
        receiver.publish("temperature", tempreading, qos=1)
        print("msg sent: temperature " + "%.2f" % tempreading )
    else:
        print("waiting for connection...")