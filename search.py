from parallelHillClimber import PARALLEL_HILL_CLIMBER
import os
import re
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-type', type=str, help='evolve or show', default='evolve')
args = parser.parse_args()

if args.type == 'evolve':
    ### uncomment to run parallel hill climber (evolve)
    # ----------------------------
    # run parallel hill climber
    phc = PARALLEL_HILL_CLIMBER()
    phc.Evolve()
    id = phc.Show_Best()
    phc.Save_Best_Brain(id)

    # save fitness data for plotting
    np.savetxt('fitnessMat.txt', phc.fitnessMat)
    # ----------------------------

else:

    ### uncomment to run best brain
    # ----------------------------
    regex = re.compile(r'\d+') # regex to find numbers in string

    # get best brain id from file name
    for file in os.listdir('./'):
        if file.startswith("brain"):
            bestId = regex.findall(file)[0]

    # run best brain simulation
    os.system(f'python3 simulate.py GUI {bestId} test 2&>1 &')
    # ----------------------------


