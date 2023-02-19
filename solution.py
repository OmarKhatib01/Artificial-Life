import random
import time
import numpy
import pyrosim.pyrosim as pyrosim
import os
import constants as c

class SOLUTION:
    def __init__(self, id):
        self.myID = id
        self.linksWithSensors = []
        self.numSensorNeurons = 0
        self.numMotorNeurons = 0

    def init_weights(self):
        self.numSensorNeurons = len(self.linksWithSensors)
        self.numMotorNeurons = c.numLinks - 1
        self.weights = numpy.random.rand(self.numSensorNeurons, self.numMotorNeurons) * 2 - 1
    
    def Set_ID(self, id):
        self.myID = id
    
    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.End()

    def Generate_Body(self):
        pyrosim.Start_URDF("body.urdf")
        length, width, height = c.length, c.width, c.height
        position = c.initPosition
        axis = None
        for i in range(c.numLinks):
            self.Generate_Link(random.choice(c.linkShapes), 
                            i, random.choice([True, True, False]),
                            position= position,
                            length= length,
                            width= width,
                            height= height)

            prevAxis = axis
            axis = random.choice(['x', 'y', 'z'])
            # dir = random.choice([-1, 1])

            self.Generate_Joints(axis, prevAxis, i, length, width, height, position)
            
            length=width=height = random.uniform(0.5, 1)
            match axis:
                case 'x':
                    position = [-length/2, 0, 0]
                case 'y':
                    position = [0, -width/2, 0]
                case 'z':
                    position = [0, 0, -height/2]
            
        pyrosim.End()
        self.init_weights()

    def Generate_Link(self, shape, linkNumber, hasSensor, position, length, width, height):
        if hasSensor:
            self.linksWithSensors.append(linkNumber)

        if shape == 'cube':
            pyrosim.Send_Cube(name=f'link{linkNumber}', pos=position , size=[length,width,height], hasSensor=hasSensor)
        elif shape == 'cylinder':
            pyrosim.Send_Cylinder(name=f'link{linkNumber}', pos=position , length=length, radius=width/2, hasSensor=hasSensor)
        elif shape == 'sphere':
            pyrosim.Send_Sphere(name=f'link{linkNumber}', pos=position , radius=width/2, hasSensor=hasSensor)
        else:
            return 'Invalid shape'

    def Generate_Joints(self, axis, prevAxis, linkNumber, length, width, height, position):
        print(axis, linkNumber, position, length, width, height)
        match axis:
            case 'x':
                if linkNumber == 0 or prevAxis == None:
                    pyrosim.Send_Joint( name = f'link{linkNumber}_link{linkNumber+1}' , parent= f'link{linkNumber}' , child = f'link{linkNumber+1}' , type = "revolute", position = [-c.length/2, 0, position[2]], jointAxis="1 0 0")
                elif linkNumber != c.numLinks-1:
                    if prevAxis == 'y':
                        pyrosim.Send_Joint( name = f'link{linkNumber}_link{linkNumber+1}' , parent= f'link{linkNumber}' , child = f'link{linkNumber+1}' , type = "revolute", position = [-length/2, -width/2, 0], jointAxis="1 0 0")
                    elif prevAxis == 'z':
                        pyrosim.Send_Joint( name = f'link{linkNumber}_link{linkNumber+1}' , parent= f'link{linkNumber}' , child = f'link{linkNumber+1}' , type = "revolute", position = [-length/2, 0, -height/2], jointAxis="1 0 0")
                    else:
                        pyrosim.Send_Joint( name = f'link{linkNumber}_link{linkNumber+1}' , parent= f'link{linkNumber}' , child = f'link{linkNumber+1}' , type = "revolute", position = [-length, 0, 0], jointAxis="1 0 0")
                else:
                    return
            case 'y':
                if linkNumber == 0:
                    pyrosim.Send_Joint( name = f'link{linkNumber}_link{linkNumber+1}' , parent= f'link{linkNumber}' , child = f'link{linkNumber+1}' , type = "revolute", position = [0, -c.length/2, position[2]], jointAxis="0 1 0")
                elif linkNumber != c.numLinks-1:
                    if prevAxis == 'x':
                        pyrosim.Send_Joint( name = f'link{linkNumber}_link{linkNumber+1}' , parent= f'link{linkNumber}' , child = f'link{linkNumber+1}' , type = "revolute", position = [-length/2, -width/2, 0], jointAxis="0 1 0")
                    elif prevAxis == 'z':
                        pyrosim.Send_Joint( name = f'link{linkNumber}_link{linkNumber+1}' , parent= f'link{linkNumber}' , child = f'link{linkNumber+1}' , type = "revolute", position = [0, -length/2, -height/2], jointAxis="0 1 0")
                    else:                    
                        pyrosim.Send_Joint( name = f'link{linkNumber}_link{linkNumber+1}' , parent= f'link{linkNumber}' , child = f'link{linkNumber+1}' , type = "revolute", position = [0, -length, 0], jointAxis="0 1 0")
                else:
                    return
            case 'z':
                if linkNumber == 0:
                    pyrosim.Send_Joint( name = f'link{linkNumber}_link{linkNumber+1}' , parent= f'link{linkNumber}' , child = f'link{linkNumber+1}' , type = "revolute", position = [0, 0, position[2]-c.length/2], jointAxis="0 0 1") # rotate around x/z plane 010
                elif linkNumber != c.numLinks-1:
                    if prevAxis == 'x':
                        pyrosim.Send_Joint( name = f'link{linkNumber}_link{linkNumber+1}' , parent= f'link{linkNumber}' , child = f'link{linkNumber+1}' , type = "revolute", position = [-length/2, 0, -height/2], jointAxis="0 0 1")
                    elif prevAxis == 'y':
                        pyrosim.Send_Joint( name = f'link{linkNumber}_link{linkNumber+1}' , parent= f'link{linkNumber}' , child = f'link{linkNumber+1}' , type = "revolute", position = [0, -width/2, -height/2], jointAxis="0 0 1")
                    else:
                        pyrosim.Send_Joint( name = f'link{linkNumber}_link{linkNumber+1}' , parent= f'link{linkNumber}' , child = f'link{linkNumber+1}' , type = "revolute", position = [0, 0, -height], jointAxis="0 0 1")
                else:
                    return

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