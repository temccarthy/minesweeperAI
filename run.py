from game import Game
from random import randrange
import selenium
import sys

def Main(difficultyStr, losses, driver):
    gameObj = Game(driver, difficultyStr)

    listL = [(randrange(gameObj.boardObj.boardArray.shape[0]),
              randrange(gameObj.boardObj.boardArray.shape[1]))]
    gameObj.clickAll(listL, [])

    while not gameObj.loss:
        gameObj.addNewDataToArray(listL)

        listL, listR = gameObj.boardObj.flagAndClick()
        if len(listL) == 0 and len(listR) == 0:
            gameObj.boardObj.flagOrClickWithNoMovesLeft(listL)
            print("no moves found, picking random")
        gameObj.clickAll(listL, listR)
        try:
            alert = gameObj.driver.switch_to.alert
            print("you won after "+str(losses)+" losses")
            break
        except selenium.common.exceptions.NoAlertPresentException:  # NoAlertPresentException
            pass
    if gameObj.loss:
        face = gameObj.game.find_element_by_id("face")
        action = selenium.webdriver.common.action_chains.ActionChains(
            gameObj.driver)
        action.click(face)
        action.perform()
        gameObj.loss = False
        print("you've lost "+str(losses+1)+"x")
        losses += 1
        Main(difficultyStr, losses, driver)


if __name__ == "__main__":
    argList = ["beginner","intermediate","expert"]
    driver = selenium.webdriver.Chrome()
    if len(sys.argv)==1:
        Main("intermediate", 0, driver)
    elif sys.argv[1] in argList:
        driver = selenium.webdriver.Chrome()
        Main(sys.argv[1], 0, driver)
    else:
        print("Argument not valid")
        driver.close()
