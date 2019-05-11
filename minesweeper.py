from selenium import webdriver
import numpy as np
import time
from contextlib import suppress
from random import randrange


"""
in array:
-1 = blank
-2 = flagged
-3 = bomb (unused?)
0,1,2... = clicked squares with n bombs around 
"""

#PART 0 (setup)
def setUp(difficultyStr):
    boardSize={"beginner":(9,9), "intermediate":(16,16), "expert":(16,30)}[difficultyStr]
    board=np.full(boardSize,-1)

    driver = webdriver.Chrome()
    
    if difficultyStr=="expert":
        difficultyStr=""
    driver.get("http://minesweeperonline.com/#"+difficultyStr)

    game = findGameBoard(driver)

    return driver,board, game

def findGameBoard(driver):
    outerContainer = driver.find_element_by_xpath("//td")
    innerContainer = outerContainer.find_element_by_class_name("inner-container")
    centerColumn = innerContainer.find_element_by_id("center-column")
    gameContainer = centerColumn.find_element_by_id("game-container")
    game = gameContainer.find_element_by_id("game")
    return game

#PART 1
def addAllDataToArray(game, board):
    start=time.time()
    
    for (i,j), item in np.ndenumerate(board):
        if item ==-1:
            board[i][j] = getDataPoint(game, i, j)
    
    print("done adding data, took " + str(time.time()-start)+" seconds")
    return board

def getDataPoint(game, i, j):
    #square = game.find_element_by_xpath("//div[@id='"+str(i+1)+"_"+str(j+1)+"']")
    square = game.find_element_by_id(str(i+1)+"_"+str(j+1)) #change this to speed up?
    squareData = square.get_attribute("class").split(" ")[-1][-1]
    try:
        value = {"d":-2, "k":-1}[squareData] #flagge"d" -> -2, blan"k" -> -1
    except KeyError:
        value = int(squareData)
    return value



"""
def addAllDataToArray2(game,board,initialA):
    start=time.time()
    a=initialA
    i=1
    j=1
    while True:
        print("checking div["+str(a)+"]")
        square = game.find_element_by_xpath("//div["+str(a)+"]")
        if square.get_attribute("id")==str(i)+"_"+str(j):
            print("found "+str(i)+"_"+str(j))
            board[i-1][j-1]=interpretSquareClass(square)
            j+=1
            if j==board.shape[1]+1:
                j=1
                i+=1
                if i==board.shape[0]+1:
                    break
        a+=1
                

    print("done adding data, took " + str(time.time()-start)+" seconds")
    return board

def interpretSquareClass(square):
    squareData = square.get_attribute("class").split(" ")[-1][-1]
    try:
        value = {"d":-2, "k":-1}[squareData] #flagge"d" -> -2, blan"k" -> -1
    except KeyError:
        value = int(squareData)
    return value
    

def find1_1Div(game):
    a=1
    while True:
        possibleSquare = game.find_element_by_xpath("//div["+str(a)+"]")
        if possibleSquare.get_attribute("id")=="1_1":
            break
        else:
            a+=1
    return a
"""


#PART 2
def flagOrClick(board):
    start=time.time()
    flagSquareList=[]
    emptySquareList=[]
    
    for (i,j), item in np.ndenumerate(board):
        if item>0:
            neighborList = getBoardNeighbors(board,i,j)
            
            d={-2:0, -1:0}
            for a,b,board[a][b] in neighborList:
                d[board[a][b]]=d.get(board[a][b],0)+1
                
            if d[-1]+d[-2]==item:
                for x in neighborList:
                    if x[2]==-1:
                        flagSquareList.append(x)    

            d={-2:0, -1:0}
            for a,b,board[a][b] in neighborList:
                d[board[a][b]]=d.get(board[a][b],0)+1
                
            if d[-2]==item:
                for x in neighborList:
                    if x[2]==-1:
                        emptySquareList.append(x)
            
    print("done deciding clicks, took " + str(time.time()-start)+" seconds")                    
    return list(set(emptySquareList)), list(set(flagSquareList))
        
def getBoardNeighbors(board,i,j):
    neighborList=[]
    if i!=0 and j!=0:
        neighborList.append((i-1,j-1,board[i-1][j-1]))
    if i!=0:
        neighborList.append((i-1,j,board[i-1][j]))
        with suppress(IndexError):
            neighborList.append((i-1,j+1,board[i-1][j+1]))
    with suppress(IndexError):
        neighborList.append((i,j+1,board[i][j+1]))
    with suppress(IndexError):
        neighborList.append((i+1,j+1,board[i+1][j+1]))
    with suppress(IndexError):
        neighborList.append((i+1,j,board[i+1][j]))
    if j!=0:
        with suppress(IndexError):
            neighborList.append((i+1,j-1,board[i+1][j-1]))
        neighborList.append((i,j-1,board[i][j-1]))
    return neighborList

def flagOrClickWithNoMovesLeft(board, leftClickList):
    i,j = np.where(board==-1)
    rand=randrange(len(i))
    leftClickList.append((i[rand],j[rand]))
    #print(i,j)


#PART 3
def clickAll(game,leftClickList, rightClickList):
    actions = webdriver.common.action_chains.ActionChains(driver)
    for pair in leftClickList:
        clickOnElt(actions,game,pair[0],pair[1],True)
    for pair in rightClickList:
        if board[pair[0]][pair[1]]==-1:
            clickOnElt(actions,game,pair[0],pair[1],False)
    actions.perform()

def clickOnElt(actions,game,i,j,left):
    squareToClick = game.find_element_by_id(str(i+1)+"_"+str(j+1))
    if left:
        actions.click(squareToClick)
    else:
        actions.context_click(squareToClick)
        board[i][j]=-2

#RUN
if __name__ == "__main__":
    driver, board, game = setUp("beginner")
    
    clickAll(game,[(randrange(board.shape[0]+1),randrange(board.shape[1]+1))],[])
    
    while True:
        board = addAllDataToArray(game,board)
        list1, list2 = flagOrClick(board)
        if len(list1)==0 and len(list2)==0:
            flagOrClickWithNoMovesLeft(board, list1)
            print("no moves found, picking random")
        clickAll(game,list1,list2)
        try:
            alert = driver.switch_to.alert
            print("game over!")
            break
        except: #NoAlertPresentException
            pass
    


    
