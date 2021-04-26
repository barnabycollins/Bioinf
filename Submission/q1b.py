import math
from collections import OrderedDict
from typing import Union

def ExpectationMaximisation(sequence: str, num_states: int, alphabet: list = [], max_iter: int = 1000, log: bool = False) -> tuple:
    """Finds a local maximum set of parameters for an HMM with 'num_states' states and observed output 'sequence'

    Parameters:
    - sequence:     a string of single-character symbols representing observed outputs
                    eg, 'ACTGGTCTCGAGTGTGACTG'
    - num_states:   the integer number of states the HMM being modelled has
    - alphabet:     (Optional; default []) a list of all the symbols to be found in the sequence.
                    Will be generated automatically from the sequence if omitted or an empty list is given.
    - max_iter:     (Optional; default 1000) The maximum number of iterations to perform before stopping.
                    The algorithm will stop before this point if increase in likelihood drops below machine precision.
    - log:          (Optional; default False) Whether to output the likelihood to the command line on each iteration.

    Returns a tuple of optimised parameters, as follows:
    (
        Initial state probability distribution (ie, for the first state in the sequence)
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

    def safeLog(number: Union[int, float]) -> float:
        """Returns the log of a number, returning -infinity if the number is 0 to avoid errors."""

        if (number == 0):
            return -math.inf
        
        return math.log(number)
    
    def safeExp(number: Union[int, float]) -> float:
        """Returns the log of a number, returning 0 if the number is -infinity to avoid errors."""

        if (number == -math.inf):
            return 0
        
        return math.exp(number)


    if (alphabet == []):
        alphabet = list(OrderedDict.fromkeys(sequence).keys())
    
    num_symbols = len(alphabet)

    sequence = [alphabet.index(s) for s in sequence]
    sequenceLength = len(sequence)

    # Set random initial conditions
    transitions = generateProbabilityMatrix(num_states, num_states)
    emissions = generateProbabilityMatrix(num_states, num_symbols)
    initialDistribution = generateProbabilityMatrix(1, num_states)[0]

    # Convert structures to log space
    [lTransitions, lEmissions, lInitialDistribution] = convertToLog([transitions, emissions, initialDistribution])

    lastLikelihood = -1.1e308
    likelihood = -1e308

    # This is effectively a do-while loop: there is a check when a new likelihood is generated to break when
    #   no further improvements are being made
    for i in range(max_iter):
        
        lastLikelihood = likelihood
        
        # Initialise trellises
        fTrellis = []
        bTrellis = []
        for o in range(sequenceLength):
            fTrellis.append([])
            bTrellis.append([])

            for s in range(num_states):
                fTrellis[o].append(0)
                bTrellis[o].append(0)
        
        rowSums = [0 for i in range(sequenceLength)]

        # === FORWARD ALGORITHM ===
        # Populate first row of trellis
        for s in range(num_states):
            fTrellis[0][s] = lInitialDistribution[s] + lEmissions[s][sequence[0]]
            rowSums[0] += safeExp(fTrellis[0][s])
        
        # Scale values - based on section V. A in http://dx.doi.org/10.1109/5.18626
        rowSums[0] = safeLog(rowSums[0])
        fTrellis[0] = [fTrellis[0][s] - rowSums[0] for s in range(num_states)]
        
        # Populate the rest of the trellis
        for l in range(1, sequenceLength):
            for s in range(num_states):
                fTrellis[l][s] = lEmissions[s][sequence[l]] + safeLog(sum([safeExp(fTrellis[l-1][i] + lTransitions[i][s]) for i in range(num_states)]))
                rowSums[l] += safeExp(fTrellis[l][s])
            
            rowSums[l] = safeLog(rowSums[l])
            fTrellis[l] = [fTrellis[l][s] - rowSums[l] for s in range(num_states)]

        # === BACKWARD ALGORITHM ===
        lastItem = sequenceLength - 1

        # Populate last row of trellis
        for s in range(num_states):
            bTrellis[lastItem][s] = safeLog(1.0)

        # Populate the rest of the trellis
        for l in reversed(range(0, lastItem)):
            for s in range(num_states):
                bTrellis[l][s] = safeLog(sum([safeExp(bTrellis[l+1][i] + lTransitions[s][i] + lEmissions[i][sequence[l+1]]) for i in range(num_states)]))
            
            bTrellis[l] = [bTrellis[l][s] - rowSums[l] for s in range(num_states)]
        

        # === UPDATE ESTIMATES ===
        # Probabilities of being in each state at each point in the sequence
        gammas = []

        # Probabilities of performing each transition at each point in the sequence
        ksis = []

        for l in range(sequenceLength):
            gammas.append([])

            if (l != lastItem):
                ksis.append([])
                bottom = safeLog(sum([sum([safeExp(fTrellis[l][i] + lTransitions[i][j] + bTrellis[l+1][j] + lEmissions[j][sequence[l+1]]) for j in range(num_states)]) for i in range(num_states)]))

            for s in range(num_states):
                gammas[l].append((fTrellis[l][s] + bTrellis[l][s]) - safeLog(sum([safeExp(fTrellis[l][i] + bTrellis[l][i]) for i in range(num_states)])))

                if (l != lastItem):
                    ksis[l].append([])

                    for t in range(num_states):
                        top = fTrellis[l][s] + lTransitions[s][t] + bTrellis[l+1][t] + lEmissions[t][sequence[l+1]]
                        ksis[l][s].append(top - bottom)

        # Compute likelihood for new parameters
        likelihood = sum(rowSums)
        
        if (log):
            print(f'Likelihood: {likelihood}')

        if (likelihood == lastLikelihood):
            break

        lastLikelihood = likelihood
        
        # Update parameters
        initialDistribution = []
        transitions = []
        emissions = []

        for s in range(num_states):

            initialDistribution.append(safeExp(gammas[0][s]))
            transitions.append([])
            emissions.append([])

            bottomList = [safeExp(gammas[l][s]) for l in range(sequenceLength)]

            bottom_t = sum(bottomList[:-1])
            bottom_e = sum(bottomList)

            # Update transition matrix
            for t in range(num_states):
                top = sum([safeExp(ksis[l][s][t]) for l in range(sequenceLength-1)])

                transitions[s].append(top / bottom_t)
            
            # Update emission probabilities
            for o in range(num_symbols):
                top = sum([int(sequence[l] == o) * safeExp(gammas[l][s]) for l in range(sequenceLength)])

                emissions[s].append(top / bottom_e)
        
        # Convert structures to log space
        [lTransitions, lEmissions, lInitialDistribution] = convertToLog([transitions, emissions, initialDistribution])
    
    return (initialDistribution, transitions, emissions, alphabet, likelihood)
