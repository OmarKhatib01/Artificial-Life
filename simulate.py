from simulation import SIMULATION
# import pybullet as p
# import pybullet_data
# import time
# import numpy
# import random
# import constants as c


# backLegSensorValues = numpy.zeros(1000)
# frontLegSensorValues = numpy.zeros(1000)
# # numpy.save("data/backLegSensorValues", backLegSensorValues)
# # numpy.save("data/frontLegSensorValues", frontLegSensorValues)


# backLegMotorAngles = numpy.sin(c.frequency_bl*numpy.linspace(0, 2*numpy.pi, 1000)+c.phaseOffset_bl)*c.amplitude_bl
# frontLegMotorAngles = numpy.sin(c.frequency_fl*numpy.linspace(0, 2*numpy.pi, 1000)+c.phaseOffset_fl)*c.amplitude_fl
# # numpy.save("data/backLegMotorAngles", backLegMotorAngles)
# # numpy.save("data/frontLegMotorAngles", frontLegMotorAngles)
# # exit()






# p.disconnect()

simulation = SIMULATION()
simulation.Run()