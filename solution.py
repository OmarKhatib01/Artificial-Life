import random
import time
import numpy
import pyrosim.pyrosim as pyrosim
import pybullet as p
import os
import constants as c
from collections import defaultdict
from link import LINK

class SOLUTION:
    def __init__(self, id, seed = None):
        self.seed = time.time() if seed == None else seed
        self.myID = id
        self.links = defaultdict(LINK)
        self.linksWithSensors = []
        self.hasSensor = [random.random() < 0.5 for i in range(c.numLinks)]
        self.numSensorNeurons = 0
        self.numMotorNeurons = 0
        self.Generate_Body()


    def init_weights(self):
        self.numSensorNeurons = len(self.linksWithSensors)
        self.numMotorNeurons = c.numLinks - 1
        self.weights = numpy.random.rand(self.numSensorNeurons, self.numMotorNeurons) * 2 - 1
    
    def Set_ID(self, id):
        self.myID = id
    
    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.End()

    def Generate_Brain(self):
        pyrosim.Start_NeuralNetwork(f'brain{self.myID}.nndf')

        for i in range(self.numSensorNeurons):
            pyrosim.Send_Sensor_Neuron(name = i , linkName = f"link{self.linksWithSensors[i]}")

        for i in range(c.numLinks, 2*c.numLinks):
            linkNumber = i - c.numLinks
            if linkNumber != c.numLinks-1:
                pyrosim.Send_Motor_Neuron(name = linkNumber + self.numSensorNeurons , jointName = f"link{linkNumber}_link{linkNumber+1}")

        for currentRow in range(self.numSensorNeurons):
            for currentColumn in range(self.numMotorNeurons):
                pyrosim.Send_Synapse(sourceNeuronName = currentRow , targetNeuronName = currentColumn + self.numSensorNeurons  , weight = self.weights[currentRow, currentColumn])
        pyrosim.End()

    def Start_Simulation(self, directOrGUI):
        self.Create_World()
        self.Generate_Brain()
        os.system("python3 simulate.py " + directOrGUI + " " + str(self.myID) + " 2&>1 &")

    def Generate_Body(self):
        pyrosim.Start_URDF("body.urdf")
        random.seed(self.seed)
        length, width, height = c.length, c.width, c.height
        position = c.initPosition
        axis = None
        prevAxis = None

        for i in range(c.numLinks):
            if i == c.numLinks-1 and len(self.linksWithSensors) == 0:
                self.hasSensor[i] = True
            if self.hasSensor[i]:
                self.linksWithSensors.append(i)
            self.links[i] = LINK(shape=random.choice(c.linkShapes),
            linkNumber=i ,
            hasSensor=self.hasSensor[i] ,
            position=position,
            length=length,
            width=width,
            height=height,
            prevAxis=prevAxis)

            self.links[i].Generate_Link()

            prevAxis = axis
            axis = random.choice(['x', 'y', 'z'])
            # dir = random.choice([-1, 1])

            self.links[i].Generate_Joints(axis)
        
            length=width=height=random.uniform(0.5, 1)
            match axis:
                case 'x':
                    position = [-length/2, 0, 0]
                case 'y':
                    position = [0, -width/2, 0]
                case 'z':
                    position = [0, 0, -height/2]
            
        pyrosim.End()
        self.init_weights()



    def Wait_For_Simulation_To_End(self):
        while not os.path.exists(f'fitness{str(self.myID)}.txt'):
            time.sleep(0.01)
            # print("waiting for fitness file to be created")
        f = open(f'fitness{str(self.myID)}.txt', "r")
        self.fitness = float(f.read())
        f.close()
        # print("fitness: ", self.fitness)
        os.system(f'rm fitness{str(self.myID)}.txt')

    
    def modifyBody(self):
        pyrosim.Start_URDF("body.urdf")
        for i in range(len(self.links)):
            self.links[i].Generate_Link()
            self.links[i].Generate_Joints(self.links[i].axis)

        pyrosim.End()

    def Mutate(self):
        choice = random.choice([0, 1])
        # mutate brain
        if choice == 0:
            row = random.randint(0, self.numSensorNeurons-1)
            column = random.randint(0, self.numMotorNeurons-1)
            self.weights[row, column] = random.random() * 2 - 1
        else:
            # mutate body
            linkNumber = random.randint(1, c.numLinks-1)
            self.links[linkNumber].Mutate()
            self.modifyBody()

    




