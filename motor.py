import numpy
import constants as c
import pyrosim.pyrosim as pyrosim
import pybullet as p

class MOTOR:
    def __init__(self, jointName):
        self.jointName = jointName
        self.Prepare_To_Act()

    def Prepare_To_Act(self):
        self.amplitude = c.amplitude
        self.frequency = c.frequency
        self.phaseOffset = c.phaseOffset
        self.motorValues = numpy.sin(self.frequency*numpy.linspace(0, 2*numpy.pi, 1000)+self.phaseOffset)*self.amplitude

    def Set_Value(self, step, robotId):
        pyrosim.Set_Motor_For_Joint(
            bodyIndex = robotId,
            jointName = self.jointName,
            controlMode = p.POSITION_CONTROL,
            targetPosition = self.motorValues[step],
            maxForce = 50
            )
    
    def Save_Values(self):
        numpy.save("data/motorValues", self.motorValues)