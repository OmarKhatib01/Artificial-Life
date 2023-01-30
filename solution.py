import random
import time
import numpy
import pyrosim.pyrosim as pyrosim
import os
import constants as c

class SOLUTION:
    def __init__(self, id):
        self.myID = id
        self.weights = numpy.random.rand(c.numSensorNeurons, c.numMotorNeurons) * 2 - 1

    def Set_ID(self, id):
        self.myID = id

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")

        pyrosim.Send_Cube(name='box', pos=[-3,3,.5] , size=[1,1,1])
        pyrosim.End()

    def Generate_Body(self):
        pyrosim.Start_URDF("body.urdf")
        # dimensions of the box
        length, width, height = 1, 1, 1
        pyrosim.Send_Cube(name='Torso', pos=[0,0,1] , size=[length,width,height])

        pyrosim.Send_Joint( name = "Torso_Backleg" , parent= "Torso" , child = "Backleg" , type = "revolute", position = [0,-0.5,1], jointAxis="1 0 0")
        pyrosim.Send_Cube(name='Backleg', pos=[0,-0.5,0] , size=[0.2,1,0.2])
        pyrosim.Send_Joint( name = "Backleg_BackLowerleg" , parent= "Backleg" , child = "BackLowerleg" , type = "revolute", position = [0,-1,0], jointAxis="1 0 0")
        pyrosim.Send_Cube(name='BackLowerleg', pos=[0,0,-0.5] , size=[0.2,0.2,1])
        
        pyrosim.Send_Joint( name = "Torso_Frontleg" , parent= "Torso" , child = "Frontleg" , type = "revolute", position = [0, 0.5, 1], jointAxis="1 0 0")
        pyrosim.Send_Cube(name='Frontleg', pos=[0,0.5,0] , size=[0.2,1,0.2])
        pyrosim.Send_Joint( name = "Frontleg_FrontLowerleg" , parent= "Frontleg" , child = "FrontLowerleg" , type = "revolute", position = [0,1,0], jointAxis="1 0 0")
        pyrosim.Send_Cube(name='FrontLowerleg', pos=[0,0,-0.5] , size=[0.2,0.2,1])

        pyrosim.Send_Joint( name = "Torso_Leftleg" , parent= "Torso" , child = "Leftleg" , type = "revolute", position = [-0.5, 0, 1], jointAxis="0 1 0")
        pyrosim.Send_Cube(name='Leftleg', pos=[-0.5,0,0] , size=[1,0.2,0.2])
        pyrosim.Send_Joint( name = "Leftleg_LeftLowerleg" , parent= "Leftleg" , child = "LeftLowerleg" , type = "revolute", position = [-1,0,0], jointAxis="0 1 0")
        pyrosim.Send_Cube(name='LeftLowerleg', pos=[0,0,-0.5] , size=[0.2,0.2,1])

        pyrosim.Send_Joint( name = "Torso_Rightleg" , parent= "Torso" , child = "Rightleg" , type = "revolute", position = [0.5, 0, 1], jointAxis="0 1 0")
        pyrosim.Send_Cube(name='Rightleg', pos=[0.5,0,0] , size=[1,0.2,0.2])
        pyrosim.Send_Joint( name = "Rightleg_RightLowerleg" , parent= "Rightleg" , child = "RightLowerleg" , type = "revolute", position = [1,0,0], jointAxis="0 1 0")
        pyrosim.Send_Cube(name='RightLowerleg', pos=[0,0,-0.5] , size=[0.2,0.2,1])

        pyrosim.End()

    def Generate_Brain(self):
        pyrosim.Start_NeuralNetwork(f'brain{self.myID}.nndf')

        # pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
        # pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "Backleg")
        # pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "Frontleg")  
        # pyrosim.Send_Sensor_Neuron(name = 3 , linkName = "Leftleg") 
        # pyrosim.Send_Sensor_Neuron(name = 4 , linkName = "Rightleg") 
        pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "BackLowerleg")
        pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "FrontLowerleg")  
        pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "LeftLowerleg") 
        pyrosim.Send_Sensor_Neuron(name = 3 , linkName = "RightLowerleg") 
        
        pyrosim.Send_Motor_Neuron(name = 4 , jointName = "Backleg_BackLowerleg")
        pyrosim.Send_Motor_Neuron(name = 5 , jointName = "Frontleg_FrontLowerleg")
        pyrosim.Send_Motor_Neuron(name = 6 , jointName = "Leftleg_LeftLowerleg")
        pyrosim.Send_Motor_Neuron(name = 7 , jointName = "Rightleg_RightLowerleg")

        for currentRow in range(c.numSensorNeurons):
            for currentColumn in range(c.numMotorNeurons):
                pyrosim.Send_Synapse(sourceNeuronName = currentRow, targetNeuronName = currentColumn+c.numSensorNeurons, weight = self.weights[currentRow, currentColumn])
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

    def Evaluate(self):
        pass 

    def Mutate(self):
        row = random.randint(0, c.numSensorNeurons-1)
        column = random.randint(0, c.numMotorNeurons-1)
        self.weights[row, column] = random.random() * 2 - 1