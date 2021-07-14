import os

def rchop(s, suffix):
    if suffix and s.endswith(suffix):
        return s[:-len(suffix)]
    return s

fileList = [ '/home/ashwini/Desktop/IOT/simEquOsc.py',
			'/home/ashwini/Desktop/IOT/simEquTb.py',
			'/home/ashwini/Desktop/IOT/simHumidityAct.py',
			'/home/ashwini/Desktop/IOT/simHumiditySensor.py',
			'/home/ashwini/Desktop/IOT/simLine.py',			
			'/home/ashwini/Desktop/IOT/simRoomTemp.py',
			'/home/ashwini/Desktop/IOT/simTempAct.py',
			'/home/ashwini/Desktop/IOT/simProdServer.py']

cmd = ''
for item in fileList:
	cmd += 'python3 ' + item + ' & '

cmd = rchop(cmd , ' & ')

#print(cmd)
os.system(cmd)