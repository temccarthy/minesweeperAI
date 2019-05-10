from selenium import webdriver
import numpy as np
import time
from contextlib import suppress
from collections import Counter

driver = webdriver.Chrome()
driver.get("http://minesweeperonline.com/#intermediate")


board = np.full((16,16),-1)


"""
in array:
-1 = blank
-2 = flagged
-3 = bomb (unused?)
0,1,2... = clicked squares with n bombs around 

"""

#PART 1

def findGameBoard(driver):
    outerContainer = driver.find_element_by_xpath("//td")
    innerContainer = outerContainer.find_element_by_class_name("inner-container")
    centerColumn = innerContainer.find_element_by_id("center-column")
    gameContainer = centerColumn.find_element_by_id("game-container")
    game = gameContainer.find_element_by_id("game")
    return game

def addAllDataToArray(game, board):
    start=time.time()
    for (i,j), item in np.ndenumerate(board):
        if item ==-1:
            board[i][j] = getDataPoint(game, i, j)
    
    print("done adding data, took " + str(time.time()-start)+" seconds")
    return board
    #gets faster over time

def getDataPoint(game, i, j):
    square = game.find_element_by_id(str(i+1)+"_"+str(j+1)) #change this to speed up?
    squareData = square.get_attribute("class").split(" ")[-1][-1]
    try:
        value = {"d":-2, "k":-1}[squareData] #flagge"d" -> -2, blan"k" -> -1
    except KeyError:
        value = int(squareData)
    return value

#addAllDataToArray(game,board)
#print(game.get_attribute("id"))

#PART 2
#takes in array
#will return a list of i,j pairs to be flagged and a list to be clicked
def flagOrClick(board):
    flagSquareList=[]
    emptySquareList=[]
    
    for (i,j), item in np.ndenumerate(board):
        if item>0:
            neighborList = getNeighbors(board,i,j)
            #print(i, j, board[i][j], neighborList)
            d={-2:0, -1:0}
            for a,b,board[a][b] in neighborList:
                d[board[a][b]]=d.get(board[a][b],0)+1
            #print(d)
            #print(str(d[-2])+"=?="+str(item))
            if d[-2]==item:
                for x in neighborList:
                    if x[2]==-1:
                        #print("added" + str(x) + "to left click")
                        emptySquareList.append(x)
            else:
                #print(str(d[-1]+d[-2]) + "=??=" + str(item))
                if d[-1]+d[-2]==item:
                    #print("sum found")
                    for x in neighborList:
                        if x[2]==-1:
                            #print("added" + str(x) + "to right click")
                            flagSquareList.append(x)
            #print("")
    return list(set(emptySquareList)), list(set(flagSquareList))
        
def getNeighbors(board,i,j):
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
        


#PART 3
#takes in the 2 lists, clicks as such

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


game = findGameBoard(driver)
clickAll(game,[(8,8)],[])
#board1 = addAllDataToArray(game,board)
#print(board1)
#list1,list2=flagOrClick(board1)
#clickAll(game,list1,list2)

while True:
    board1 = addAllDataToArray(game,board)
    if np.all(board1!=-1):
        break
    #print(board1)
    list1,list2=flagOrClick(board1)
    clickAll(game,list1,list2)
    
    
"""
1 - get data from website -> array
    - data is stored in HTML
    - navigate thru HTML - get id + class 

2 - do things with data -> square to click on


3 - click on square in website -> new data on site

repeat


"""
#driver.quit()
