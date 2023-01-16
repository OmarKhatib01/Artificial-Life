from motor import MOTOR
from robot import ROBOT
from sensor import SENSOR
from world import WORLD

import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import time
import numpy
import random
import constants as c



class SIMULATION:
    def __init__(self):
        self.physicsClient = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0,0,-9.8)

        self.world = WORLD()
        self.robot = ROBOT()

    def Run(self):
        for i in range(1000):
            # print(i)
            time.sleep(1/1000)
            p.stepSimulation()
            self.robot.Sense(i)
            self.robot.Act(i)


    def __del__(self):
        p.disconnect()
        MOTOR.Save_Values()
        SENSOR.Save_Values()