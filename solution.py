import random
import time
import numpy
import pyrosim.pyrosim as pyrosim
import os

class SOLUTION:
    def __init__(self, id):
        self.myID = id
        self.weights = numpy.random.rand(3, 2) * 2 - 1

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

        pyrosim.Send_Cube(name='Torso', pos=[1.5,0,1.5] , size=[length,width,height])
        pyrosim.Send_Joint( name = "Torso_Backleg" , parent= "Torso" , child = "Backleg" , type = "revolute", position = [1,0,1])
        pyrosim.Send_Cube(name='Backleg', pos=[-.5,0,-0.5] , size=[length,width,height])
        pyrosim.Send_Joint( name = "Torso_Frontleg" , parent= "Torso" , child = "Frontleg" , type = "revolute", position = [2, 0, 1])
        pyrosim.Send_Cube(name='Frontleg', pos=[0.5,0,-0.5] , size=[length,width,height])

        pyrosim.End()

    def Generate_Brain(self):
        pyrosim.Start_NeuralNetwork(f'brain{self.myID}.nndf')

        pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
        pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "Backleg")
        pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "Frontleg")    
        
        pyrosim.Send_Motor_Neuron(name = 3 , jointName = "Torso_Backleg")
        pyrosim.Send_Motor_Neuron(name = 4 , jointName = "Torso_Frontleg")

        for currentRow in range(3):
            for currentColumn in range(2):
                pyrosim.Send_Synapse(sourceNeuronName = currentRow, targetNeuronName = currentColumn+3, weight = self.weights[currentRow, currentColumn])

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
        row = random.randint(0, 2)
        column = random.randint(0, 1)
        self.weights[row, column] = random.random() * 2 - 1