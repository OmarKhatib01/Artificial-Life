import random
import time
import numpy as np
import pyrosim.pyrosim as pyrosim
import pybullet as p
import os
import constants as c
from collections import defaultdict
from link import LINK

class SOLUTION:
    def __init__(self, id, seed = None, mode='train', phc_run=0):
        self.mode = mode
        self.phc_run = phc_run
        self.seed = time.time() if seed == None else seed
        random.seed(self.seed)
        self.myID = id

        self.numLinks = c.numLinks
        self.links = defaultdict(LINK)
        self.linksWithSensors = []
        self.hasSensor = [random.random() < 0.5 for i in range(self.numLinks)]

        self.numSensorNeurons = 0
        self.numMotorNeurons = 0
        self.Generate_Body()


    def init_weights(self):
        self.numSensorNeurons = len(self.linksWithSensors)
        self.numMotorNeurons = self.numLinks - 1
        self.weights = np.random.rand(self.numSensorNeurons, self.numMotorNeurons) * 2 - 1
    
    def Set_ID(self, id):
        self.myID = id
    
    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.End()

    def Generate_Brain(self):
        random.seed(self.seed)
        pyrosim.Start_NeuralNetwork(f'{self.phc_run}brain{self.myID}.nndf')

        for i in range(self.numSensorNeurons):
            pyrosim.Send_Sensor_Neuron(name = i , linkName = f"link{self.linksWithSensors[i]}")

        for i in range(self.numLinks, 2*self.numLinks):
            linkNumber = i - self.numLinks
            if linkNumber != self.numLinks-1:
                pyrosim.Send_Motor_Neuron(name = linkNumber + self.numSensorNeurons , jointName = f"link{linkNumber}_link{linkNumber+1}")

        for currentRow in range(self.numSensorNeurons):
            for currentColumn in range(self.numMotorNeurons):
                pyrosim.Send_Synapse(sourceNeuronName = currentRow , targetNeuronName = currentColumn + self.numSensorNeurons  , weight = self.weights[currentRow, currentColumn])
        pyrosim.End()

    def Generate_Body(self):
        pyrosim.Start_URDF(f'save/{self.phc_run}body.urdf')
        random.seed(self.seed)
        length, width, height = c.length, c.width, c.height
        position = c.initPosition
        axis = None
        prevAxis = None
        jointAxis = random.choice(c.jointAxes)

        for i in range(self.numLinks):
            if i == self.numLinks-1 and len(self.linksWithSensors) == 0:
                self.hasSensor[i] = True
            if self.hasSensor[i]:
                self.linksWithSensors.append(i)

            prevAxis = axis

            self.links[i] = LINK(numLinks=self.numLinks, shape=random.choice(c.linkShapes),
            linkNumber=i ,
            hasSensor=self.hasSensor[i] ,
            position=position,
            jointAxis=jointAxis,
            length=length,
            width=width,
            height=height,
            prevAxis=prevAxis)

            self.links[i].Generate_Link()

            axis = random.choice(c.axes)

            self.links[i].Generate_Joints(axis)
        
            length, width, height= random.uniform(c.minSize, c.maxSize), random.uniform(c.minSize, c.maxSize), random.uniform(c.minSize, c.maxSize)
            position = self.update_position(axis, length, width, height)
            
        pyrosim.End()
        self.init_weights()

    def update_position(self, axis, length, width, height):
        match axis:
            case 'x':
                position = [length/2, 0, 0]
            case 'y':
                position = [0, width/2, 0]
            case 'z':
                position = [0, 0, height/2]
        return position

    def modifyBody(self):
        pyrosim.Start_URDF(f'save/{self.phc_run}body.urdf')
        for i in range(self.numLinks):
            self.links[i].Generate_Link()
            self.links[i].Generate_Joints(self.links[i].axis)

        pyrosim.End()

    def Mutate(self):
        random.seed()
        choice = random.choice([0, 1])
        # mutate brain
        if choice == 0:
            weightsToMutate = random.randint(1, (self.numSensorNeurons * self.numMotorNeurons)//2)
            for i in range(weightsToMutate):
                row = random.randint(0, self.numSensorNeurons-1)
                column = random.randint(0, self.numMotorNeurons-1)
                self.weights[row, column] = random.random() * 2 - 1
        else:
            # mutate body
            linkNumber = random.randint(1, self.numLinks-1)
            choice = random.randint(1,6)
            if choice == 0: # change link shape
                self.links[linkNumber].shape = random.choice(c.linkShapes)
            elif choice == 1: # change link length
                self.links[linkNumber].length = random.uniform(c.minSize, c.maxSize)
            elif choice == 2: # change link width
                self.links[linkNumber].width = random.uniform(c.minSize, c.maxSize)
            elif choice == 3: # change link height
                self.links[linkNumber].height = random.uniform(c.minSize, c.maxSize)  
            elif choice == 4: # change joint axis
                self.links[linkNumber].joinAxis = random.choice(c.jointAxes)   
            elif choice == 5: # add/remove sensor
                self.links[linkNumber].hasSensor = random.random() < 0.5
                if self.links[linkNumber].hasSensor and linkNumber not in self.linksWithSensors:
                    self.linksWithSensors.append(linkNumber)
                    # add row to weights
                    self.weights = np.vstack((self.weights, np.random.rand(1, self.numMotorNeurons)*2-1))

                elif not self.links[linkNumber].hasSensor and linkNumber in self.linksWithSensors:
                    self.linksWithSensors.remove(linkNumber)
                    # remove row from weights
                    self.weights = np.delete(self.weights, self.numSensorNeurons-1, 0)   
            elif choice == 6: # change link axis
                self.links[linkNumber].axis = random.choice(c.axes)
                if linkNumber != self.numLinks-1:
                    self.links[linkNumber+1].prevAxis = self.links[linkNumber].axis                    
            else:
                return 'Invalid choice'
            
            self.numSensorNeurons = len(self.linksWithSensors)
            self.numMotorNeurons = self.numLinks - 1
            self.modifyBody()

    def Start_Simulation(self, directOrGUI):
        self.Create_World()
        self.Generate_Brain()

        if directOrGUI == "GUI": # only in beginning and showing best
            # save the brain file as bestBrain.nndf
            os.system(f'cp {self.phc_run}brain{self.myID}.nndf save/{self.phc_run}bestBrain.nndf')

        os.system(f"python3 simulate.py {directOrGUI}  {str(self.myID)} {self.mode} {self.phc_run} 2&>1 &")

    def Wait_For_Simulation_To_End(self):
        while not os.path.exists(f'fitness{str(self.myID)}.txt'):
            time.sleep(0.01)
        f = open(f'fitness{str(self.myID)}.txt', "r")
        self.fitness = float(f.read())
        f.close()
        os.system(f'rm fitness{str(self.myID)}.txt')


            