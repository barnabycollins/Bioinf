import random
from q1b import ExpectationMaximisation as EM
from q2d import TreeNode
import sys

TEST_Q1B = True
TEST_Q2D = False

def getStandardDeviation(structure1, structure2):
    if (type(structure1) == list):
        total = 0
        denom = 0
        for i in range(len(structure1)):
            (SD, num) = getStandardDeviation(structure1[i], structure2[i])
            total += SD * num
            denom += num
        
        return (total/denom, denom)
    
    else:
        return (abs(structure1 - structure2), 1)

def sample(distribution):
    
    # normalise
    distSum = sum(distribution)
    distribution = [i / distSum for i in distribution]

    val = random.random()

    for i, x in enumerate(distribution):
        val -= x
        
        if (val < 0):
            return i
    
    return 'bruh'

def HMM(initial, transitions, emissions, sequenceLength):
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+-=_;:,.<>[]`¬!"£$%^&*()\\|~#'

    num_states = len(initial)

    state = sample(initial)
    sequence = letters[sample(emissions[state])]

    for i in range(sequenceLength-1):
        state = sample(transitions[state])
        sequence += letters[sample(emissions[state])]
    
    return sequence


def gen_random_sequence(length, num_symbols = 4):
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+-=_;:,.<>[]`¬!"£$%^&*()\\|~#'

    letters = letters[:num_symbols]

    output = ''

    for i in range(length):
        output += letters[random.randrange(num_symbols)]
    
    return output

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

if(TEST_Q1B):
    NUM_ITERATIONS = 10

    if (NUM_ITERATIONS == 0):
        NUM_STATES = 8

        observations = 'ABCDCBASAKDHASJILDJASOPKAHSDASJKHDASJKDHASJDKHASDJKASHDIAUSDAJSDIASHNDSALIDHNASLIDUHASDUKJASGBDLYIUSAKHDBUADHB JASCHBASJKDCGAIUKJWDHIUADKHSDBUIASCHJBYSAUIDHASLBYDUUHAKLEGDWIUKDJBSAUYKHNSABUCYGISAHDBLSAUYJDHKBWALUDBAUIWDHNSAOIDUHBSAIO;DLHSAGUYCJBKAIUSDHBNASIODUHBASIUDHBSALKDUHASLKDJHAKUWKDBKUAYJHDBYUBASDILAYWGDBILUWAGYBDSAGCIASUBDUAWIHBWIDIOKASNBHCHUOALSUIDALSIEOIAJDSAKJDSADASKJDKLSAJDSIOAPUDIOWJKNADBJSIUACJSADBWIUODJASDBASUDOIJASDASFIUSAJFNSABDIASULDHSADJAKSDHAHSFSATYGUFGYDSTG'

        print(EM(observations, NUM_STATES))
    
    else:
        USE_HMMS = True

        if (not USE_HMMS):
            for i in range(NUM_ITERATIONS):
                NUM_STATES = random.randrange(1, 16)
                observations = gen_random_sequence(random.randrange(1, 400), random.randrange(1, 30))
                
                sys.stdout = sys.__stdout__
                print(f'Beginning run:\nNUM_STATES: {NUM_STATES}\nobservations: {observations}\n')

                f = open(f'randrun{i}.txt', 'w')
                sys.stdout = f

                print(EM(observations, NUM_STATES))

                f.close()
            
        else:
            for i in range(NUM_ITERATIONS):
                NUM_STATES = random.randrange(2, 16)
                NUM_SYMBOLS = random.randrange(2, 32)
                
                initial = generateProbabilityMatrix(1, NUM_STATES)[0]
                transitions = generateProbabilityMatrix(NUM_STATES, NUM_STATES)
                emissions = generateProbabilityMatrix(NUM_STATES, NUM_SYMBOLS)
                sequenceLength = random.randrange(10, 400)

                observations = HMM(initial, transitions, emissions, sequenceLength)
                print(f'Beginning run:\nNUM_STATES: {NUM_STATES}\nobservations: {observations}\n...')

                f = open(f'hmmrun{i}.txt', 'w')
                sys.stdout = f

                results = EM(observations, NUM_STATES)
                print(results)

                """SDs = [getStandardDeviation(initial, results[0]), getStandardDeviation(transitions, results[1]), getStandardDeviation(emissions, results[2])]
                print(SDs)"""

                f.close()
                sys.stdout = sys.__stdout__

                print(f'{results}\n')


