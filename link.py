# make a link class

import pyrosim.pyrosim as pyrosim
import random
import constants as c
import numpy

class LINK:
    def __init__(self, shape, linkNumber, hasSensor, position, jointAxis, length, width, height, prevAxis=None):
        self.shape = shape
        self.linkNumber = linkNumber
        self.hasSensor = hasSensor
        self.position = position
        self.length = length
        self.width = width
        self.height = height
        self.prevAxis = prevAxis
        self.jointAxis = jointAxis
    
    def Generate_Link(self):

        if self.shape == 'cube':
            pyrosim.Send_Cube(name=f'link{self.linkNumber}', pos=self.position , size=[self.length,self.width,self.height], hasSensor=self.hasSensor)
        elif self.shape == 'cylinder':
            pyrosim.Send_Cylinder(name=f'link{self.linkNumber}', pos=self.position , length=self.length, radius=self.width/2, hasSensor=self.hasSensor)
        elif self.shape == 'sphere':
            pyrosim.Send_Sphere(name=f'link{self.linkNumber}', pos=self.position , radius=self.width/2, hasSensor=self.hasSensor)
        else:
            return 'Invalid shape'

    def hasSensor(self):
        return self.hasSensor

    def Generate_Joints(self, axis):
        self.axis = axis
        match self.axis:
            case 'x':
                if self.linkNumber == 0 :
                    pyrosim.Send_Joint( name = f'link{self.linkNumber}_link{self.linkNumber+1}' , parent= f'link{self.linkNumber}' , child = f'link{self.linkNumber+1}' , type = "revolute", position = [c.length/2, 0, self.position[2]], jointAxis=self.jointAxis)
                elif self.linkNumber != c.numLinks-1:
                    if self.prevAxis == 'y':
                        pyrosim.Send_Joint( name = f'link{self.linkNumber}_link{self.linkNumber+1}' , parent= f'link{self.linkNumber}' , child = f'link{self.linkNumber+1}' , type = "revolute", position = [self.length/2, self.width/2, 0], jointAxis=self.jointAxis)
                    elif self.prevAxis == 'z':
                        pyrosim.Send_Joint( name = f'link{self.linkNumber}_link{self.linkNumber+1}' , parent= f'link{self.linkNumber}' , child = f'link{self.linkNumber+1}' , type = "revolute", position = [self.length/2, 0, self.height/2], jointAxis=self.jointAxis)
                    else:
                        pyrosim.Send_Joint( name = f'link{self.linkNumber}_link{self.linkNumber+1}' , parent= f'link{self.linkNumber}' , child = f'link{self.linkNumber+1}' , type = "revolute", position = [self.length, 0, 0], jointAxis=self.jointAxis)
                else:
                    return
            case 'y':
                if self.linkNumber == 0 and self.prevAxis == None:
                    pyrosim.Send_Joint( name = f'link{self.linkNumber}_link{self.linkNumber+1}' , parent= f'link{self.linkNumber}' , child = f'link{self.linkNumber+1}' , type = "revolute", position = [0, c.width/2, self.position[2]], jointAxis=self.jointAxis)
                elif self.linkNumber != c.numLinks-1:
                    if self.prevAxis == 'x':
                        pyrosim.Send_Joint( name = f'link{self.linkNumber}_link{self.linkNumber+1}' , parent= f'link{self.linkNumber}' , child = f'link{self.linkNumber+1}' , type = "revolute", position = [self.length/2, self.width/2, 0], jointAxis=self.jointAxis)
                    elif self.prevAxis == 'z':
                        pyrosim.Send_Joint( name = f'link{self.linkNumber}_link{self.linkNumber+1}' , parent= f'link{self.linkNumber}' , child = f'link{self.linkNumber+1}' , type = "revolute", position = [0, self.width/2, self.height/2], jointAxis=self.jointAxis)
                    else:
                        pyrosim.Send_Joint( name = f'link{self.linkNumber}_link{self.linkNumber+1}' , parent= f'link{self.linkNumber}' , child = f'link{self.linkNumber+1}' , type = "revolute", position = [0, self.width, 0], jointAxis=self.jointAxis)
                else:
                    return
            case 'z':
                if self.linkNumber == 0 and self.prevAxis == None:
                    pyrosim.Send_Joint( name = f'link{self.linkNumber}_link{self.linkNumber+1}' , parent= f'link{self.linkNumber}' , child = f'link{self.linkNumber+1}' , type = "revolute", position = [0, 0, c.initPosition[2]+c.length/2], jointAxis=self.jointAxis)
                elif self.linkNumber != c.numLinks-1:
                    if self.prevAxis == 'x':
                        pyrosim.Send_Joint( name = f'link{self.linkNumber}_link{self.linkNumber+1}' , parent= f'link{self.linkNumber}' , child = f'link{self.linkNumber+1}' , type = "revolute", position = [self.length/2, 0, self.height/2], jointAxis=self.jointAxis)
                    elif self.prevAxis == 'y':
                        pyrosim.Send_Joint( name = f'link{self.linkNumber}_link{self.linkNumber+1}' , parent= f'link{self.linkNumber}' , child = f'link{self.linkNumber+1}' , type = "revolute", position = [0,self.width/2, self.height/2], jointAxis=self.jointAxis)
                    else:
                        pyrosim.Send_Joint( name = f'link{self.linkNumber}_link{self.linkNumber+1}' , parent= f'link{self.linkNumber}' , child = f'link{self.linkNumber+1}' , type = "revolute", position = [0, 0, self.height], jointAxis=self.jointAxis)
                else:
                    return


    def Mutate(self):
        # choose one property to mutate
        # mutate that property
        # print(f'Link {self.linkNumber}: {self.shape}, {self.length}, {self.width}, {self.height}')

        choice = random.randint(0, 4)
        if choice == 0:
            self.shape = random.choice(c.linkShapes)
        elif choice == 1:
            self.length = random.uniform(c.minSize, c.maxSize)
        elif choice == 2:
            self.width = random.uniform(c.minSize, c.maxSize)
        elif choice == 3:
            self.height = random.uniform(c.minSize, c.maxSize)  
        elif choice == 4:
            self.joinAxis = random.choice(c.jointAxes)    
        else:
            return 'Invalid choice'
        # print(f'Link {self.linkNumber} mutated: {self.shape}, {self.length}, {self.width}, {self.height}')
