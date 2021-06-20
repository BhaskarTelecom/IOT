from random import random
import numpy as np

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
        self.value = 0.0

    def measure(self,minPressure,maxPressure):
        self.value = np.random.choice(np.linspace(minPressure, maxPressure,10),1)
        return self.value

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
        self.value = np.random.choice(np.linspace(conveyorBeltWidth, 0,10),1)
        return self.value

    def objectDetected(self):
        distance = self.measure()

        if(distance <= 0.75 * conveyorBeltWidth ):
            return True
        else : 
            return False

    def getInstanceID(self):
        return self.instanceID