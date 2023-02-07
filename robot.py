import numpy
import pyrosim.pyrosim as pyrosim
import pybullet as p
import constants as c
import os

from pyrosim.neuralNetwork import NEURAL_NETWORK
from sensor import SENSOR
from motor import MOTOR

class ROBOT:
    def __init__(self, solutionID):
        self.solutionID = solutionID
        self.robotId = p.loadURDF("body.urdf")
        pyrosim.Prepare_To_Simulate(self.robotId)
        self.nn = NEURAL_NETWORK(f'brain{self.solutionID}.nndf')
        self.Prepare_To_Sense()
        self.Prepare_To_Act()
        os.system(f'rm brain{self.solutionID}.nndf')

    
    def Prepare_To_Sense(self):
        self.sensors = {}
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)

    def Sense(self, step):
        for sensor in self.sensors:
            self.sensors[sensor].Get_Value(step)
            

    def Prepare_To_Act(self):
        self.motors = {}
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)

    def Act(self):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName) * c.motorJointRange
                self.motors[jointName.encode("utf-8")].Set_Value(desiredAngle, self.robotId)
                
    def Think(self):
        self.nn.Update()
        # self.nn.Print()

    def Get_Fitness(self):
        basePositionAndOrientation = p.getBasePositionAndOrientation(self.robotId)
        basePosition = basePositionAndOrientation[0]
        zPosition = basePosition[2]
        # f = open(f'tmp{self.solutionID}.txt', "w")
        # f.write(str(zPosition))


        relevantLinks = ['BackLowerleg', 'FrontLowerleg', 'LeftLowerleg', 'RightLowerleg']
        self.SensorValues = []
        for linkName in relevantLinks:
            self.SensorValues.append(numpy.mean(self.sensors[linkName].sensorValues))
        
        flattenedSensorValues = numpy.ravel(self.SensorValues, order='F')
        splitSensorValues = numpy.split(flattenedSensorValues, numpy.where(numpy.diff(flattenedSensorValues) != 0)[0]+1)
        maxLen = 0

        for i in range(len(splitSensorValues)):
            if splitSensorValues[i][0]== -1:
                maxLen = max(maxLen, len(splitSensorValues[i]))

        f = open(f'tmp{self.solutionID}.txt', "w")
        # Divide by 4 because each step is 4 values. This is because the sensor values are stored in a 2D array and then flattened
        # Multiply zposition by 60 to scale it to the same range as maxLen.
        # estimate but it seems to work
        f.write(str(maxLen//4+zPosition*60))
        f.close()
        os.system(f'mv tmp{self.solutionID}.txt fitness{self.solutionID}.txt')