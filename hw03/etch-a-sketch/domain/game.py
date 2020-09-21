import typing
import data.drawable as drawable

# Basically a static class that is used to update the actual 'game'
class Game:
    def __init__(self, startPos):
        self.__reset = True
        self.__startPos = startPos
        self.__cursorPos = (0, 0)
        self.__directionPressed = [ False, False, False, False ]
        self.__clearPressed = False
        self.__directionReleased = [ False, False, False, False ]
        self.__clearReleased = False

    def update(self, key, currBuff):
        newBuff = currBuff

        if self.__reset:
            # Clear display, and reset cursor pos
            newBuff.clear()
            self.__cursorPos = self.__startPos
            self.__reset = False
            newBuff.setPoint(self.__cursorPos, True)
            newBuff.shouldUpdate = True
        
        """
        Update the cursor position
        (and draw the next piece of line)
        based on release trigger.
        """
        self.__updateKeys(key)
        if self.__directionReleased[0] and self.__cursorPos[1] > 0:
            self.__cursorPos = (self.__cursorPos[0], self.__cursorPos[1] - 1)
            newBuff.setPoint(self.__cursorPos, True)
            newBuff.shouldUpdate = True
        elif self.__directionReleased[1] \
        and self.__cursorPos[1] < newBuff.size()[1] - 1:
            self.__cursorPos = (self.__cursorPos[0], self.__cursorPos[1] + 1)
            newBuff.setPoint(self.__cursorPos, True)
            newBuff.shouldUpdate = True
        if self.__directionReleased[2] \
        and self.__cursorPos[0] > 0:
            self.__cursorPos = (self.__cursorPos[0] - 1, self.__cursorPos[1])
            newBuff.setPoint(self.__cursorPos, True)
            newBuff.shouldUpdate = True
        elif self.__directionReleased[3] \
        and self.__cursorPos[0] < newBuff.size()[0] - 1:
            self.__cursorPos = (self.__cursorPos[0] + 1, self.__cursorPos[1])
            newBuff.setPoint(self.__cursorPos, True)
            newBuff.shouldUpdate = True
        
        # Similar to above, but with resetting the screen
        if self.__clearReleased:
            self.__reset = True
            newBuff.shouldUpdate = True
        
        return newBuff
    
    """
    We want to receive press & release,
    so basically we check if last loop, a key was pressed,
    and if it's not pressed,
    then now we can handle a 'released' event
    """
    def __updateKeys(self, key):
        self.__directionReleased[0] = self.__directionPressed[0] and key != 'w'
        self.__directionReleased[1] = self.__directionPressed[1] and key != 's'
        self.__directionReleased[2] = self.__directionPressed[2] and key != 'a'
        self.__directionReleased[3] = self.__directionPressed[3] and key != 'd'
        self.__clearReleased = self.__clearPressed and key != 'e'

        self.__directionPressed = [
            key == 'w', key == 's', key == 'a', key == 'd'
        ]
        self.__clearPressed = key == 'e'