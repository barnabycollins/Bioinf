
def ExpectationMaximisation(sequence, num_states):
    
    # Generates and returns a randomised matrix where each row contains a discrete probability distribution
    # - height = number of distributions
    # - width = number of items in each distribution
    def generateProbabilityMatrix(height, width=False):
        import random
        if (width == False):
            width = height

        matrix = []

        for i in range(height):
            # randpd2 from https://thehousecarpenter.wordpress.com/2017/02/22/generating-random-probability-distributions/

            variates = [random.random() for i in range(width)]
            s = sum(variates)
            matrix.append([i/s for i in variates])
        
        return matrix


    # Recursively converts numerical values in nested lists to log space
    def convertToLog(structure):
        if (type(structure) is list):
            output = []
            for i in structure:
                output.append(convertToLog(i))
            return output
        return math.log(structure)


    import math
    from collections import OrderedDict

    symbols = list(OrderedDict.fromkeys(sequence).keys())
    num_symbols = len(symbols)

    sequence = [sequence.index(s) for s in symbols]
    sequenceLength = len(sequence)

    # Set random initial conditions
    transitions = generateProbabilityMatrix(num_states)
    emissions = generateProbabilityMatrix(num_states, num_symbols)
    initialDistribution = generateProbabilityMatrix(1, num_states)[0]

    # Convert structures to log space
    [lTransitions, lEmissions, lInitialDistribution] = convertToLog([transitions, emissions, initialDistribution])

    # Initialise trellises
    fTrellis = []
    bTrellis = []
    for o in range(sequenceLength):
        fTrellis.append([])
        bTrellis.append([])

        for s in range(num_states):
            fTrellis[i].append(0.0)
            bTrellis[i].append(0.0)

    # === FORWARD ALGORITHM ===
    # Populate first row of trellis
    for s in range(num_states):
        fTrellis[0][s] = lInitialDistribution[s] + lEmissions[s][sequence[0]]
    
    # Populate the rest of the trellis
    for l in range(1, sequenceLength):
        for s in range(num_states):
            fTrellis[l][s] = lEmissions[s][sequence[l]] + math.log(sum([math.exp(fTrellis[i][l-1] + lTransitions[i][s]) for i in range(num_states)]))

    # === BACKWARD ALGORITHM ===
    lastItem = sequenceLength - 1

    # Populate last row of trellis
    for s in range(num_states):
        bTrellis[lastItem][s] = 1.0

    # Populate the rest of the trellis
    for l in range(lastItem, 0, -1):
        for s in range(num_states):
            bTrellis[l-1][s] = math.log(sum([math.exp(bTrellis[i][l] + lTransitions[s][i] + lEmissions[i][sequence[l]]) for i in range(num_states)]))
    
    # === OKAY NOW I HAVE TO WORK OUT HOW TO UPDATE ===
