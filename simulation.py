import pybullet as p
import pybullet_data
import time
import pyrosim.pyrosim as pyrosim
import numpy
import random

amplitude_bl, frequency_bl, phaseOffset_bl = numpy.pi/4, 8, numpy.pi/8
amplitude_fl, frequency_fl, phaseOffset_fl = numpy.pi/4, 10, 0

backLegSensorValues = numpy.zeros(1000)
frontLegSensorValues = numpy.zeros(1000)

backLegMotorAngles = numpy.sin(frequency_bl*numpy.linspace(0, 2*numpy.pi, 1000)+phaseOffset_bl)*amplitude_bl
frontLegMotorAngles = numpy.sin(frequency_fl*numpy.linspace(0, 2*numpy.pi, 1000)+phaseOffset_fl)*amplitude_fl

# numpy.save("data/backLegMotorAngles", backLegMotorAngles)
# numpy.save("data/frontLegMotorAngles", frontLegMotorAngles)
# exit()


physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

p.setGravity(0,0,-9.8)
planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")

p.loadSDF("world.sdf")
pyrosim.Prepare_To_Simulate(robotId)


for i in range(1000):
    time.sleep(1/500)
    p.stepSimulation()
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("Backleg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("Frontleg")
    pyrosim.Set_Motor_For_Joint(
        bodyIndex = robotId,
        jointName = b'Torso_Backleg',
        controlMode = p.POSITION_CONTROL,
        targetPosition = backLegMotorAngles[i],
        maxForce = 50
        )

    pyrosim.Set_Motor_For_Joint(
        bodyIndex = robotId,
        jointName = b'Torso_Frontleg',
        controlMode = p.POSITION_CONTROL,
        targetPosition = frontLegMotorAngles[i],
        maxForce = 50
        )

numpy.save("data/backLegSensorValues", backLegSensorValues)
numpy.save("data/frontLegSensorValues", frontLegSensorValues)
p.disconnect()