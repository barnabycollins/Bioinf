
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

    lastLikelihood = 0
    likelihood = -1

    while (likelihood != lastLikelihood):
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
        

        # === UPDATE ESTIMATES ===
        # Probabilities of being in each state at each point in the sequence
        gammas = []

        # Probabilities of performing each transition at each point in the sequence
        etas = []

        for l in range(sequenceLength):
            gammas.append([])
            etas.append([])
            for s in range(num_states):
                gammas.append((fTrellis[l][s] + bTrellis[l][s]) - math.log(sum([math.exp(fTrellis[l][i] + bTrellis[l][i]) for i in range(num_states)])))

                if (l != lastItem):
                    etas[l].append([])
                    for t in range(num_states):
                        top = fTrellis[l][s] + lTransitions[s][t] + bTrellis[l+1][t] + lEmissions[t][sequence[l+1]]
                        bottom = math.log(sum([sum([fTrellis[i][j] + lTransitions[i][j] + bTrellis[l+1][j] + lEmissions[j][sequence[l+1]] for j in range(num_states)]) for i in range(num_states)]))
                        etas[l][s].append(top - bottom)
        
        initialDistribution = []
        transitions = []
        emissions = []

        for s in range(num_states):
            initialDistribution.append(math.exp(gammas[0][s]))
            transitions.append([])
            emissions.append([])

            bottom = sum([math.exp(gammas[l][s]) for l in range(sequenceLength-1)])

            for t in range(num_states):
                top = sum([math.exp(etas[l][s][t]) for l in range(sequenceLength-1)])

                transitions[s].append(top / bottom)
            
            for o in range(num_symbols):
                top = sum([int(sequence[l] == o) * math.exp(gammas[l][s]) for l in range(sequenceLength)])

                emissions.append(top / bottom)

        likelihood = sum([math.log(sum([math.exp(emissions[s][sequence[l]]) for s in range(num_states)])) for l in range(sequenceLength)])
    


