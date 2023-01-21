import numpy
import pyrosim.pyrosim as pyrosim
import constants as c

class SENSOR:
    def __init__(self, linkName):
        self.linkName = linkName
        self.sensorValues = numpy.zeros(c.steps)

    def Get_Value(self, step):
        self.sensorValues[step] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)

    def Save_Values(self):
        numpy.save("data/sensorValues", self.sensorValues)