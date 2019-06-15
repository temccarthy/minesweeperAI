from selenium import webdriver
from board import BoardData
import time
from contextlib import suppress


class Game:

    def __init__(self, driver, difficultyStr):
        boardObj = BoardData(difficultyStr)

        if difficultyStr == "expert":
            difficultyStr = ""
        driver.get("http://minesweeperonline.com/#"+difficultyStr)
        game = self.findGameBoard(driver)

        loss = False

        self.driver = driver
        self.game = game
        self.boardObj = boardObj
        self.loss = loss

    def findGameBoard(self, driver):
        outerContainer = driver.find_element_by_xpath("//td")
        innerContainer = outerContainer.find_element_by_class_name(
            "inner-container")
        centerColumn = innerContainer.find_element_by_id("center-column")
        gameContainer = centerColumn.find_element_by_id("game-container")
        game = gameContainer.find_element_by_id("game")

        return game

    def addNewDataToArray(self, leftClickList):
        start = time.time()
        checkedList = []
        for x in leftClickList:
            self.updateArrayWithNeighbors(x[0], x[1], checkedList)
        print("done adding data recursively, took " +
              str(time.time()-start)+" seconds")

    def updateArrayWithNeighbors(self, i, j, checkedList):

        checkedList.append((i, j))

        value = self.getDataPoint(i, j)
        self.boardObj.boardArray[i][j] = value

        if value == 0:
            if i != 0 and j != 0 and (i-1, j-1) not in checkedList:
                self.updateArrayWithNeighbors(i-1, j-1, checkedList)
            if i != 0:
                if (i-1, j) not in checkedList:
                    self.updateArrayWithNeighbors(i-1, j, checkedList)
                with suppress(IndexError):
                    if (i-1, j+1) not in checkedList:
                        self.updateArrayWithNeighbors(i-1, j+1, checkedList)
            with suppress(IndexError):
                if (i, j+1) not in checkedList:
                    self.updateArrayWithNeighbors(i, j+1, checkedList)
            with suppress(IndexError):
                if (i+1, j+1) not in checkedList:
                    self.updateArrayWithNeighbors(i+1, j+1, checkedList)
            with suppress(IndexError):
                if (i+1, j) not in checkedList:
                    self.updateArrayWithNeighbors(i+1, j, checkedList)
            if j != 0:
                with suppress(IndexError):
                    if (i+1, j-1) not in checkedList:
                        self.updateArrayWithNeighbors(i+1, j-1, checkedList)
                if (i, j-1) not in checkedList:
                    self.updateArrayWithNeighbors(i, j-1, checkedList)

    def getDataPoint(self, i, j):
        square = self.game.find_element_by_id(str(i+1)+"_"+str(j+1))
        squareData = square.get_attribute("class").split(" ")[-1][-1]
        try:
            # flagge"d" -> -2, blan"k" -> -1
            value = {"d": -2, "k": -1}[squareData]
        except KeyError:
            try:
                value = int(squareData)
            except ValueError:
                value = 101
                self.loss = True
        return value

    def clickAll(self, leftClickList, rightClickList):
        actions = webdriver.common.action_chains.ActionChains(self.driver)
        for pair in leftClickList:
            self.clickOnElt(actions, pair[0], pair[1], True)
        for pair in rightClickList:
            if self.boardObj.boardArray[pair[0]][pair[1]] == -1:
                self.clickOnElt(actions, pair[0], pair[1], False)
        try:
            actions.perform()
        except:  # alert error if halfway through clicking
            pass

    def clickOnElt(self, actions, i, j, left):
        squareToClick = self.game.find_element_by_id(str(i+1)+"_"+str(j+1))
        if left:
            actions.click(squareToClick)
        else:
            actions.context_click(squareToClick)
            self.boardObj.boardArray[i][j] = -2
