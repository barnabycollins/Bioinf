class Constraint:
    """Class representing a tree constraint such as those used by the BUILD algorithm.
    Stored constraint becomes (a, b) < (c, d) where a, b, c, d are the four arguments provided.
    Access Constraint.text to get the constraint as a human-readable string.
    """

    def __init__(self, a: str, b: str, c: str, d:str):
        self.items = [a, b, c, d]
        self.text = f'({a}, {b}) < ({c}, {d})'


class TreeNode:
    """Class representing a node in a tree. Takes two arguments:
    - children: A list of TreeNodes representing children (provide [] for a leaf)
    - name: The node's name (required for a leaf, optional otherwise)
    """

    def __init__(self, children: list, name: str = ''):
        self.children = children
        self.name = name
        self.isLeaf = children == []
    
    def traverse(self) -> (list, list, list):
        """Returns three values in a tuple:
        - A list of constraints representing the subtree below the current node
        - A 'flattened' list of the named nodes beneath the current node in the tree
            ie, a node with children (a node connected to (a, b), c) would return [a, b, c]
        - A list of pairs of nodes that would need to be linked together by constraints created
            by any parent of the current node
        """

        # Leaves return just themselves
        if (self.isLeaf):
            return ([], [self.name], [])
        
        numChildren = len(self.children)


        # Traverse children
        leaves = []
        internals = []

        childFlatLists = []
        constraintLists = []

        for i in self.children:
            (constraints, flatList, pairsToConnect) = i.traverse()

            if (len(flatList) == 1):
                leaves.append(flatList[0])
            
            else:
                internals.append((constraints, flatList, pairsToConnect))
                childFlatLists.append(flatList)
                constraintLists.append(constraints)

        numLeaves = len(leaves)
        numInternals = len(internals)


        # Generate constraints from data returned by children
        myConstraints = []
        myFlatList = leaves
        myPairsToConnect = []
        childPairsToConnect = []

        # If we're only connected to leaves, just return the flattened list of leaves,
        #   making sure the parent connects them
        if (numInternals == 0):
            return ([], leaves, [(leaves[i], leaves[i+1]) for i in range(numLeaves-1)])

        # If there are multiple internal children, link them all with constraints
        elif (numInternals > 1):
            # As we are connecting two internal children at a time, making one constrant for
            #   each would result in an unnecessary 'loop' - therefore we can omit one
            for i in range(numInternals-1):
                # Use the current internal child's pairsToConnect if available
                if (len(internals[i][2]) > 0):
                    connectingPair = internals[i][2].pop(0)

                else:
                    # Otherwise, just pick two leaves beneath it
                    connectingPair = (internals[i][1][0], internals[i][1][1])
                
                # Generate constraint, adding the right hand side to the list of pairs to connect for any parent
                nextFlatList = internals[i+1][1]
                myConstraints.append(Constraint(connectingPair[0], connectingPair[1], connectingPair[0], nextFlatList[0]))
                myPairsToConnect.append((connectingPair[0], nextFlatList[0]))

                # Add any remaining pairsToConnect from the current internal to a central list
                childPairsToConnect.extend(internals[i][2])
        
        # Add pairsToConnect for any children not covered above
        #   (either a single internal child skipped by the if, or the final one which was not covered by the loop)
        childPairsToConnect.extend(internals[numInternals-1][2])
        
        # Link any leaves to an internal
        # (If we've got this far without returning, we have at least one internal child)
        firstFlatList = internals[0][1]
        for i in leaves:
            # If we still have pairsToConnect from internal children, use those
            if (len(childPairsToConnect) > 0):
                connectingPair = childPairsToConnect.pop(0)
            
            else:
                # Otherwise, just use the first two leaves in the first internal
                connectingPair = firstFlatList
            
            # Generate constraint, adding the right hand side to the list of pairs to connect for any parent
            myConstraints.append(Constraint(connectingPair[0], connectingPair[1], connectingPair[0], i))
            myPairsToConnect.append((connectingPair[0], i))
        
        # If there are any more pairsToConnect from children
        while (len(childPairsToConnect) > 0):
            toConnect = childPairsToConnect.pop(0)

            # If we have any leaves, just connect to the first one
            if (numLeaves != 0):
                toConnectTo = leaves[0]
            
            else:
                # Otherwise, find a pair from any internal that doesn't include the pair we're connecting
                # There will always be at least two children in a valid tree, so
                #   if there are no leaves there will be enough internals
                toConnectTo = next(
                    flatList[0]
                    for flatList in childFlatLists
                    if ((toConnect[0] not in flatList) and (toConnect[1] not in flatList))
                )
            
            # Generate the constraint
            #   (no need to add to myPairsToConnect as the right hand side is superfluous)
            myConstraints.append(Constraint(toConnect[0], toConnect[1], toConnect[0], toConnectTo))
        
        # Prepare output & return
        for i in childFlatLists:
            myFlatList.extend(i)
        
        for i in constraintLists:
            myConstraints.extend(i)

        return (myConstraints, myFlatList, myPairsToConnect)
    
    def getConstraints(self):
        """Returns a list of constraints representing the (sub)tree under the current node
        (Executes traverse() and returns only the constraints)
        """

        return self.traverse()[0]
        

