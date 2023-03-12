from simulation import SIMULATION
import sys

directOrGUI = sys.argv[1]
solutionID = sys.argv[2]
mode = sys.argv[3]
phc_run = sys.argv[4]

simulation = SIMULATION(directOrGUI, solutionID, mode, phc_run=phc_run)
simulation.Run()
simulation.Get_Fitness()