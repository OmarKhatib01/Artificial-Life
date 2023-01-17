from robot import ROBOT
from world import WORLD
import constants as c

import pybullet as p
import pybullet_data
import time




class SIMULATION:
    def __init__(self):
        self.physicsClient = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0,0,-9.8)

        self.world = WORLD()
        self.robot = ROBOT()

    def Run(self):
        for i in range(c.steps):
            # print(i)
            time.sleep(1/100)
            p.stepSimulation()
            self.robot.Sense(i)
            self.robot.Act(i)


    def __del__(self):
        p.disconnect()
        # MOTOR.Save_Values()
        # SENSOR.Save_Values()