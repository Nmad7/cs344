"""
This module implements local search on a sine function.
@author: ngm7
@date: 02-14-19
"""
from search import Problem, hill_climbing, simulated_annealing, \
    exp_schedule, genetic_search
from random import randrange
import math
from numpy.ma.core import sin
# added time tracking
import time


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
    # Formulate a problem with a 2D hill function and a single maximum value.
    maximum = 30
    i = 0
    initialList = []
    xList = []
    valueList = []
    while i > 100:
        initial = randrange(0, maximum)
        initialList [i] = initial
        p = SineVariant(initial, maximum, delta=1)
        # Solve the problem using hill-climbing.
        hill_solution = hill_climbing(p)
        xList[i] = hill_solution
        valueList [i] = p.value(hill_solution)
        i = i + 1
    i = 0
    bestValue = 0
    while i > 100:
        initial = randrange(0, maximum)
        p = SineVariant(initial, maximum, delta=1)
        # Solve the problem using simulated annealing.
        tic = time.perf_counter()

        annealing_solution = simulated_annealing(
            p,
            exp_schedule(k=20, lam=0.005, limit=1000)
        )

        toc = time.perf_counter()
        print(f"annealing_solution in {toc - tic:0.4f} seconds")
        print('Simulated annealing solution x: ' + str(annealing_solution)
              + '\tvalue: ' + str(p.value(annealing_solution))
              )
