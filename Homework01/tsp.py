"""
This implements a local-search version of TSP for AIMA-Python.
@author: Noah Madrid
"""
from search import Problem, hill_climbing, simulated_annealing, exp_schedule, RandomGraph
import random

class TSP(Problem):
    """An implementation of TSP for local search.
        State representation:
            [city0, city1, city2]
        Move representation:
            [index0, index1]: Swap the city in the given path index with the city in the other index.
    """
    def __init__(self, initialPath, cityGraph):
        self.initial = initialPath
        self.cityGraph = cityGraph

    def actions(self, state):
        """Actions: swap two cities next to each other in the path (as long as the first and last city are not altered)
        """
        actions = []
        for i in range(1, len(state)-2):
            newPath = state[:]
            newPath[i], newPath[i+1] = newPath[i+1], newPath[i]
            actions.append(newPath)
        return actions

    def result(self, state, move):
        """Makes the given move."""
        return move

    def value(self, state):
        """This method computes a value of given state using distance traveled
        """
        value = 0;
        for i in range(len(state)-1):
            value = value + cityGraph.get(state[i],state[i+1])
        # multiply by one to pursue the lowest value
        return -1 * value

if __name__ == '__main__':
    # Set the number of cities
    cityAmount = 20
    print('Cities:\t\t' + str(cityAmount))

    # Create unique city ids and add them to city list
    cityList = []
    for i in range(cityAmount):
        cityList.append(str(i))

    # Create a random graph using search RandomGraph()
    cityGraph = RandomGraph(cityList, cityAmount-1, 10000, 10000)

    # Initialize initial path randomly
    path = random.sample(cityGraph.nodes(), len(cityGraph.nodes()))

    # Add first city as the last city to make it the destination
    path.append(path[0])
    print('Starting path:\t' + str(path))

    p = TSP(path,cityGraph)

    # Solve the problem using hill climbing.
    hill_solution = hill_climbing(p)
    print('\nHill-climbing:')
    print('\tSolution:\t' + str(hill_solution))
    print('\tValue:\t\t' + str(p.value(hill_solution)))

    # Solve the problem using simulated annealing.
    annealing_solution = \
        simulated_annealing(p, exp_schedule(k=20, lam=0.005, limit=10000))
    print('\nSimulated annealing:')
    print('\tSolution:\t' + str(annealing_solution))
    print('\tValue:\t\t' + str(p.value(annealing_solution)))