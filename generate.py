import math
import random
import pyrosim.pyrosim as pyrosim

# dimensions of the box
length, width, height = 1, 1, 1
# position of the box
x, y, z = 0, 0, 0.5

def Create_World():
    pyrosim.Start_SDF("world.sdf")

    pyrosim.Send_Cube(name='box', pos=[-3,3,z] , size=[length,width,height])
    pyrosim.End()

def Create_Robot():
    pass
    
def Generate_Body():
    pyrosim.Start_URDF("body.urdf")
    pyrosim.Send_Cube(name='Torso', pos=[1.5,0,1.5] , size=[length,width,height])
    pyrosim.Send_Joint( name = "Torso_Backleg" , parent= "Torso" , child = "Backleg" , type = "revolute", position = [1,0,1])
    pyrosim.Send_Cube(name='Backleg', pos=[-.5,0,-0.5] , size=[length,width,height])
    pyrosim.Send_Joint( name = "Torso_Frontleg" , parent= "Torso" , child = "Frontleg" , type = "revolute", position = [2, 0, 1])
    pyrosim.Send_Cube(name='Frontleg', pos=[0.5,0,-0.5] , size=[length,width,height])

    pyrosim.End()

def Generate_Brain():
    pyrosim.Start_NeuralNetwork("brain.nndf")

    for sensorNeuron in range(3):
        for motorNeuron in range(3,5):
            pyrosim.Send_Synapse( sourceNeuronName = sensorNeuron , targetNeuronName = motorNeuron , weight = math.tanh(random.random()))

    pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
    pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "Backleg")
    pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "Frontleg")    
    
    pyrosim.Send_Motor_Neuron(name = 3 , jointName = "Torso_Backleg")
    pyrosim.Send_Motor_Neuron(name = 4 , jointName = "Torso_Frontleg")

    # pyrosim.Send_Synapse( sourceNeuronName = 0 , targetNeuronName = 3 , weight = -1.0 )
    # pyrosim.Send_Synapse( sourceNeuronName = 1 , targetNeuronName = 3 , weight = -1.0 )
    # pyrosim.Send_Synapse( sourceNeuronName = 0 , targetNeuronName = 4 , weight = -3.0 )
    # pyrosim.Send_Synapse( sourceNeuronName = 2 , targetNeuronName = 4 , weight = -3.0 )



    pyrosim.End()


if __name__ == "__main__":
    Create_World()
    Create_Robot()
    Generate_Body()
    Generate_Brain()

# for i in range(5):
#     for j in range(5):
#         for k in range(10):
#             pyrosim.Send_Cube(name=f'Box{i+1}', pos=[x,y,z] , size=[length,width,height])
#             length, width, height = .9*length, .9*width, .9*height
#             z = z + 1
#         length, width, height = 1, 1, 1
#         x = x + 1
#         z = 0.5
#     y = y + 1
#     x = 0


    # for i in range(5):
    # pyrosim.Send_Cube(name=f'Box{i+1}', pos=[x,y,z] , size=[length,width,height])
    # z = z + 1
    # length, width, height = .9*length, .9*width, .9*height

