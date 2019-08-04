import datetime
import moves

fName = "MoveGraph.txt"

wGraph = moves.GetWinMovesGraph()

def PrintGraph():
    global wGraph
    for i in wGraph.keys():
        print(i, " :-> ", wGraph[i])


def WriteWinGraphToFile():
    global wGraph
    now = datetime.datetime.now()
    strNow = now.strftime("%Y-%m-%d %H:%M")
    fileName = strNow + "_" + fName
    print("\nWriting Graph to File: ", fileName)

    # f = open(fileName, 'w')
    f = open(fName, 'w')

    for x in wGraph.keys():
        f.write(str(x) + " | " + str(wGraph[x]) + "\n")
    f.close()