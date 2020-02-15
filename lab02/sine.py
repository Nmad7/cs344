"""
This module implements local search on a sine function.
@author: ngm7 (Noah Madrid)
@date: 02-14-19
"""
from search import Problem, hill_climbing, simulated_annealing, \
    exp_schedule, genetic_search
from random import randrange
import math
from numpy.ma.core import sin


class SineVariant(Problem):
    """
    State: x value for the sine function variant f(x)
    Move: a new x value delta steps from the current x (in both directions)
    """

    def __init__(self, initial, maximum=30.0, delta=0.001):
        self.initial = initial
        self.maximum = maximum
        self.delta = delta

    def actions(self, state):
        return [state + self.delta, state - self.delta]

    def result(self, stateIgnored, x):
        return x

    def value(self, x):
        return abs(x * sin(x))


if __name__ == '__main__':
    # random restarting sine function
    maximum = 30
    i = 0
    # Create lists to store values from each restart
    initialList = []
    hillList = []
    annealingList = []
    hillBest = [0,0]
    annealingBest = [0,0]

    #Do a random restart 50 times
    while i < 50:
        initial = randrange(0, maximum)
        p = SineVariant(initial, maximum, delta=1.0)
        initialList.append([p.initial, p.value(initial)])
        # Solve the problem using hill-climbing.
        hill_solution = hill_climbing(p)
        hillList.append([hill_solution, p.value(hill_solution)])
        if hillBest[1] < p.value(hill_solution):
            hillBest = [hill_solution, p.value(hill_solution)]
        # Solve the problem using simulated annealing
        annealing_solution = simulated_annealing(
            p,
            exp_schedule(k=20, lam=0.005, limit=1000)
        )
        # Throw out value if maximum is past graph maximum (to get more accurate average/best value)
        if maximum < annealing_solution:
            # Assume that if simulated annealing goes past the max it would have stopped there
            annealingBest = [30, 30.0]
            annealingList.append([30, 30.0])
        else:
            # If the answer is valid append it and update best
            annealingList.append( [annealing_solution, p.value(annealing_solution)])
            if annealingBest[1] < p.value(annealing_solution):
                annealingBest = [annealing_solution, p.value(annealing_solution)]
        # Go to next restart
        i = i + 1

    # after 50 restarts of both programs
    print('Hill-climbing best       x: ' + str(hillBest[0])
          + '\tvalue: ' + str(p.value(hillBest[1]))
          )
    # Find the average value of hill climb
    hillAverage = 0
    for i in range(len(hillList)):
        hillAverage = hillList[i][1] + hillAverage
    print('hillaverage: '+str(hillAverage/len(hillList)))

    print('Simulated annealing best x: ' + str(annealingBest[0])
          + '\tvalue: ' + str(p.value(annealingBest[1]))
          )
    # Find the average value of simulated annealing
    annealingAverage = 0
    for i in range(len(annealingList)):
        annealingAverage = annealingList[i][1] + annealingAverage
    print('annealingAverage: '+str(annealingAverage/len(annealingList)))