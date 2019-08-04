from collections import defaultdict
import helper
import board
# START: The Winning Moves Map stuff

WinMovesGraph = defaultdict(set)

# set default key
#WinMovesGraph[(0,0,0,0,0)] = {(0, 0)} #TBD: the key is static for 3 levels, but has to be generic
def SetDefaultKeysInWinGraph():
    defKey = list()
    for x in range(0, board.LEVELS):
        defKey.append(0)
    WinMovesGraph[tuple(defKey)] = {(0,0)}

#WinMovesGraph[(3,5,7)] = {(2,3)}

# Helper functions

# Get boundary condition moves
def GetBoundaryConditionMove():
    l = -1
    e = -1

    if (board.GetNumberOfNonEmptyLevels() == 1):

        if(board.GetNumberOfElementsAtLevel(board.GetFirstNonEmptyLevel()) > 1): # (2), (3), (4), (5)... -> won the game after this move
            l = board.GetFirstNonEmptyLevel()
            e = board.GetNumberOfElementsAtLevel(l) - 1

        elif(board.GetNumberOfElementsAtLevel(board.GetFirstNonEmptyLevel()) == 1): # (1) -> Lost the game
            l = board.GetFirstNonEmptyLevel()
            e = 1

        else: # No next move, Won the game (0)
            l = 0
            e = 0

        print("\nBoundary condition move (l, e) => ", l, "  ", e)

    elif(board.GetNumberOfNonEmptyLevels() == 2):

        lvls = board.GetLastTwoNonEmptyLevels()

        # Both have EQUAL elements
        if( (board.GetNumberOfElementsAtLevel(lvls[0])) == (board.GetNumberOfElementsAtLevel(lvls[1])) ):

            if(board.GetNumberOfElementsAtLevel(lvls[0]) == 1): # (1,1) -> won the game
                l = lvls[0]
                e = 1

            if(board.GetNumberOfElementsAtLevel(lvls[0]) >= 2): # (2,2), (3,3) , (4,4), (5,5), (6,6), (7,7) -> Lost the game
                l = lvls[0]
                e = 1

        else: # Both have NOT EQUAL in the two levels

            # both have > 2 and un equal
            if ((board.GetNumberOfElementsAtLevel(lvls[0]) > 2) and (board.GetNumberOfElementsAtLevel(lvls[1]) > 2)):
                if (board.GetNumberOfElementsAtLevel(lvls[0]) > board.GetNumberOfElementsAtLevel(lvls[1])):
                    l = lvls[0]
                    e = board.GetNumberOfElementsAtLevel(lvls[0]) - board.GetNumberOfElementsAtLevel(lvls[1])
                    tryAgain = 0

                if (board.GetNumberOfElementsAtLevel(lvls[1]) > board.GetNumberOfElementsAtLevel(lvls[0])):
                    l = lvls[1]
                    e = board.GetNumberOfElementsAtLevel(lvls[1]) - board.GetNumberOfElementsAtLevel(lvls[0])
                    tryAgain = 0

            # If l0 have > 2 and the other l1 == 2
            if((board.GetNumberOfElementsAtLevel(lvls[0]) > 2) and (board.GetNumberOfElementsAtLevel(lvls[1]) == 2)):
                l = lvls[0]
                e = board.GetNumberOfElementsAtLevel(lvls[0]) - board.GetNumberOfElementsAtLevel(lvls[1])

            # If l1 have > 2 and the other l0 == 2
            if ((board.GetNumberOfElementsAtLevel(lvls[1]) > 2) and (board.GetNumberOfElementsAtLevel(lvls[0]) == 2)):
                l = lvls[1]
                e = board.GetNumberOfElementsAtLevel(lvls[1]) - board.GetNumberOfElementsAtLevel(lvls[0])


            # If l0 have >= 2 and the other l1 == 1
            if ((board.GetNumberOfElementsAtLevel(lvls[0]) >= 2) and (board.GetNumberOfElementsAtLevel(lvls[1]) == 1)): # (>=2, 1) -> won the game
                l = lvls[0]
                e = board.GetNumberOfElementsAtLevel(lvls[0])

            # If l1 have > 2 and the other l0 == 2
            if ((board.GetNumberOfElementsAtLevel(lvls[1]) >= 2) and (board.GetNumberOfElementsAtLevel(lvls[0]) == 1)): # (1, >= 2) -> won the game
                l = lvls[1]
                e = board.GetNumberOfElementsAtLevel(lvls[1])

        print("\nBoundary condition move (l, e) => ", l, "  ", e)

    elif (board.GetNumberOfNonEmptyLevels() == 3):
        # 1. all levels have equal elements then remove any row completely
        # 2. two have equal
        a, b, c = board.CheckIfAnyTwoLevelsHaveEqualElements()
        if (a != -1):
            l = c
            e = board.GetNumberOfElementsAtLevel(c)
        elif (a == -1):
            l = c
            e = b

    else: # Play random move
        l = -1
        e = -1

    return l, e


