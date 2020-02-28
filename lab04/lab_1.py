'''
@author: ngm7
@date Feb 28, 2020
'''

from probability import JointProbDist, enumerate_joint_ask

P = JointProbDist(['Toothache', 'Cavity', 'Catch'])
T, F = True, False
P[T, T, T] = 0.108; P[T, T, F] = 0.012
P[F, T, T] = 0.072; P[F, T, F] = 0.008
P[T, F, T] = 0.016; P[T, F, F] = 0.064
P[F, F, T] = 0.144; P[F, F, F] = 0.576

# Computer P(Cavity|CatchT) by hand
# P(Cavity|Catch)=P(Cavity^Catch)/P(Catch)=(.108+.072)/(.108+.072+.016+.144)=.529

# Compute P(Cavity|Catch=T)
PC = enumerate_joint_ask('Cavity', {'Catch': T}, P)
print(PC.show_approx())

P = JointProbDist(['Coin 1', 'Coin 2'])
P[T, T] = 0.25; P[T, F] = 0.25
P[F, T] = 0.25; P[F, F] = 0.25

# Compute P(Cavity|Catch=T)
PC = enumerate_joint_ask('Coin 2', {'Coin 1': T}, P)
print(PC.show_approx())


