# cs-396-Alife - Omar Khatib

## Assignment 5 - Design Your Own Creature

My program is designed to make a creature with 4 legs and 4 arms learn how to jump. To achieve the act of "jumping" in this evolutionary algorithm, a fitness function (`Get_Fitness()` in robot.py) records the fitness as a weighted sum of the longest time the 4 legs are off the ground denoted by `maxLen`, and the z coordinate of the torso denoted by `zposition`. 
The fitness is then maximized through multiple parallel simulations over a number of generations to find the best performing creature. 

### Running the Code:
#### Follow the steps below to reproduce results

1. Clone the repository into a directory of your choice

2. create a virtual environment for the directory 

3. switch to the branch `assgmt5` by running `git checkout assgmt5` in your console

4. run `main.py`