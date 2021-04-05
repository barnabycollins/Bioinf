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


    def convertToLog(structure: Union[list, float, int]) -> Union[list, float]:
        """Recursively converts numerical values in nested lists to log space"""

        if (type(structure) is list):
            output = []
            for i in structure:
                output.append(convertToLog(i))
            return output
        return safeLog(structure)

    def safeLog(number: float):
        """Returns the log of a number, returning -1e308 (the lower limit of a float) if the number is zero to avoid errors."""

        if (number == 0):
            return -1e308
        
        return math.log(number)

    symbols = list(OrderedDict.fromkeys(sequence).keys())
    num_symbols = len(symbols)

    sequence = [symbols.index(s) for s in sequence]
    sequenceLength = len(sequence)

    # Set random initial conditions
    transitions = generateProbabilityMatrix(num_states, num_states)
    emissions = generateProbabilityMatrix(num_states, num_symbols)
    initialDistribution = generateProbabilityMatrix(1, num_states)[0]

    lastLikelihood = -1
    likelihood = 0

    while (likelihood > lastLikelihood):
        print(f'Likelihood: {likelihood}')
        # Convert structures to log space
        [lTransitions, lEmissions, lInitialDistribution] = convertToLog([transitions, emissions, initialDistribution])
        
        lastLikelihood = likelihood
        
        # Initialise trellises
        fTrellis = []
        bTrellis = []
        for o in range(sequenceLength):
            fTrellis.append([])
            bTrellis.append([])

            for s in range(num_states):
                fTrellis[o].append(0.0)
                bTrellis[o].append(0.0)

        # === FORWARD ALGORITHM ===
        # Populate first row of trellis
        for s in range(num_states):
            fTrellis[0][s] = lInitialDistribution[s] + lEmissions[s][sequence[0]]
        
        # Populate the rest of the trellis
        for l in range(1, sequenceLength):
            for s in range(num_states):
                fTrellis[l][s] = lEmissions[s][sequence[l]] + safeLog(sum([math.exp(fTrellis[l-1][i] + lTransitions[i][s]) for i in range(num_states)]))

        # === BACKWARD ALGORITHM ===
        lastItem = sequenceLength - 1

        # Populate last row of trellis
        for s in range(num_states):
            bTrellis[lastItem][s] = 1.0

        # Populate the rest of the trellis
        for l in range(lastItem, 0, -1):
            for s in range(num_states):
                bTrellis[l-1][s] = safeLog(sum([math.exp(bTrellis[l][i] + lTransitions[s][i] + lEmissions[i][sequence[l]]) for i in range(num_states)]))
        

        # === UPDATE ESTIMATES ===
        # Probabilities of being in each state at each point in the sequence
        gammas = []

        # Probabilities of performing each transition at each point in the sequence
        etas = []

        for l in range(sequenceLength):
            gammas.append([])
            etas.append([])
            for s in range(num_states):
                gammas[l].append((fTrellis[l][s] + bTrellis[l][s]) - safeLog(sum([math.exp(fTrellis[l][i] + bTrellis[l][i]) for i in range(num_states)])))

                if (l != lastItem):
                    etas[l].append([])
                    for t in range(num_states):
                        top = fTrellis[l][s] + lTransitions[s][t] + bTrellis[l+1][t] + lEmissions[t][sequence[l+1]]
                        bottom = safeLog(sum([sum([math.exp(fTrellis[l][i] + lTransitions[i][j] + bTrellis[l+1][j] + lEmissions[j][sequence[l+1]]) for j in range(num_states)]) for i in range(num_states)]))
                        etas[l][s].append(top - bottom)
        
        # Update parameters
        initialDistribution = []
        transitions = []
        emissions = []

        for s in range(num_states):

            initialDistribution.append(math.exp(gammas[0][s]))
            transitions.append([])
            emissions.append([])

            bottom = sum([math.exp(gammas[l][s]) for l in range(sequenceLength-1)])

            # Update transition matrix
            for t in range(num_states):
                top = sum([math.exp(etas[l][s][t]) for l in range(sequenceLength-1)])

                transitions[s].append(top / bottom)
            
            # Update emission probabilities
            for o in range(num_symbols):
                top = sum([int(sequence[l] == o) * math.exp(gammas[l][s]) for l in range(sequenceLength)])

                emissions[s].append(top / bottom)

        # Compute likelihood for new parameters
        likelihood = sum([safeLog(sum([math.exp(emissions[s][sequence[l]]) for s in range(num_states)])) for l in range(sequenceLength)])
    
    return (initialDistribution, transitions, emissions, symbols, likelihood)
