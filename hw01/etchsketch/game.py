import typing
import window.display as display

class Game:
    def __init__(self, startPos : (int, int)) -> None:
        self.__reset : bool = True
        self.__startPos : (int, int) = startPos
        self.__cursorPos : (int, int) = (0, 0)
        self.__directionPressed : List[bool] = [ False, False, False, False ]
        self.__clearPressed : bool = False
        self.__directionReleased : List[bool] = [ False, False, False, False ]
        self.__clearReleased : bool = False

    def update(self, key : str, disp : display.Display) -> None:   
        if self.__reset:
            disp.clear()
            self.__cursorPos = self.__startPos
            self.__reset = False
            disp.setPoint(self.__cursorPos)
        
        self.__updateKeys(key)
        if self.__directionReleased[0] and self.__cursorPos[1] > 0:
            self.__cursorPos = (self.__cursorPos[0], self.__cursorPos[1] - 1)
            disp.setPoint(self.__cursorPos)
        elif self.__directionReleased[1] and self.__cursorPos[1] < disp.size()[1] - 1:
            self.__cursorPos = (self.__cursorPos[0], self.__cursorPos[1] + 1)
            disp.setPoint(self.__cursorPos)
        
        if self.__directionReleased[2] and self.__cursorPos[0] > 0:
            self.__cursorPos = (self.__cursorPos[0] - 1, self.__cursorPos[1])
            disp.setPoint(self.__cursorPos)
        elif self.__directionReleased[3] and self.__cursorPos[0] < disp.size()[1] - 1:
            self.__cursorPos = (self.__cursorPos[0] + 1, self.__cursorPos[1])
            disp.setPoint(self.__cursorPos)
        
        if self.__clearReleased:
            self.__reset = True
    
    def __updateKeys(self, key : str) -> None:
        self.__directionReleased[0] = self.__directionPressed[0] and key != 'w'
        self.__directionReleased[1] = self.__directionPressed[1] and key != 's'
        self.__directionReleased[2] = self.__directionPressed[2] and key != 'a'
        self.__directionReleased[3] = self.__directionPressed[3] and key != 'd'
        self.__clearReleased = self.__clearPressed and key != 'e'

        self.__directionPressed = [ key == 'w', key == 's', key == 'a', key == 'd']
        self.__clearPressed = key == 'e'