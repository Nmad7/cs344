'''
This module implements the Bayesian network shown in the text, Figure 14.2.
It's taken from the AIMA Python code.

@author: kvlinden
@student: Noah Madrid
@date: 3-6-20
'''

from probability import BayesNet, enumeration_ask, elimination_ask, gibbs_ask

# Utility variables
T, F = True, False

# From AIMA code (probability.py) - Fig. 14.2 - burglary example
burglary = BayesNet([
    ('Burglary', '', 0.001),
    ('Earthquake', '', 0.002),
    ('Alarm', 'Burglary Earthquake', {(T, T): 0.95, (T, F): 0.94, (F, T): 0.29, (F, F): 0.001}),
    ('JohnCalls', 'Alarm', {T: 0.90, F: 0.05}),
    ('MaryCalls', 'Alarm', {T: 0.70, F: 0.01})
    ])

# Compute P(Alarm |  burglary ∧ ¬earthquake).
print(enumeration_ask('Alarm', dict(Burglary=T, Earthquake=F), burglary).show_approx())

# Compute P(John | burglary ∧ ¬earthquake).
print(enumeration_ask('JohnCalls', dict(Burglary=T, Earthquake=F), burglary).show_approx())

# Compute P(Burglary | alarm).
print(enumeration_ask('Burglary', dict(Alarm=T), burglary).show_approx())

# Compute P(Burglary | john ∧ mary)
print(enumeration_ask('Burglary', dict(JohnCalls=T, MaryCalls=T), burglary).show_approx())

'''
Exercise 5.4
'''
print("\nExercise 5.4\n")
# Compute P(Burglary | John and Mary both call).
print(enumeration_ask('Burglary', dict(JohnCalls=T, MaryCalls=T), burglary).show_approx())
# elimination_ask() is a dynamic programming version of enumeration_ask().
print(elimination_ask('Burglary', dict(JohnCalls=T, MaryCalls=T), burglary).show_approx())
# gibbs_ask() is an approximation algorithm helps Bayesian Networks scale up.
print(gibbs_ask('Burglary', dict(JohnCalls=T, MaryCalls=T), burglary).show_approx())
# See the explanation of the algorithms in AIMA Section 14.4.

'''
enumeration_ask
False: 0.716, True: 0.284
elimination_ask
False: 0.716, True: 0.284
gibbs_ask
False: 0.708, True: 0.292

No, gibbs_ask gives a slightly different answer than enumeration_ask. Elimination_ask should give (and does give) the 
same answer as enumeration_ask as it removes needless calculations. Gibbs, on the other hand, randomly assigns
each non-evidence variable (in this case JohnCalls and MaryCalls) and samples them to get an estimate probability.
'''


