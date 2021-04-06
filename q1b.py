import math
from collections import OrderedDict
from typing import Union

def ExpectationMaximisation(sequence: str, num_states: int, alphabet: list = []) -> tuple:
    """Finds a local maximum set of parameters for an HMM with 'num_states' states and observed output 'sequence'

    Parameters:
    - sequence:     a string representing observed outputs.
                    eg, 'ACTGGTCTCGAGTGTGACTG'
                    Note that this implementation assumes that each single character in the string is a separate symbol!
    - num_states:   the integer number of states the HMM being modelled has.
    - [alphabet]:   The (OPTIONAL) alphabet. If none is given, it will be generated from the characters in the sequence.

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
            # this uses randpd2 from https://thehousecarpenter.wordpress.com/2017/02/22/generating-random-probability-distributions/

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
        """Returns the log of a number, returning -1e308 (the lower limit of Python float) if the number is zero to avoid errors."""

        #if (number == 0):
            #print("BRUH 2")
            #return -1e308
        
        return math.log(number)
    
    def safeExp(number: float):
        """Returns the log of a number, returning -1e308 (the lower limit of Python float) if the number is zero to avoid errors."""

        #try:
        return math.exp(number)
        
        """except OverflowError:
            #print("BRUH 1")
            if (number > 0):
                return 1e308
            
            else:
                return 0"""
    

    if (alphabet == []):
        alphabet = list(OrderedDict.fromkeys(sequence).keys())
    
    num_symbols = len(alphabet)

    sequence = [alphabet.index(s) for s in sequence]
    sequenceLength = len(sequence)

    # Set random initial conditions
    transitions = generateProbabilityMatrix(num_states, num_states)
    emissions = generateProbabilityMatrix(num_states, num_symbols)
    initialDistribution = generateProbabilityMatrix(1, num_states)[0]

    lastLikelihood = -1
    likelihood = sum([safeLog(sum([safeExp(emissions[s][sequence[l]]) for s in range(num_states)])) for l in range(sequenceLength)])

    # Do-while loop
    while likelihood > lastLikelihood:
        print(f'Likelihood: {likelihood}')
        # Convert structures to log space
        #[lTransitions, lEmissions, lInitialDistribution] = convertToLog([transitions, emissions, initialDistribution])

        #print('\n'.join([str(i) for i in [transitions, emissions, initialDistribution]]))
        lTransitions = convertToLog(transitions)
        lEmissions = convertToLog(emissions)
        lInitialDistribution = convertToLog(initialDistribution)
        
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

        rowSums = []

        # === FORWARD ALGORITHM ===
        # Populate first row of trellis
        for s in range(num_states):
            fTrellis[0][s] = lInitialDistribution[s] + lEmissions[s][sequence[0]]

        # Scale probabilities properly (based on section V.A in Rabiner 1989 - http://dx.doi.org/10.1109/5.18626)
        rowSum = safeLog(sum([safeExp(fTrellis[0][i]) for i in range(num_states)]))
        fTrellis[0] = [(fTrellis[0][i] - rowSum) for i in range(num_states)]
        rowSums.append(rowSum)
        
        # Populate the rest of the trellis
        for l in range(1, sequenceLength):
            for s in range(num_states):
                fTrellis[l][s] = lEmissions[s][sequence[l]] + safeLog(sum([safeExp(fTrellis[l-1][i] + lTransitions[i][s]) for i in range(num_states)]))

            # Scale probabilities properly
            rowSum = safeLog(sum([safeExp(fTrellis[l][i]) for i in range(num_states)]))
            fTrellis[l] = [(fTrellis[l][i] - rowSum) for i in range(num_states)]
            rowSums.append(rowSum)

        # === BACKWARD ALGORITHM ===
        lastItem = sequenceLength - 1

        # Populate last row of trellis
        for s in range(num_states):
            bTrellis[lastItem][s] = 1.0
        
        # Scale probabilities properly
        rowSum = rowSums[lastItem]
        bTrellis[lastItem] = [(bTrellis[lastItem][i] - rowSum) for i in range(num_states)]

        # Populate the rest of the trellis
        for l in range(lastItem, 0, -1):
            for s in range(num_states):
                try:
                    bTrellis[l-1][s] = safeLog(sum([safeExp(bTrellis[l][i] + lTransitions[s][i] + lEmissions[i][sequence[l]]) for i in range(num_states)]))
                
                except Exception as e:
                    print(e)
                    print([[safeExp(bTrellis[l][i]), safeExp(lTransitions[s][i]), safeExp(lEmissions[i][sequence[l]])] for i in range(num_states)])
                    print("fuck this")
                    exit()

            # Scale probabilities properly
            rowSum = rowSums[l]
            bTrellis[l] = [(bTrellis[l][i] - rowSum) for i in range(num_states)]
        

        # === UPDATE ESTIMATES ===
        # Probabilities of being in each state at each point in the sequence
        gammas = []

        # Probabilities of performing each transition at each point in the sequence
        etas = []

        for l in range(sequenceLength):
            gammas.append([])
            etas.append([])
            for s in range(num_states):
                gammas[l].append((fTrellis[l][s] + bTrellis[l][s]) - safeLog(sum([safeExp(fTrellis[l][i] + bTrellis[l][i]) for i in range(num_states)])))

                if (l != lastItem):
                    etas[l].append([])
                    for t in range(num_states):
                        top = fTrellis[l][s] + lTransitions[s][t] + bTrellis[l+1][t] + lEmissions[t][sequence[l+1]]
                        bottom = safeLog(sum([sum([safeExp(fTrellis[l][i] + lTransitions[i][j] + bTrellis[l+1][j] + lEmissions[j][sequence[l+1]]) for j in range(num_states)]) for i in range(num_states)]))
                        etas[l][s].append(top - bottom)
        
        # Update parameters
        newInitialDistribution = []
        newTransitions = []
        newEmissions = []

        for s in range(num_states):

            newInitialDistribution.append(safeExp(gammas[0][s]))
            newTransitions.append([])
            newEmissions.append([])

            bottom = sum([safeExp(gammas[l][s]) for l in range(sequenceLength-1)])

            # Update transition matrix
            for t in range(num_states):
                top = sum([safeExp(etas[l][s][t]) for l in range(sequenceLength-1)])

                newTransitions[s].append(top / bottom)
            
            # Update emission probabilities
            for o in range(num_symbols):
                top = sum([int(sequence[l] == o) * safeExp(gammas[l][s]) for l in range(sequenceLength)])

                newEmissions[s].append(top / bottom)

        # Compute likelihood for new parameters
        likelihood = sum([safeLog(sum([safeExp(newEmissions[s][sequence[l]]) for s in range(num_states)])) for l in range(sequenceLength)])
    
        if (likelihood <= lastLikelihood):
            break
        
        initialDistribution = newInitialDistribution
        transitions = newTransitions
        emissions = newEmissions
    
    return (initialDistribution, transitions, emissions, alphabet, likelihood)
