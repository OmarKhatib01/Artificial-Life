import numpy
import matplotlib.pyplot as plt

backLegSensorValues = numpy.load("data/backLegSensorValues.npy")
frontLegSensorValues = numpy.load("data/frontLegSensorValues.npy")
backLegMotorAngles = numpy.load("data/backLegMotorAngles.npy")
frontLegMotorAngles = numpy.load("data/frontLegMotorAngles.npy")
# targetAngles = numpy.load("data/targetAngles.npy")

plt.plot(backLegMotorAngles, label="Back Leg Motor", linewidth=3.5)
plt.plot(frontLegMotorAngles, label="Front Leg Motor")
plt.legend(["Back Leg Motor", "Front Leg Motor"])
plt.show()

plt.plot(backLegSensorValues, label="Back Leg", linewidth=3.5)
plt.plot(frontLegSensorValues, label="Front Leg")
plt.legend(["Back Leg", "Front Leg"])
plt.show()
