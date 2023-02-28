from solution import SOLUTION
import pyrosim.pyrosim as pyrosim
import constants as c
import copy
import os
import random
import pandas as pd

class PARALLEL_HILL_CLIMBER:
    def __init__(self):
        os.system('rm brain*.nndf')
        os.system('rm fitness*.txt')
        self.parents = {}
        self.nextAvailableID = 0
        self.minfitnessList = []*c.numberOfGenerations
        for i in range(c.populationSize):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1

    def Evolve(self):
        self.Evaluate(self.parents, -1)
        for currentGeneration in range(c.numberOfGenerations):
            print(f'Generation: {currentGeneration}')
            self.Evolve_For_One_Generation(currentGeneration)
        
    def Evolve_For_One_Generation(self, currentGeneration):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children, currentGeneration)
        self.printFitness()
        self.minfitnessList.append(self.getGenMinFitness())
        self.Select()

    def printFitness(self):
        print("\n")
        for parent in self.parents.keys():
            print(f"parent: {self.parents[parent].fitness}, child: {self.children[parent].fitness} \n")

    def getGenMinFitness(self):
        minFitness = float("inf")
        for parent in self.parents.keys():
            if self.parents[parent].fitness < minFitness:
                minFitness = self.parents[parent].fitness
        return minFitness
        
    def Spawn(self):
        self.children = {}
        for parent in self.parents.keys():
            self.children[parent] = copy.deepcopy(self.parents[parent])
            self.children[parent].Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1
    
    def Mutate(self):
        for child in self.children.keys():
            self.children[child].Mutate()

    def Evaluate(self, solutions, currentGeneration):
        for solution in solutions.keys():
            # show GUI on first generation
            if solution == 0 and currentGeneration == 0:
                solutions[solution].Start_Simulation("GUI")
            else:
                solutions[solution].Start_Simulation("DIRECT")
        for solution in solutions.keys():
            solutions[solution].Wait_For_Simulation_To_End()

    def Select(self):
        for parent in self.parents.keys():
            if self.parents[parent].fitness > self.children[parent].fitness:
                self.parents[parent] = self.children[parent]

    def Show_Best(self):
        minFitness = float("inf")
        bestParent = None
        for parent in self.parents.keys():
            if self.parents[parent].fitness < minFitness:
                minFitness = self.parents[parent].fitness
                bestParent = parent
        print(f'Best Parent: {bestParent}, Fitness: {minFitness}')
        self.parents[bestParent].Start_Simulation("GUI")
        # df = pd. DataFrame(self.minfitnessList)
        # df.to_csv("minfitnessList4.csv")
        # self.parents[bestParent].Wait_For_Simulation_To_End()
        

        