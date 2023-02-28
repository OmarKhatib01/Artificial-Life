import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

# get the fitness data from the fitness files
fitnessData = []
for i in range(5):
    fitnessData.append(pd.read_csv(f'minfitnessList{i}.csv', header=None)[1])

# plot 5 curves for each of the files read
for i in range(5):
    plt.plot(fitnessData[i], label=f'run {i}')

# add labels and legend
plt.title('Fitness over Generations for 5 Runs | Objective: Minimize x position')
plt.xlabel('Generation')
plt.ylabel('Fitness')
plt.legend()

# save the plot
plt.savefig('fitness.png')

# show the plot
plt.show()