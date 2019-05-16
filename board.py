import numpy as np
import time
from contextlib import suppress
from random import randrange

class BoardData:

    def __init__(self, difficultyStr):
        boardSize={"beginner":(9,9), "intermediate":(16,16), "expert":(16,30)}[difficultyStr]
        boardArray=np.full(boardSize,-1)
        self.boardArray=boardArray

    def flagAndClick(self):
        start=time.time()
        flagSquareList=[]
        emptySquareList=[]

        # iterates through all numerical squares (not -1 or -2) in the array
        for (i,j), item in np.ndenumerate(self.boardArray):
            if item>0:
                neighborList = self.getBoardNeighbors(i,j)

                # creates a dictionary of the values surrounding the square at (i,j)
                d={-2:0, -1:0}
                for a, b,self.boardArray[a][b] in neighborList:
                    d[self.boardArray[a][b]]=d.get(self.boardArray[a][b],0)+1

                # if number of blanks + number of flags == the square's value, plan to
                # right click on the blanks
                if d[-1]+d[-2]==item:
                    for x in neighborList:
                        if x[2]==-1:
                            flagSquareList.append(x)

                # if number of flags == the square's value, plan to left click on the
                # blanks
                if d[-2]==item:
                    for x in neighborList:
                        if x[2]==-1:
                            emptySquareList.append(x)
                
        print("done deciding clicks, took " + str(time.time()-start)+" seconds")
        
        return list(set(emptySquareList)), list(set(flagSquareList))

    def getBoardNeighbors(self, i, j):
        neighborList=[]
        
        if i!=0 and j!=0:
            neighborList.append((i-1,j-1,self.boardArray[i-1][j-1]))
        if i!=0:
            neighborList.append((i-1,j,self.boardArray[i-1][j]))
            with suppress(IndexError):
                neighborList.append((i-1,j+1,self.boardArray[i-1][j+1]))
        with suppress(IndexError):
            neighborList.append((i,j+1,self.boardArray[i][j+1]))
        with suppress(IndexError):
            neighborList.append((i+1,j+1,self.boardArray[i+1][j+1]))
        with suppress(IndexError):
            neighborList.append((i+1,j,self.boardArray[i+1][j]))
        if j!=0:
            with suppress(IndexError):
                neighborList.append((i+1,j-1,self.boardArray[i+1][j-1]))
            neighborList.append((i,j-1,self.boardArray[i][j-1]))
        
        return neighborList

    def flagOrClickWithNoMovesLeft(self, leftClickList):
        i,j = np.where(self.boardArray==-1)
        randArrayValue = randrange(len(i))
        leftClickList.append((i[randArrayValue],j[randArrayValue]))
