import math
from collections import OrderedDict
from typing import Union

def ExpectationMaximisation(sequence: str, num_states: int) -> tuple:
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