# first generate all the permutations of the given key and if any permutation is present in the graph
# then return as ke found
def GetIfAnyKeyPermutationIsPresentInTheGraph(keyTuple, graph):
    permutations = helper.GenerateAllPermutationsOfTheGivenTuple(keyTuple)
    for p in permutations:
        if p in graph.keys():
            return p
    return keyTuple

def UpdateWinMovesGraph(player, playerMoveMap):
    global WinMovesGraph
    for x in playerMoveMap.keys():
        move = playerMoveMap[x]
        # check for permutation of this x(i.e keyTuple)
        # And re adjust the move level according to graph key
        p = GetIfAnyKeyPermutationIsPresentInTheGraph(x, WinMovesGraph)
        playerKeyAsList = list(x)
        graphKeyAsList = list(p)

        graphLevel = graphKeyAsList.index(playerKeyAsList[move[0]])

        newMove = list()
        newMove.append(graphLevel)
        newMove.append(move[1])

        WinMovesGraph[p].add(tuple(newMove))


def NextWinMoveForComputer(boardPosition):
    global WinMovesGraph
    #moveSet = WinMovesGraph[boardPosition] # TBD: Pick the first move from the list for now, later randomize
    # search for all the permutations of the boardPosition in the graph as they are same
    l = -1
    e = -1
    l, e = GetBoundaryConditionMove()

    if (l == -1):
        key = GetIfAnyKeyPermutationIsPresentInTheGraph(boardPosition, WinMovesGraph)
        moveSet = WinMovesGraph.get(key)
        if(moveSet is not None):
            #move = list(moveSet)[0]
            move = list(moveSet)[helper.GetOneRandomNumberInRangeL1(0, len(moveSet))]
            # return move[0], move[1] # level, element to remove

            # Modify/Re-arrange this move to match the actual board position
            keyAsList = list(key) # move is according to this board position
            bpAsList = list(boardPosition)

            newLevel = bpAsList.index(keyAsList[move[0]])

            # Debug
            '''
            print("\n.......... Actual Board Position : ", boardPosition)
            print(".......... Corresponding Key permutation in graph : ", key)
            print(".......... Associated Win Graph Move : ", move[0], " ", move[1])
            print(".......... Adjusted Move for actual board position : ", newLevel, " ", move[1])
            print("\n")
            '''

            return newLevel, move[1]


    return -1, -1 # key not found i.e no winning move corresponding to this board position in the WinMoveGraph

#def NextLooseMoveForComputer(boardPosition):
    # TBD

def PrintWinMovesGraph():
    global WinMovesGraph
    for i in WinMovesGraph.keys():
        print(i, " -> ", WinMovesGraph[i])


# END : The Winning Moves Map stuff

# START: The Loosing Moves Map stuff ----------------------------------------------------------
LostMovesGraph = defaultdict(set)

# Helper Functions
def UpdateLostMovesGraph(player, playerMoveMap):
    global LostMovesGraph
    for x in playerMoveMap.keys():
        # check for permutation of this x(i.e keyTuple)
        p = GetIfAnyKeyPermutationIsPresentInTheGraph(x, LostMovesGraph)
        LostMovesGraph[p].add(tuple(playerMoveMap[x]))

