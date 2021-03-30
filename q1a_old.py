
def ExpectationMaximisation(observations, symbols, transitions, emissions, initialProbabilities):
    observations = [symbols.index(s) for s in observations]

    NUM_STATES = len(transitions)
    
    states = range(NUM_STATES)
    
    # Work out the overall probability of that observation
    # (by summing the probability that it occurred in each possible starting state)
    lTheta = sum([initialProbabilities[s] * emissions[s][observations[0]]  for s in states])

    for i in range(1, len(observations)):
        lTheta *= sum([transitions[s] * emissions[s][observations[i]]  for s in states])
