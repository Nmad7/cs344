'''
This module implements the Bayesian network shown in the text, Figure 14.12a.
@student: Noah Madrid
@date: 3-6-20
'''

from probability import BayesNet, enumeration_ask, elimination_ask, gibbs_ask

# Utility variables
T, F = True, False

wet = BayesNet([
    ('Cloudy', '', 0.5),
    ('Sprinkler', 'Cloudy', {T: 0.1, F: 0.50}),
    ('Rain', 'Cloudy', {T: 0.80, F: 0.2}),
    ('WetGrass', 'Sprinkler Rain', {(T, T): 0.99, (T, F): 0.90, (F, T): 0.90, (F, F): 0.00})
    ])

# Compute P(cloudy)
print(enumeration_ask('Cloudy', dict(), wet).show_approx())

# Compute P(Sprinkler | cloudy)
print(enumeration_ask('Sprinkler', dict(Cloudy=T), wet).show_approx())

# Compute P(Cloudy| the sprinkler is running and it’s not raining)
print(enumeration_ask('Cloudy', dict(Sprinkler=T, Rain=F), wet).show_approx())

# Compute P(WetGrass | it’s cloudy, the sprinkler is running and it’s raining)
print(enumeration_ask('WetGrass', dict(Cloudy=T, Sprinkler=T, Rain=T), wet).show_approx())

# Compute P(Cloudy | the grass is not wet)
print(enumeration_ask('Cloudy', dict(WetGrass=F), wet).show_approx())


