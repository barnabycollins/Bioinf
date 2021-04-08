import math
from collections import OrderedDict
import numpy as np

def generateProbabilityMatrix(height: int, width: int) -> list:
    """Generates and returns a randomised matrix where each row contains a discrete probability distribution
    Parameters
    - height = number of distributions
    - width = number of items in each distribution
    """

    import random

    matrix = []

    for i in range(height):
        # randpd2 from https://thehousecarpenter.wordpress.com/2017/02/22/generating-random-probability-distributions/

        variates = [random.random() for i in range(width)]
        s = sum(variates)
        matrix.append([i/s for i in variates])
    
    return matrix


def ExpectationMaximisation(sequence, num_states, alphabet = []):
    """Finds a local maximum set of parameters for an HMM with 'num_states' states and observed output 'sequence'

    Parameters:
    - sequence:     a string of symbols representing observed outputs
                    eg, 'ACTGGTCTCGAGTGTGACTG'
    - num_states:   the integer number of states the HMM being modelled has

    Returns a tuple of optimised parameters, as follows:
    (
        Initial state probability distribution (ie, for the first item in the sequence)
        State transition matrix (as a 2D list, where the inner lists represent the distribution of transitions from one state)
        Emission matrix (as a 2D list, where the inner lists represent the distribution of observed symbols for one state)
        Ordered list of the symbols (mapping symbols to indices in the emission matrix)
        Log likelihood of the optimised parameters
    )
    """

    if (alphabet == []):
        alphabet = list(OrderedDict.fromkeys(sequence).keys())

    num_symbols = len(symbols)
    len_sequence = len(sequence)

    observed = [alphabet.index(s) for s in sequence]

    [initialStates, endStates] =    generateProbabilityMatrix(2, num_states)
    transitions =                   generateProbabilityMatrix(num_states, num_states)
    emissions =                     generateProbabilityMatrix(num_states, num_symbols)

    # === FORWARD ALGORITHM ===
    fTrellis = [[] for o in len_sequence]
    fTrellis[0] = [initialStates[s] * emissions[s][observed[0]] for s in range(num_states)]
    for i, x in enumerate(observed)[1:]:
        for s in range(num_states):
            fTrellis[i].append(0)
            for r in range(num_states):
                fTrellis[i][s] += fTrellis[i-1][r] * transitions[r][s]
            
            fTrellis[i][s] *= emissions[s][x]
    
    lastItem = len_sequence - 1

    bTrellis = [[] for o in len_sequence]
    bTrellis[lastItem] = endStates
    for i, x in reversed(enumerate(observed)):
        pass # bruh
