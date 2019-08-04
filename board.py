import config

#Globals
LEVELS = config.Difficulty
BOARD = dict()
ELEMENTS = 0 # Total number of elements on the board


#------------------------------------------------------------------------
def DisplayBoard():
    global LEVELS
    global BOARD
    for x in range(LEVELS -1, -1, -1):
        slots = ((x + 1) * 2) + 1
        elem = BOARD[x]
        empty = slots - elem
        print(x, ":  " + ("1 " * elem) + ("0 " * empty))

#------------------------------------------------------------------------
def ResetAll():
    global LEVELS
    global BOARD
    global ELEMENTS
    # Reset The Board
    for x in range(0, LEVELS):
        BOARD[x] = ((x + 1) * 2) + 1

    # Initialize the total number of elements
    ELEMENTS = 0
    for y in range(0, LEVELS):
        ELEMENTS = ELEMENTS + BOARD[y]

#------------------------------------------------------------------------
def RemoveFromBoard(level, elements):
    global BOARD
    BOARD[level] = BOARD[level] - elements

#------------------------------------------------------------------------
def UpdateTheTotalElementsCount(element):
    global ELEMENTS
    ELEMENTS = ELEMENTS - element

#------------------------------------------------------------------------
def GetNumberOfElementsAtLevel(level):
    global BOARD
    return BOARD[level]

#------------------------------------------------------------------------
def GetNumberOfNonEmptyLevels():
    global LEVELS
    global BOARD
    count = 0
    for x in range(0, LEVELS):
        if (BOARD[x] != 0):
            count = count + 1

    return count

#------------------------------------------------------------------------
def GetNumberOfEmptyLevels():
    global LEVELS
    return (LEVELS - GetNumberOfNonEmptyLevels())

#------------------------------------------------------------------------
def CheckForWinningCondition():
    return 1

#------------------------------------------------------------------------
def GetNumberOfElements():
    global ELEMENTS
    return ELEMENTS

#------------------------------------------------------------------------
def GetBoardStateAsTuple():
    l = []
    for x in range(0, LEVELS):
        l.append(BOARD[x])
    return (tuple(l))

#------------------------------------------------------------------------
def GetFirstNonEmptyLevel():
    for x in range(0, LEVELS):
        if (BOARD[x] != 0):
            return x
    return 0

#------------------------------------------------------------------------
def GetLastTwoNonEmptyLevels():
    lList = []
    for x in range(0, LEVELS):
        if(BOARD[x] != 0):
            lList.append(x)
    if(len(lList) == 2):
        return lList
    return None

#------------------------------------------------------------------------
# The follwoing will be called only when there are 3 non empty levels
# This can be further enhanced, like when two levels have 1 each and the 3rd has > 1 : TBD
def CheckIfAnyTwoLevelsHaveEqualElements():
    l = GetAllTheNonEmptyLevels()
    x = -1
    y = -1
    z = -1

    if (BOARD[l[0]] == BOARD[l[1]]) and (BOARD[l[1]] == BOARD[l[2]]): # if all are equal then remove one random row (z)
        x = l[1]
        y = l[2]
        z = l[0]
        return (x,y,z)

    if (BOARD[l[0]] == BOARD[l[1]]):
        if (BOARD[l[0]] != 1):
            x = l[0]
            y = l[1]
            z = l[2]
            return (x, y, z)

        elif (BOARD[l[0]] == 1 ):
            x = -1  # signifies that we are sending elemebts to be removed as 'y'
            y = BOARD[l[2]] - 1
            z = l[2]
            return (x, y, z)

    if (BOARD[l[0]] == BOARD[l[2]]):
        if (BOARD[l[0]] != 1):
            x = l[0]
            y = l[2]
            z = l[1]
            return (x, y, z)

        elif (BOARD[l[0]] == 1):
            x = -1  # signifies that we are sending elemebts to be removed as 'y'
            y = BOARD[l[1]] - 1
            z = l[1]
            return (x, y, z)

    if (BOARD[l[1]] == BOARD[l[2]]):
        if (BOARD[l[1]] != 1):
            x = l[1]
            y = l[2]
            z = l[0]
            return (x, y, z)

        elif (BOARD[l[1]] == 1):
            x = -1  # signifies that we are sending elemebts to be removed as 'y'
            y = BOARD[l[0]] - 1
            z = l[0]
            return (x, y, z)

    return (x, y, z) # Z, is the row/level which has to be removed

# ------------------------------------------------------------------------
def GetAllTheNonEmptyLevels():
    lList = []
    for x in range(0, LEVELS):
        if(BOARD[x] != 0):
            lList.append(x)
    return lList


#------------------------------------------------------------------------
# Winning and Boundary conditions

def CheckForWinOrLooseCondition():

    if(GetNumberOfElements() == 1):
        return 0  # 0 is form loosing

    elif(GetNumberOfElements() == 0):
        return 1  # 1 is for winning

    else:
        return -1  # Carry on with the game


