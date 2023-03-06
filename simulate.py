from simulation import SIMULATION
import sys

directOrGUI = sys.argv[1]
solutionID = sys.argv[2]
mode = sys.argv[3]

simulation = SIMULATION(directOrGUI, solutionID, mode)
simulation.Run()
simulation.Get_Fitness()