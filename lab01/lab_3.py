"""
lab_3.py
Author: Noah Madrid
CS344
A problem GPS cannot solve
GPS cannot do things well if goals are order specific as it will go down
one path and not be able to do the other becuase it cannot reverse
"""
from gps import gps

# Formulate the problem states and actions.
problem = {
    'initial': ['in helicopter', 'parachute in helicopter'],
    'goal': ['landed safely'],

    'actions': [
        {
            'action': 'jump off',
            'preconds': [
                'in helicopter'
            ],
            'add': [
                'falling'
            ],
            'delete': [
                'in helicopter',
            ]
        },
        {
            # if one switches around 'falling' and 'have parachute' the program functions correctly
            # because it looks for grabbing the parachute first instead of falling
            'action': 'open parachute',
            'preconds': [
                'falling',
                'have parachute'
            ],
            'add': [
                'landed safely'
            ],
            'delete': [
                'have parachute'
            ]
        },
        {
            'action': 'grab parachute',
            'preconds': [
                'in helicopter',
                'parachute in helicopter'
            ],
            'add': [
                'have parachute'
            ],
            'delete': [
                'have parachute',
                'parachute in helicopter'
            ]
        }
    ]
}


if __name__ == '__main__':

    # Use GPS to solve the problem formulated above.
    actionSequence = gps(
        problem['initial'],
        problem['goal'],
        problem['actions']
    )

    # Print the solution, if there is one.
    if actionSequence is not None:
        for action in actionSequence:
            print(action)
    else:
        print('plan failure...')
