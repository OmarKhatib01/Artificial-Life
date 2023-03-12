import numpy
import random

numLinks = random.randint(3, 6)
maxLinks = 8
linkShapes = ['cube']#, 'sphere', 'cylinder']
axes = ['x', 'y', 'z']
jointAxes = ['1 0 0', '0 1 0', '0 0 1']
initPosition = [0, 0, 5]
length, width, height =0.5, 0.5, 0.5
minSize, maxSize = 0.2, 1

steps = 2500

numberOfGenerations = 500 # should be 500
populationSize = 10 # should be 10


motorJointRange = 0.7