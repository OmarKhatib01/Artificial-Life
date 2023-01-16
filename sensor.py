import numpy
import pyrosim.pyrosim as pyrosim

class SENSOR:
    def __init__(self, linkName):
        self.linkName = linkName
        self.sensorValues = numpy.zeros(1000)

    def Get_Value(self, step):
        self.sensorValues[step] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)
        print(self.sensorValues) if step == 999 else None

    def Save_Values(self):
        numpy.save("data/sensorValues", self.sensorValues)