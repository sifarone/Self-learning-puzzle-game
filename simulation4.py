import random
import config
import board
import moves
import helper
import fileHelper

import time

"""
board.ResetAll()
board.DisplayBoard()
print(board.GetNumberOfElements())

"""
# Code for simulating Two players playing against each other: START

def makeMove(playerName, playerMoveMap): # TBD to be more intelligent

    print("\n---------------- PLAYER : ", playerName)
    print("Got board as : \n")
    board.DisplayBoard()

    tryAgain = 1
    lvl = -1
    elem = -1

    while(tryAgain):
        lvl = -1
        elem = -1

        lvl, elem = moves.GetBoundaryConditionMove()

        if(lvl != -1): # Boundary condition move found
            tryAgain = 0

        else: # Did not get the Boundary condition Move, play random move
            lvl = helper.GetOneRandomNumberInRangeL1(0, board.LEVELS)
            if (board.GetNumberOfElementsAtLevel(lvl) > 0):
                elementsLeft = board.GetNumberOfElementsAtLevel(lvl)
                elem = helper.GetOneRandomNumberInRangeL1(1, elementsLeft + 1)
                tryAgain = 0

                """
                # Check if the chosen move is present in the LostMoveGraph for this boardState or not
                if (moves.CheckIfMoveIsPresentInLostMovesGraph(board.GetBoardStateAsTuple(), [lvl, elem])):
                    # This move is present in the LostMovesGraph, so don make this move
                    # moves.DeleteCommonMovesFromWinGraph(board.GetBoardStateAsTuple(), [lvl, elem])
                    if(moves.CheckIfMoveIsPresentInBothGraphs(board.GetBoardStateAsTuple(), [lvl,elem])):
                        tryAgain = 0
                    else:
                        print("\n >> This Move is a Loosing Move"," LEVEL : ",lvl," | ELEMENTS : ",elem," trying another move --")
                        tryAgain = 1
                else:
                    tryAgain = 0
                """
            else:
                tryAgain = 1

    if(lvl != -1):

        # Update the player move graph
        playerMoveMap[board.GetBoardStateAsTuple()] = [lvl, elem]
        # Make the changes to the board
        board.RemoveFromBoard(lvl, elem)
        # Update the total number of elements
        board.UpdateTheTotalElementsCount(elem)
        # Valid move made, no need to try again

        print("\nLevel Chosen : ", lvl)
        print("Elements Removed : ", elem)
        print("Resulting Board after the move : \n")
        board.DisplayBoard()


def runSimulatedGame(numberOfGamesToSimulate):

    moves.SetDefaultKeysInWinGraph() # TBD

    for i in range(1, numberOfGamesToSimulate+1):
        print("******************************************Game No: ",i)
        board.ResetAll()

        p1MoveMap = dict()
        p2MoveMap = dict()
        winner = 0

        while (board.GetNumberOfElements() != 0): # Main Loop for one complete game
            print("Element Left on the board : ", board.GetNumberOfElements())

            # Player 1 :------------------------------------------------------
            win = board.CheckForWinOrLooseCondition()
            #print("++ Number of elements : ", board.GetNumberOfElements())
            if(win == 1):
                winner = 1
                break
            elif(win == 0):
                winner = 2
                break
            else:
                # Player 1 Makes the move
                makeMove(1, p1MoveMap)

            # Player 2 :------------------------------------------------------
            win = board.CheckForWinOrLooseCondition()
            #print("-- Number of elements : ",board.GetNumberOfElements())
            if (win == 1):
                winner = 2
                break
            elif (win == 0):
                winner = 1
                break
            else:
                # Player 2 Makes the move
                makeMove(2, p2MoveMap)

        # End of while Loop

        # Update the final Winning move map with the winner moves
        print("================= >>>>>> WINNER = ",winner)
        if(winner == 1):
            moves.UpdateWinMovesGraph(1, p1MoveMap)
            moves.UpdateLostMovesGraph(2, p2MoveMap)
            # For Debug: START
            print("Game #", i, " Over => Winner is Player : ", winner)
            print("Player 1 Moves -> ", p1MoveMap)
            print("Player 2 Moves -> ", p2MoveMap)
            # For Debug: END

        if(winner == 2):
            moves.UpdateWinMovesGraph(2, p2MoveMap)
            moves.UpdateLostMovesGraph(1, p1MoveMap)
            # For Debug: START
            print("Game #", i, " Over => Winner is Player : ", winner)
            print("Player 2 Moves -> ", p2MoveMap)
            print("Player 1 Moves -> ", p1MoveMap)
            # For Debug: END

        # End of for Loop

