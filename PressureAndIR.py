import random
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

#Reference
#https://www.researchgate.net/figure/Touch-sensing-capacity-of-the-sensor-a-Change-in-capacitance-before-and-after-several_fig4_315906018
#https://www.researchgate.net/figure/Fig4Calibration-curve-of-IR-sensorOutput-voltage-calibration-a-Voltage-vs-distance_fig1_272355203

class PressureSensor:

    sensorType = "pressure"
    unit = "kPa"

    def __init__(self, instanceID ,avgPressure=1, minPressure=0.25, threshPressure = 100):
        self.minPressure = minPressure
        self.threshPressure = threshPressure
        self.instanceID = instanceID
        self.avgPressure = avgPressure

        self.value = np.random.normal(minPressure , 0.03  )

    def measure(self):
        
        self.value += np.random.normal(self.avgPressure, 0.03)

        return self.value

    def clearPressure(self):
        self.value = 0


    def getThreshold(self, check = False):
        #when check = True, return whether current pressure more than threshold
        if check :
            if(self.threshPressure > self.value):
                return False 
            else :
                return True 
        else :         
            return self.threshPressure

    def getInstanceID(self):
        return self.instanceID


class IrSensor:
    sensorType = "IR"
    unit = "cm"

    def __init__(self,instanceID, conveyorBeltWidth = 35):
        self.conveyorBeltWidth = conveyorBeltWidth  #in cm
        self.instanceID = instanceID
        self.value = 0.0

        self.totalTrue = 0
        self.totalFalse = 0


    def measure(self):
        self.value = np.random.choice(np.linspace(self.conveyorBeltWidth, 0,10),1)
        return self.value

    def objectDetected(self):
        distance = self.measure()

        if(distance <= 0.75 * self.conveyorBeltWidth ):
            self.totalTrue += 1           
        else : 
            self.totalFalse += 1           

    def getCount(self):

        return {"True": self.totalTrue , "False":self.totalFalse}

    def clearCount(self):
        self.totalTrue = 0
        self.totalFalse = 0


    def getInstanceID(self):
        return self.instanceID


class EsdProtectionSensor:
    sensorType = "Esd"

    def __init__(self,instanceID, proximityMinValue =1000, proximityMaxValue=10000, tensionMinvalue=1000, tensionMaxvalue=10000):
        self.proximityMinValue = proximityMinValue
        self.proximityMaxValue = proximityMaxValue
        self.tensionMinvalue = tensionMinvalue
        self.tensionMaxvalue = tensionMaxvalue
        self.proximityValue = 0.0
        self.tensionValue = 0.0
        self.instanceID = instanceID

        self.result = False
        self.oldResult = self.result


    def proximityMeasure(self):
        self.proximityValue = np.random.choice(np.linspace(self.proximityMinValue, self.proximityMaxValue,10000),1)
        if(self.proximityValue >= 3000 ):
            return True
        else : 
            return False

    def tensionMeasure(self):
        self.tensionValue = np.random.choice(np.linspace(self.tensionMinvalue, self.tensionMaxvalue,10000),1)

        if(self.tensionValue >= 3000 ):
            return True
        else : 
            return False

    def EsdCheckPass(self):
        if(self.tensionMeasure() & self.proximityMeasure()):
            temp =  True
        else:
            temp = False

        [self.result] = random.choices([self.result,temp], weights = [0.7, 0.3], k=1)

    def getStatus(self):

        return self.result

    def getInstanceID(self):
        return self.instanceID
        

# pressure = PressureSensor(25,1, 10,1)
# plt.plot(pressure.measure())
# #plt.plot( 250+ 250*signal.sawtooth(2 * np.pi * pressure.measure() ))
# t  = np.linspace(0, 1, 1000)
# values = pressure.measure()
# print(np.shape(values))
# plt.show()
