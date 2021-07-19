from PressureAndIR import *


class EsdActuator:

    def EsdFeedback(self):
        esd = EsdProtectionSensor(1000,10000, 1000, 10000, 123)
        if(esd.EsdCheckPass()):
            print("Esd Check Passed")
        else:
            print("Esd Check Failed, TAKE ESD PRECAUTIONS")


class 

test = EsdActuator()
test.EsdFeedback()