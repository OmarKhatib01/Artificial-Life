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
args = parser.parse_args()

# get seeds from save/seeds.txt



if args.type == 'evolve':
    # seeds.txt is used to save the seed for each run so I can get random results (1st body of 1st gen)
    # delete seeds.txt to start fresh
    if os.path.exists('save/seeds.csv'):
        os.remove('save/seeds.csv')
    ### uncomment to run parallel hill climber (evolve)
    # ----------------------------
    # run parallel hill climber
    totalTime = time.time()
    runTime = collections.defaultdict(str)

    for i in range(args.run): # should be 10
        timeRun = time.time()
        print(f'PHC run: {i}')
        phc = PARALLEL_HILL_CLIMBER(phc_run=i, seed=None)
        phc.Evolve()
        id = phc.Show_Best()
        phc.Save_Best()
    
        # save fitness data for plotting
        np.savetxt(f'save/fitnessMat{i}.txt', phc.fitnessMat)
        print(f'Fitness matrix saved to save/fitnessMat{i}.txt')

        runTime[i] = format_time(time.time() - timeRun)
    
    totalTime = time.time() - totalTime
    print(f'Total time for {args.run} PHC runs: {format_time(totalTime)}')
    print(f'Average time per run: {format_time(totalTime/args.run)}')
    print(f'Run time per run: {runTime}')
    # ----------------------------

else:

    ### uncomment to run best brain
    # ----------------------------
    regex = re.compile(r'\d+') # regex to find numbers in string
    phc_run = []
    bestId = []

    # get best brain id from file name
    for file in os.listdir('save/'):
        if pd.Series(file).str.contains('brain').any():
            print(regex.findall(file))
            phc_run.append(regex.findall(file)[0])
            bestId.append(regex.findall(file)[1])
    print(f'phc_run: {phc_run}')
    print(f'bestId: {bestId}')
    

    # run best brain simulation
    for i in range(args.run):
        os.system(f'python3 simulate.py GUI {bestId[i]} test {phc_run[i]} 2&>1 &')
        time.sleep(15)
    # ----------------------------


