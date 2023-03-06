import numpy

numLinks = 5
linkShapes = ['cube']#, 'sphere', 'cylinder']
axes = ['x', 'y', 'z']
jointAxes = ['1 0 0', '0 1 0', '0 0 1']
initPosition = [0, 0, 5]
length, width, height =1, 1, 1
minSize, maxSize = 0.5, 1

steps = 2500

numberOfGenerations = 10
populationSize =10



motorJointRange = 1