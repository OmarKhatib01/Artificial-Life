from motor import MOTOR
from robot import ROBOT
from sensor import SENSOR
from world import WORLD
import constants as c

import pybullet as p
import pybullet_data
import time

class SIMULATION:
    def __init__(self, directOrGUI, solutionID):
        self.directOrGUI = directOrGUI
        self.physicsClient = p.connect(p.GUI) if directOrGUI == "GUI" else p.connect(p.DIRECT)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0,0,-9.8)
        self.world = WORLD()
        self.robot = ROBOT(solutionID)

    def Run(self):
        for i in range(c.steps):
            # print(i)
            # if self.directOrGUI == "GUI":
            #     time.sleep(1/1000)
            p.stepSimulation()
            self.robot.Sense(i)
            self.robot.Think()
            self.robot.Act()
            # print(self.robot.sensorValues)

    def Get_Fitness(self):
        self.robot.Get_Fitness()

    def __del__(self):
        p.disconnect()
        # MOTOR.Save_Values()
        # SENSOR.Save_Values()