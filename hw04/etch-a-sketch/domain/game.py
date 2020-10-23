import typing
import data.drawable as drawable

# Basically a static class that is used to update the actual 'game'
class Game:
    def __init__(self, startPos):
        self._reset = True
        self._startPos = startPos
        self._cursorPos = (0, 0)
        self._directionPressed = [ False, False, False, False ]
        self._clearPressed = False
        self._directionReleased = [ False, False, False, False ]
        self._clearReleased = False

    def update(self, key, currBuff):
        newBuff = currBuff

        if self._reset:
            # Clear display, and reset cursor pos
            newBuff.clear()
            self._cursorPos = self._startPos
            self._reset = False
            newBuff.setPoint(self._cursorPos, True)
            newBuff.shouldUpdate = True
        
        """
        Update the cursor position
        (and draw the next piece of line)
        based on release trigger.
        """
        self._updateKeys(key)
        if self._directionReleased[0] and self._cursorPos[1] > 0:
            self._cursorPos = (self._cursorPos[0], self._cursorPos[1] - 1)
            newBuff.setPoint(self._cursorPos, True)
            newBuff.shouldUpdate = True
        elif self._directionReleased[1] \
        and self._cursorPos[1] < newBuff.size()[1] - 1:
            self._cursorPos = (self._cursorPos[0], self._cursorPos[1] + 1)
            newBuff.setPoint(self._cursorPos, True)
            newBuff.shouldUpdate = True
        if self._directionReleased[2] \
        and self._cursorPos[0] > 0:
            self._cursorPos = (self._cursorPos[0] - 1, self._cursorPos[1])
            newBuff.setPoint(self._cursorPos, True)
            newBuff.shouldUpdate = True
        elif self._directionReleased[3] \
        and self._cursorPos[0] < newBuff.size()[0] - 1:
            self._cursorPos = (self._cursorPos[0] + 1, self._cursorPos[1])
            newBuff.setPoint(self._cursorPos, True)
            newBuff.shouldUpdate = True
        
        # Similar to above, but with resetting the screen
        if self._clearReleased:
            self._reset = True
            newBuff.shouldUpdate = True
        
        return newBuff
    
    """
    We want to receive press & release,
    so basically we check if last loop, a key was pressed,
    and if it's not pressed,
    then now we can handle a 'released' event
    """
    def _updateKeys(self, key):
        self._directionReleased[0] = self._directionPressed[0] and key != 'w'
        self._directionReleased[1] = self._directionPressed[1] and key != 's'
        self._directionReleased[2] = self._directionPressed[2] and key != 'a'
        self._directionReleased[3] = self._directionPressed[3] and key != 'd'
        self._clearReleased = self._clearPressed and key != 'e'

        self._directionPressed = [
            key == 'w', key == 's', key == 'a', key == 'd'
        ]
        self._clearPressed = key == 'e'