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
    pyrosim.Start_URDF("body.urdf")
    pyrosim.Send_Cube(name='torso', pos=[x,y,z] , size=[length,width,height])
    pyrosim.Send_Joint( name = "Torso_Leg" , parent= "torso" , child = "leg" , type = "revolute", position = [0.5,0,1])
    pyrosim.Send_Cube(name='leg', pos=[1,0,1.5] , size=[length,width,height])

    pyrosim.End()
    
if __name__ == "__main__":
    Create_World()
    Create_Robot()

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

