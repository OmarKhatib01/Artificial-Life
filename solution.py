import random
import time
import numpy
import pyrosim.pyrosim as pyrosim
import os
import constants as c

class SOLUTION:
    def __init__(self, id):
        self.myID = id
        # self.weights = numpy.random.rand(c.numSensorNeurons, c.numMotorNeurons) * 2 - 1

    def Set_ID(self, id):
        self.myID = id

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.End()

    def Generate_Link(self, shape, linkNumber, position, length, width, height):
        x, y, z = position
        if linkNumber != c.numLinks - 1:
            pyrosim.Send_Joint( name = f'link{linkNumber}_link{linkNumber+1}' , parent= f'link{linkNumber}' , child = f'link{linkNumber+1}' , type = "revolute", position = [-length, 0, 0], jointAxis="0 0 1")
        if shape == 'cube':
            pyrosim.Send_Cube(name=f'link{linkNumber}', pos=[x,y,z] , size=[length,width,height])
        elif shape == 'cylinder':
            pyrosim.Send_Cylinder(name=f'link{linkNumber}', pos=[x,y,z] , length=length, radius=width)
        elif shape == 'sphere':
            pyrosim.Send_Sphere(name=f'link{linkNumber}', pos=[x,y,z] , radius=length)
        else:
            return 'Invalid shape'


    def Generate_Body(self):
        pyrosim.Start_URDF("body.urdf")
        
        pyrosim.Send_Cube(name='Head', pos=c.initPosition , size=[c.length,c.width,c.height])
        # pyrosim.Send_Sphere(name='Head', pos=c.initPosition , radius=c.length)
        pyrosim.Send_Joint( name = 'Head_link0' , parent= 'Head' , child = 'link0' , type = "revolute", position = [-2, 0, 1], jointAxis="0 0 1")
        position = c.initPosition
        length, width, height = c.length, c.width, c.height
        for i in range(c.numLinks):
            length, width, height = random.uniform(1, 2), random.uniform(1, 2), random.uniform(1, 2)
            position = [-length/2, 0, 0]
            self.Generate_Link(random.choice(c.linkShapes), 
                            i, position,
                            length= length,
                            width= width,
                            height= height)
        pyrosim.End()


    def Generate_Brain(self):
        pyrosim.Start_NeuralNetwork(f'brain{self.myID}.nndf')

        pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Head")
        for i in range(1, c.numLinks):
            if random.choice([True, False]):
                pyrosim.Send_Sensor_Neuron(name = i , linkName = f"link{i}")
                pyrosim.Send_Synapse(sourceNeuronName = i , targetNeuronName = c.numLinks + i , weight = random.random() * 2 - 1)
        
        pyrosim.Send_Motor_Neuron(name = c.numLinks , jointName = "Head_link0")
        for i in range(c.numLinks+1, 2*c.numLinks):
            linkNumber = i - c.numLinks
            pyrosim.Send_Motor_Neuron(name = i , jointName = f"link{linkNumber-1}_link{linkNumber}")


        pyrosim.End()
    

    def Start_Simulation(self, directOrGUI):
        self.Create_World()
        self.Generate_Body()
        self.Generate_Brain()
        os.system("python3 simulate.py " + directOrGUI + " " + str(self.myID) + " 2&>1 &")


    def Wait_For_Simulation_To_End(self):
        while not os.path.exists(f'fitness{str(self.myID)}.txt'):
            time.sleep(0.01)
        f = open(f'fitness{str(self.myID)}.txt', "r")
        self.fitness = float(f.read())
        f.close()
        # print("fitness: ", self.fitness)
        os.system(f'rm fitness{str(self.myID)}.txt')


    def Mutate(self):
        row = random.randint(0, c.numSensorNeurons-1)
        column = random.randint(0, c.numMotorNeurons-1)
        self.weights[row, column] = random.random() * 2 - 1