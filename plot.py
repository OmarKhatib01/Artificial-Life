import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

# get the fitness data from the fitness files
fitnessData = []
for i in range(10):
    fitnessData.append(pd.read_csv(f'save/minfitnessList{i}.csv', header=None)[1])

# plot 5 curves for each of the files read
for i in range(10):
    plt.plot(fitnessData[i], label=f'run {i}')

# add labels and legend
plt.title('Fitness over Generations for 10 PHC Runs | Objective: Minimize x position')
plt.xlabel('Generation')
plt.ylabel('Fitness')
plt.legend()

# save the plot
plt.savefig('save/fitness.png')

# show the plot
plt.show()