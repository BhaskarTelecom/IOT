import paho.mqtt.client as mqtt
import time

client_name = "trailClient"


awshost = "a1etmfjjj6j48x-ats.iot.us-west-2.amazonaws.com"
awsport = 8883
caPath = "/home/ashwini/Desktop/IOT/Certificates/root-ca.pem.txt"
certPath = "/home/ashwini/Desktop/IOT/Certificates/certificate.pem.crt"
keyPath = "/home/ashwini/Desktop/IOT/Certificates/public.pem.key"


myclient = mqtt.Client(client_name)
myclient.on_connect = on_connect
myclient.on_message = on_message
myclient.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
myclient.connect(awshost, awsport, keepalive=60)
myclient.loop_start()



time.sleep(0.1)