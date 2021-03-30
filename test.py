import random
from q1a import ExpectationMaximisation as EM

NUM_STATES = 8
NUM_SYMBOLS = 4

def generateProbabilityMatrix(height, width=False):
    if (width == False):
        width = height

    matrix = []

    for i in range(height):
        # randpd2 from https://thehousecarpenter.wordpress.com/2017/02/22/generating-random-probability-distributions/
        variates = [random.random() for i in range(width)]
        s = sum(variates)
        matrix.append([i/s for i in variates])
    
    return matrix

transitions = generateProbabilityMatrix(NUM_STATES)
emissions = generateProbabilityMatrix(NUM_STATES, NUM_SYMBOLS)
symbols = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'][:NUM_SYMBOLS]
observations = 'ABCDCBA'

EM(observations, symbols, transitions, emissions)
