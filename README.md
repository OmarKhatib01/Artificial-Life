# cs-396-Alife - Omar Khatib

## Assignment 5 - Design Your Own Creature

My program is designed to make a creature with 4 legs and 4 arms learn how to jump. To achieve the act of "jumping" in this evolutionary algorithm, a fitness function (`Get_Fitness()` in robot.py) records the fitness as a weighted sum of the longest time the 4 legs are off the ground denoted by `maxLen`, and the z coordinate of the torso denoted by `zposition`. 
The fitness is then maximized through multiple parallel simulations over a number of generations to find the best performing creature. 

## Assignment 6 - generate random 1D creature morphologies

I edited the solution.py to generate random geometries of a 1D kinematic machine with random number of randomly shaped links with random sensor placement along the chain. Links with and without sensors are colored green and blue, respectively. The different shapes (box, sphere, and cylinder) are added by altering multiple files in the pyrosim directory to be written into the body.urdf file correctly

### Running the Code:
#### Follow the steps below to reproduce results

1. Clone the repository into a directory of your choice

2. create a virtual environment for the directory 

3. switch to the branch `assgmtX` by running `git checkout assgmtX` in your console

4. run `main.py`