# Code for simulating Two players playing against each other: END

# Code for Human Vs Computer
def playHumanVsComputer():

    winner = 0
    choice = 1

    ch = input("Play Game Vs Computer (0/1) ? : ")
    choice = int(ch)

    while(choice):
        winner = 0
        board.ResetAll()

        humanMoveMap = dict()  # Player 1
        compMoveMap = dict()  # Player 2
        winner = 0


        print("________________________________________________________________________")

        # print("Win Graph :")
        # moves.PrintWinMovesGraph()
        # print("\nLost Graph :")
        # moves.PrintLostMovesGraph()


        t = input("\nDo you(hooman) want to play first (1/0) ? :  ")
        toss = int(t)

        if(toss == 0): # Computer plays first

            while (board.GetNumberOfElements() != 0):

                # COMPUTER's MOVE:
                print("\n---------------- PLAYER : Computer")

                # check for the boundary and winning conditions here
                win = board.CheckForWinOrLooseCondition()

                if (win == 1): # Computer won the game and one row left
                    print("\nYou LOST Stupid Hooman !! ")
                    winner = 2
                    break

                if (win == 0): # Computer lost the game and one/zero row is left
                    print("\nHooman won the Game !!!")
                    winner = 1
                    break

                if (win == -1): # Usual scenario, more than one rows left in the game
                    # Fetch the next winning move from the WinMovesGraph
                    l, r = moves.NextWinMoveForComputer(board.GetBoardStateAsTuple())
                    if(l != -1): # Next move found in the WinMoveGraph

                        # Update the computer move graph
                        compMoveMap[board.GetBoardStateAsTuple()] = [l, r]

                        # For Debug: START
                        board.DisplayBoard()

                        time.sleep(2)

                        print("\nLevel Chosen --: ", l)
                        print("Elements Removed --: ", r)
                        # For Debug: END

                        # Make the changes to the board
                        board.RemoveFromBoard(l, r)
                        # Update the total number of elements
                        board.UpdateTheTotalElementsCount(r)

                    else: # Next Winning move not found, make a random move
                        print("\n>>>>>>> OOPs :: Computer could not find the Next win move in DB, playing Random move <<<<<<<")

                        time.sleep(2)

                        makeMove("Computer ", compMoveMap)

                # HUMANS's MOVE:

                # TBD: Boundary checks for above inputs
                if(board.GetNumberOfElements() == 1):
                    print("\nYou LOST Stupid Hooman !! \n")
                    winner = 2 # Computer
                    break

                if(board.GetNumberOfElements() == 0):
                    print("\nHooman won the Game !!! \n")
                    winner = 1 # Human
                    break

                #board.DisplayBoard()
                ret = -1
                while(ret == -1):
                    print("\n\n---------------- PLAYER : Human\n")
                    board.DisplayBoard()
                    sl = input("\nLevel ? : ")
                    se = input("elements to remove ? : ")
                    hl = int(sl)
                    he = int(se)
                    ret, msg = moves.VerifyHumanPlayerMove(hl, he)
                    if(ret == -1):
                        print("WRONG SELECTION : ", msg)

                humanMoveMap[board.GetBoardStateAsTuple()] = [hl, he]

                # Make the changes to the board
                board.RemoveFromBoard(hl, he)
                # Update the total number of elements
                board.UpdateTheTotalElementsCount(he)

        # End of Computer Playing first

        if(toss == 1): # Human Plays first

            while (board.GetNumberOfElements() != 0):

                # TBD: Boundary checks for above inputs

                if (board.GetNumberOfElements() == 1):
                    print("\nYou LOST Stupid Hooman !! ")
                    winner = 2  # Computer
                    break

                if (board.GetNumberOfElements() == 0):
                    print("\nHooman won the Game !!!")
                    winner = 1  # Human
                    break

                #board.DisplayBoard()
                ret = -1
                while (ret == -1):
                    print("\n---------------- PLAYER : Human\n")
                    board.DisplayBoard()
                    sl = input("\nLevel ? : ")
                    se = input("elements to remove ? : ")
                    hl = int(sl)
                    he = int(se)
                    ret, msg = moves.VerifyHumanPlayerMove(hl, he)
                    if (ret == -1):
                        print("WRONG SELECTION : ", msg)

                humanMoveMap[board.GetBoardStateAsTuple()] = [hl, he]

                # Make the changes to the board
                board.RemoveFromBoard(hl, he)
                # Update the total number of elements
                board.UpdateTheTotalElementsCount(he)

                # COMPUTER's MOVE:
                print("\n---------------- PLAYER : Computer")
                # check for the boundary and winning conditions here
                win = board.CheckForWinOrLooseCondition()
                if(win == 1):  # Computer won the game and one row left
                    print("\nYou LOST Stupid Hooman !!")
                    winner = 2
                    break

                if(win == 0):  # Computer lost the game and one/zero row is left
                    print("\nHooman won the Game !!!")
                    winner = 1
                    break

                if(win == -1):  # Usual scenario, mre than one rows left in the game
                    # Fetch the next winning move from the WinMovesGraph
                    l, r = moves.NextWinMoveForComputer(board.GetBoardStateAsTuple())
                    if (l != -1):  # Next move found in the WinMoveGraph

                        # Update the computer move graph
                        compMoveMap[board.GetBoardStateAsTuple()] = [l, r]

                        # For Debug: START
                        board.DisplayBoard()

                        time.sleep(2)

                        print("Level Chosen : ", l)
                        print("Elements Removed : ", r)
                        # For Debug: END
                        # For Debug: END

                        # Make the changes to the board
                        board.RemoveFromBoard(l, r)
                        # Update the total number of elements
                        board.UpdateTheTotalElementsCount(r)

                    else:  # Next Winning move not found, make a random move
                        print(">>>>>>> OOPs :: Computer could not find the Next win move in DB, playing Random move <<<<<<<")
                        time.sleep(2)
                        makeMove("Computer ", compMoveMap)

        # End of Human Playing First
        print("\nhumanMoveMap =>> ",humanMoveMap)
        print("compMoveMap  =>> ",compMoveMap)

        # one Game has ended, update the WinMovesGraph if Hooman won the game
        if(winner == 1):
            print("\n------ Updating humanMoveMap in WinMovesGraph | Showing New Update Graph\n")
            moves.UpdateWinMovesGraph(1, humanMoveMap)
            moves.UpdateLostMovesGraph(2,compMoveMap)
            # debug
            #moves.PrintWinMovesGraph()
            print("\n")
        if(winner == 2):
            print("\n------ Updating compMoveMap in WinMovesGraph | Showing New Update Graph\n")
            moves.UpdateWinMovesGraph(2, compMoveMap)
            moves.UpdateLostMovesGraph(1, humanMoveMap)
            # debug
            #moves.PrintWinMovesGraph()
            print("\n")

        print("\n")
        ch = input("Play Another game (0/1) ? : ")
        choice = int(ch)

# MAIN ()
if __name__ == "__main__":

    print("****** STARTING SIMULATION *******")

    nog = input("\nHow many games to simulate : ")
    runSimulatedGame(int(nog))

    # runSimulatedGame(1)
    # print("\n**************************************** SIMULATION OVER *********************************\n")
    # print("               ** Final Win Move Map **  \n")
    # moves.PrintWinMovesGraph()

    #print("\n               ** Final Win Move Map **  \n")
    #moves.PrintLostMovesGraph()

    fileHelper.WriteWinGraphToFile()

    print("\n          ** STARTING MAN Vs MACHINE **\n")
    # Start human vs computer game
    playHumanVsComputer()

    """
    fileHelper.PrintGraph()

    ch = 1
    while(ch == 1):
        moves.getNextWinMoveForABoardPosition()

        c = input("again ? '(0/1) :")
        ch = int(c)
    """

