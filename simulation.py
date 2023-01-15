from robot import ROBOT
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
            print(i)
            time.sleep(1/500)
            p.stepSimulation()
            # backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("Backleg")
            # frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("Frontleg")
            # pyrosim.Set_Motor_For_Joint(
            #     bodyIndex = robotId,
            #     jointName = b'Torso_Backleg',
            #     controlMode = p.POSITION_CONTROL,
            #     targetPosition = backLegMotorAngles[i],
            #     maxForce = 50
            #     )

            # pyrosim.Set_Motor_For_Joint(
            #     bodyIndex = robotId,
            #     jointName = b'Torso_Frontleg',
            #     controlMode = p.POSITION_CONTROL,
            #     targetPosition = frontLegMotorAngles[i],
            #     maxForce = 50
            #     )



        