def CheckIfMoveIsPresentInLostMovesGraph(boardPosition, playerMove): # TBD: assuming playerMove is a list (level, element), can be tuple also, CHECK
    global LostMovesGraph
    key = GetIfAnyKeyPermutationIsPresentInTheGraph(boardPosition, LostMovesGraph)
    moveSet = LostMovesGraph.get(key)
    if(moveSet is not None):
        if(tuple(playerMove) in moveSet):
            return 1 # Move is present in LostMovesGraph
        else:
            return 0
    return 0

# TBD: add the permutation based search here
def CheckIfMoveIsPresentInBothGraphs(boardPosition, playerMove):
    global WinMovesGraph
    global LostMovesGraph
    winMoveSet = WinMovesGraph.get(boardPosition)
    lostMoveSet = LostMovesGraph.get(boardPosition)
    if ((winMoveSet is not None) and (lostMoveSet is not None)):
        if((tuple(playerMove) in winMoveSet) and (tuple(playerMove) in lostMoveSet)):
            return 1
    return 0


def PrintLostMovesGraph():
    global LostMovesGraph
    for i in LostMovesGraph.keys():
        print(i, " -> ", LostMovesGraph[i])

# END : The Loosing Moves Map Stuff

def DeleteCommonMovesFromWinGraph(boardPosition, playerMove):
    global WinMovesGraph
    global LostMovesGraph

    wMoveSet = WinMovesGraph.get(boardPosition)
    lMoveSet = LostMovesGraph.get(boardPosition)

    if ((wMoveSet is not None) and (lMoveSet is not None)):
        if( (tuple(playerMove) in wMoveSet ) and (tuple(playerMove) in lMoveSet)):
            #Moves is in both the graph for this board position, remove from WinMoveGraph
            print("Common move : ", tuple(playerMove), " Found in both graph, removing from WinGraph")
            WinMovesGraph[boardPosition].remove(tuple(playerMove))



def VerifyHumanPlayerMove(lvl, elem):
    ret = 1
    msg = ""
    if(lvl >= 0 and (lvl <= board.LEVELS - 1)):
        if((elem > 0) and (elem <= board.GetNumberOfElementsAtLevel(lvl))):
            ret = 1
        else:
            ret = -1
            msg = "Invalid Number of elements chosen"
    else:
        msg = "Invalid Level chosen"
        ret = -1

    return ret, msg

def GetWinMovesGraph():
    global WinMovesGraph
    return WinMovesGraph

def GetLostMovesGraph():
    global LostMovesGraph
    return LostMovesGraph


# ----------------------------- For debugging purposes ------------------------------
def getNextWinMoveForABoardPosition():
    a = input("Level 0 elements ? ")
    b = input("Level 1 elements ? ")
    c = input("Level 2 elements ? ")

    k = list()
    k.append(int(a))
    k.append(int(b))
    k.append(int(c))


    l,e = NextWinMove(tuple(k))
    print("\nNext Move from graph for :::: ",tuple(k), " ....  ", l, " ", e)

def NextWinMove(boardPosition):
    global WinMovesGraph

    l = -1
    e = -1


    if (l == -1):
        key = GetIfAnyKeyPermutationIsPresentInTheGraph(boardPosition, WinMovesGraph)
        moveSet = WinMovesGraph.get(key)
        if(moveSet is not None):
            #move = list(moveSet)[0]
            move = list(moveSet)[helper.GetOneRandomNumberInRangeL1(0, len(moveSet))]
            # return move[0], move[1] # level, element to remove

            # Modify/Re-arrange this move to match the actual board position
            keyAsList = list(key) # move is according to this board position
            bpAsList = list(boardPosition)

            newLevel = bpAsList.index(keyAsList[move[0]])

            # Debug
            print("\n.......... Actual Board Position : ", boardPosition)
            print(".......... Corresponding Key permutation in graph : ", key)
            print(".......... Associated Win Graph Move : ", move[0], " ", move[1])
            print(".......... Adjusted Move for actual board position : ", newLevel, " ", move[1])

            return newLevel, move[1]


    return -1, -1 # key not found i.e no winning move corresponding to this board position in the WinMoveGraph