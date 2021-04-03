class Constraint:
    def __init__(self, a, b, c, d):
        self.items = [a, b, c, d]
        self.text = f'({a}, {b}) < ({c}, {d})'

class TreeNode:
    def __init__(self, children, name=None):
        self.children = children
        self.name = name
        self.isLeaf = children == []
    
    def traverse(self):
        if (self.isLeaf):
            return ([], [self.name], [])
        
        numChildren = len(self.children)

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

        myConstraints = []
        myFlatList = leaves
        myPairsToConnect = []
        childPairsToConnect = []

        # If we're only connected to leaves, just return the list of leaves
        if (numInternals == 0):
            return ([], leaves, [])

        # If there are multiple internals, link them all with constraints
        elif (numInternals > 1):
            for i in range(numInternals):
                if (len(internals[i][2]) > 0):
                    connectingPair = internals[i][2].pop(0)

                else:
                    connectingPair = (internals[i][1][0], internals[i][1][1])
                
                nextFlatList = internals[(i+1)%numInternals][1]
                myConstraints.append(Constraint(connectingPair[0], connectingPair[1], connectingPair[0], nextFlatList[0]))
                myPairsToConnect.append((connectingPair[0], nextFlatList[0]))

                # Add any remaining pairs to connect to the main list to be resolved later
                childPairsToConnect.extend(internals[i][2])
        
        # Link any leaves to internals
        firstFlatList = internals[0][1]
        for i in leaves:
            if (len(childPairsToConnect) > 0):
                connectingPair = childPairsToConnect.pop(0)
            
            else:
                connectingPair = firstFlatList
            
            myConstraints.append(Constraint(connectingPair[0], connectingPair[1], connectingPair[0], i))
            myPairsToConnect.append((connectingPair[0], i))
        
        while (len(childPairsToConnect) > 0):
            toConnect = childPairsToConnect.pop(0)
            if (numLeaves != 0):
                toConnectTo = leaves[0]
            
            else:
                toConnectTo = next(flatList[0] for flatList in childFlatLists if ((toConnect[0] not in flatList) and (toConnect[1] not in flatList)))
            
            myConstraints.append(Constraint(toConnect[0], toConnect[1], toConnect[0], toConnectTo))
        
        for i in childFlatLists:
            myFlatList.extend(i)
        
        for i in constraintLists:
            myConstraints.extend(i)

        return (myConstraints, myFlatList, myPairsToConnect)
    
    def getConstraints(self):
        return self.traverse()[0]
        

