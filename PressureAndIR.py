from random import random
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

#Reference
#https://www.researchgate.net/figure/Touch-sensing-capacity-of-the-sensor-a-Change-in-capacitance-before-and-after-several_fig4_315906018
#https://www.researchgate.net/figure/Fig4Calibration-curve-of-IR-sensorOutput-voltage-calibration-a-Voltage-vs-distance_fig1_272355203

class PressureSensor:

    sensorType = "pressure"
    unit = "kPa"

    def __init__(self, averagePressure, minPressure, maxPressure,ID):
        self.averagePressure = averagePressure
        self.minPressure = minPressure
        self.maxPressure = maxPressure
        self.instanceID = ID

    def measure(self):
        values = np.linspace( self.minPressure,  self.maxPressure,50) # for frequency change number_of_samples (1000 here)
        return 250+ 250*signal.sawtooth(2 * np.pi * values)

    def getInstanceID(self):
        return self.instanceID


class IrSensor:
    sensorType = "IR"
    unit = "cm"

    def __init__(self, conveyorBeltWidth, ID):
        self.conveyorBeltWidth = conveyorBeltWidth
        self.instanceID = ID
        self.value = 0.0


    def measure(self):
        self.value = np.random.choice(np.linspace(self.conveyorBeltWidth, 0,10),1)
        return self.value

    def objectDetected(self):
        distance = self.measure()

        if(distance <= 0.75 * self.conveyorBeltWidth ):
            return True
        else : 
            return False

    def getInstanceID(self):
        return self.instanceID


class EsdProtectionSensor:
    sensorType = "Esd"

    def __init__(self, proximityMinValue, proximityMaxValue, tensionMinvalue, tensionMaxvalue, ID):
        self.proximityMinValue = proximityMinValue
        self.proximityMaxValue = proximityMaxValue
        self.tensionMinvalue = tensionMinvalue
        self.tensionMaxvalue = tensionMaxvalue
        self.proximityValue = 0.0
        self.tensionValue = 0.0
        self.instanceID = ID
        


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
            return True
        else:
            return False

    def getInstanceID(self):
        return self.instanceID
        

pressure = PressureSensor(25,1, 10,1)
plt.plot(pressure.measure())
#plt.plot( 250+ 250*signal.sawtooth(2 * np.pi * pressure.measure() ))
t  = np.linspace(0, 1, 1000)
values = pressure.measure()
print(np.shape(values))
plt.show()