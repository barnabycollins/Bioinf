import random
from q1b import ExpectationMaximisation as EM
from q2d import TreeNode

TEST_Q1B = False
TEST_Q2D = True

if(TEST_Q1B):
    NUM_STATES = 4

    observations = 'ABCDCBASAKDHASJILDJASOPIDIOKASNBHCHUOALSUIDALSIEOIAJDSAKJDSADASKJDKLSAJDSIOAPUDIOWJKNADBJSIUACJSADBWIUODJASDBASUDOIJASDASFIUSAJFNSABDIASULDHSADJAKSDHAHSFSATYGUFGYDSTG'

    print(EM(observations, NUM_STATES))

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

    print([i.text for i in e.getConstraints()])
    print([i.text for i in f.getConstraints()])

    CHAOTIC_STEFAN = stefan.getConstraints()
    print([i.text for i in CHAOTIC_STEFAN], len(CHAOTIC_STEFAN))
    
    BIG_CHUNGUS = chungus.getConstraints()
    print([i.text for i in BIG_CHUNGUS], len(BIG_CHUNGUS))
