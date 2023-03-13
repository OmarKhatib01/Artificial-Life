import numpy
import random

numLinks = 5 #random.randint(3, 9)
maxLinks = 8
linkShapes = ['cube']#, 'sphere', 'cylinder']
axes = ['x', 'y', 'z']
jointAxes = ['1 0 0', '0 1 0', '0 0 1', '1 1 0', '1 0 1', '0 1 1', '1 1 1']

initPosition = [0, 0, 5]
minSize, maxSize = 0.2, 1
length, width, height= random.uniform(minSize, maxSize), random.uniform(minSize, maxSize), random.uniform(minSize, maxSize)

steps = 2500

numberOfGenerations = 1 # should be 500
populationSize = 1 # should be 10


motorJointRange = 0.7