if (TEST_Q2D):
    e = TreeNode([
        TreeNode([
            TreeNode([], 'a'),
            TreeNode([], 'b')
        ]),
        TreeNode([], 'c')
    ])

    f = TreeNode([
        TreeNode([], 'd'),
        TreeNode([], 'e'),
        TreeNode([], 'f'),
        TreeNode([
            TreeNode([], 'g'),
            TreeNode([], 'h')
        ]),
        TreeNode([
            TreeNode([
                TreeNode([], 'i'),
                TreeNode([], 'j')
            ]),
            TreeNode([
                TreeNode([], 'k'),
                TreeNode([], 'l')
            ])
        ])
    ])

    stefan = TreeNode([
        TreeNode([
            TreeNode([
                TreeNode([
                    TreeNode([], 'c'),
                    TreeNode([], 'h')
                ]),
                TreeNode([], 'a')
            ]),
            TreeNode([
                TreeNode([
                    TreeNode([], 'j'),
                    TreeNode([], 'n')
                ]),
                TreeNode([], 'l')
            ]),
            TreeNode([
                TreeNode([], 'e'),
                TreeNode([], 'f')
            ])
        ]),
        TreeNode([
            TreeNode([
                TreeNode([], 'd'),
                TreeNode([], 'i')
            ]),
            TreeNode([
                TreeNode([], 'g'),
                TreeNode([], 'b')
            ])
        ]),
        TreeNode([
            TreeNode([], 'k'),
            TreeNode([], 'm')
        ])
    ])

    chungus = TreeNode([
        TreeNode([
            TreeNode([
                TreeNode([], 'a'),
                TreeNode([], 'b'),
                TreeNode([], 'c'),
                TreeNode([], 'd')
            ]),
            TreeNode([], 'e'),
            TreeNode([], 'f'),
            TreeNode([], 'g'),
            TreeNode([
                TreeNode([], 'h'),
                TreeNode([], 'i')
            ])
        ]),
        TreeNode([
            TreeNode([
                TreeNode([
                    TreeNode([], 'j'),
                    TreeNode([
                        TreeNode([], 'k'),
                        TreeNode([], 'm')
                    ])
                ]),
                TreeNode([
                    TreeNode([
                        TreeNode([], 'n'),
                        TreeNode([], 'o')
                    ]),
                    TreeNode([
                        TreeNode([], 'p'),
                        TreeNode([], 'q')
                    ])
                ]),
                TreeNode([
                    TreeNode([
                        TreeNode([], 'r'),
                        TreeNode([], 's')
                    ]),
                    TreeNode([
                        TreeNode([], 't'),
                        TreeNode([], 'u')
                    ])
                ]),
                TreeNode([], 'v')
            ]),
            TreeNode([
                TreeNode([
                    TreeNode([], 'w'),
                    TreeNode([], 'x')
                ]),
                TreeNode([], 'y')
            ])
        ]),
        TreeNode([], 'z')
    ])

    saving = TreeNode([
        TreeNode([
            TreeNode([], 'a'),
            TreeNode([], 'b')
        ]),
        TreeNode([
            TreeNode([], 'i'),
            TreeNode([], 'j')
        ]),
        TreeNode([], 's'),
        TreeNode([], 't')
    ])

    print([i.text for i in e.getConstraints()])
    print([i.text for i in f.getConstraints()])

    CHAOTIC_STEFAN = stefan.getConstraints()
    print([i.text for i in CHAOTIC_STEFAN], len(CHAOTIC_STEFAN))
    
    BIG_CHUNGUS = chungus.getConstraints()
    print([i.text for i in BIG_CHUNGUS], len(BIG_CHUNGUS))
    
    LE_SAVING = saving.traverse()
    print([i.text for i in LE_SAVING[0]], len(LE_SAVING))
    print([i for i in LE_SAVING], len(LE_SAVING))
