import pyrosim.pyrosim as pyrosim

pyrosim.Start_SDF("boxes.sdf")

# dimensions of the box
length = 1
width = 1
height = 1

# position of the box
x = 0
y = 0
z = 0.5

for i in range(5):
    for j in range(5):
        for k in range(10):
            pyrosim.Send_Cube(name=f'Box{i+1}', pos=[x,y,z] , size=[length,width,height])
            length, width, height = .9*length, .9*width, .9*height
            z = z + 1
        length, width, height = 1, 1, 1
        x = x + 1
        z = 0.5
    y = y + 1
    x = 0


    # for i in range(5):
    # pyrosim.Send_Cube(name=f'Box{i+1}', pos=[x,y,z] , size=[length,width,height])
    # z = z + 1
    # length, width, height = .9*length, .9*width, .9*height


pyrosim.End()