"""
This module implements a Bayesian network

@author: kvlinden
@student: Noah Madrid
@date: 3-6-20
"""

from probability import BayesNet, enumeration_ask, elimination_ask, gibbs_ask

# Utility variables
T, F = True, False

# From AIMA code (probability.py) - Fig. 14.2 - burglary example
happiness = BayesNet([
    ('Sunny', '', 0.7),
    ('Raise', '', 0.01),
    ('Happy', 'Sunny Raise', {(T, T): 1.0, (T, F): 0.7, (F, T): 0.9, (F, F): 0.1})
    ])

print(enumeration_ask('Raise', dict(Sunny=T), happiness).show_approx())

print(enumeration_ask('Raise', dict(Happy=T, Sunny=T), happiness).show_approx())

'''
P(Raise | sunny) = <T=.01,F=.99>
This result makes sense as the weather being sunny, at least in our model,
has no impact on a raise occurring meaning that the answer should just be the 
probability of a raise.
P(Raise | happy ∧ sunny) = <T=.0142,F=.986>
This small increase of a result makes sense as even though a person is happy, given that we know
it is also sunny then one's happiness can be explained away by it being sunny making it less likely 
the raise was the cause.

P(Raise | Sunny)= <.01,.99> due to the fact that sunny is independent of raise.

P(Raise | Happy ∧ Sunny) = α P(C, t1, ¬t2) = α P(H | R, S) * P(R|S) = α P(H | R, S) * P(R)
α <1*.01,.7*.99>
<.0142,.986>

'''

print(enumeration_ask('Raise', dict(Happy=T), happiness).show_approx())

print(enumeration_ask('Raise', dict(Happy=T, Sunny=F), happiness).show_approx())

'''
P(Raise | happy) = <T=0.0185,F=.982>

P(Raise | happy ∧ ¬sunny) = <T=0.0833,F=0.917>

These results make sense as given that we know someone is happy, 
the chance of them being happy from a raise rather than something else
is very small. The second answer also makes sense as even though
we know the happiness was not caused by the sun, the chance of 
it being from a raise is still very small as other things could have
caused the happiness.
'''