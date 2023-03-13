from parallelHillClimber import PARALLEL_HILL_CLIMBER
import os
import re
import numpy as np
import pandas as pd
import argparse
import time
import datetime
import collections

def format_time(elapsed):
    return str(datetime.timedelta(seconds=int(round((elapsed)))))

parser = argparse.ArgumentParser()
parser.add_argument('-type', type=str, help='evolve or show', default='evolve')
parser.add_argument('-run', type=int, help='run number', default=10)
parser.add_argument('-seed', type=float, help='seed number', default=None)
args = parser.parse_args()


if args.type == 'evolve':

    ### uncomment to delete old seeds
    # seeds.txt is used to save the seed for each run so I can get random results (1st body of 1st gen)
    # delete seeds.txt to start fresh
    # if os.path.exists('save/seeds.csv'):
    #     os.remove('save/seeds.csv')


    ### uncomment to run parallel hill climber (evolve)
    # ----------------------------
    # run parallel hill climber
    totalTime = time.time()
    runTime = collections.defaultdict(str)

    for i in range(args.run): # should be 10
        timeRun = time.time()
        print(f'PHC run: {i}')
        phc = PARALLEL_HILL_CLIMBER(phc_run=i, seed=args.seed)
        phc.Evolve()
        id = phc.Show_Best()
        phc.Save_Best()
    
        # save fitness data for plotting
        # np.savetxt(f'save/fitnessMat{i}.txt', phc.fitnessMat)
        
        runTime[i] = format_time(time.time() - timeRun)
    
    totalTime = time.time() - totalTime

    ### uncomment to save run time data
    # save run time data 
    # with open('save/runTime.txt', 'w') as f:
    #     f.write(f'Total time for {args.run} PHC runs: {format_time(totalTime)}\n')
    #     f.write(f'Average time per run: {format_time(totalTime/args.run)}\n')
    #     f.write(f'Run time for each run:\n')
    #     for key, value in runTime.items():
    #         f.write(f'{key}: {value}\n')
    # ----------------------------

else:

    ### uncomment to run best brain
    # ----------------------------
    regex = re.compile(r'\d+') # regex to find numbers in string
    identifiers = []

    # get best brain id from file name
    for file in os.listdir('save/'):
        if pd.Series(file).str.contains('brain').any():
            identifiers.append(regex.findall(file))
    identifiers.sort()
    print(identifiers)
    

    # run best brain simulation
    for i in range(args.run):
        print(identifiers[i])
        os.system(f'python3 simulate.py GUI {identifiers[i][1]} show {identifiers[i][0]} 2&>1 &') # identifiers[i][0] = run number, identifiers[i][1] = brain id
        time.sleep(20)
    # ----------------------------


