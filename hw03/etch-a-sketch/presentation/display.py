import threading
import platform
import os
import time
import smbus
import data.drawable as drawable
import domain.app as app
import presentation.inp as inp

"""
The purpose of this class is to handle the drawing code
Originally it used the cli, but could be repurposed
to draw to other displays.
Functionally, it abstracts a display output
"""
class Display:
    def __init__(self, size, inpHand):
        self._size = size
        self.__grid = []
        for row in range(self._size[1]):
            colStr = ''
            for col in range(self._size[0]):
                colStr += ' '
            self.__grid.append(colStr)
        self._quit = False
        self._inp = inpHand

    """
    Start the main draw loop (main render thread)
    Also start the application update process and key process
    """
    def start(self, application):
        time.sleep(1)
        self._inp.start()
        application.start()

        while not application.hasQuit():
            key = self._inp.getKey()
            application.setKey(key)
            if key == 'q':
                application.quit()
            
            buff = application.getBuffer()
            if buff.shouldUpdate:
                application.handledBuffer()
                self.clear()
                self.copyDrawBuffer(buff)
                self.print()

        self._inp.quit()

    def size(self):
        return self._size

    # Copy the data layer's draw buffer into memory so it can be printed
    def copyDrawBuffer(self, buff):
        for row in range(min(self.size()[1], buff.size()[1])):
            for col in range(min(self.size()[0], buff.size()[0])):
                leftSide = self.__grid[row][0:col]
                rightSide = self.__grid[row][col + 1:]
                if buff.getPoint((col, row)):
                    self.__grid[row] = leftSide + '#' + rightSide
                else:
                    self.__grid[row] = leftSide + ' ' + rightSide
    
    def print(self):
        pass

    def clear(self):
        pass
    
class Matrix8Display(Display):
    def __init__(self, inpHand):
        super().__init__((8, 8), inpHand)

        self._bus = smbus.SMBus(2)
        self._matrixAddr = 0x70

        # Start oscillator, disp on & blink off, and full brightness
        self._bus.write_byte_data(self._matrixAddr, 0x21, 0)
        self._bus.write_byte_data(self._matrixAddr, 0x81, 0)
        self._bus.write_byte_data(self._matrixAddr, 0xE7, 0)

        self.clear()
    
    def print(self):
        drawBytes = []
        for row in range(8):
            # Get on or off
            data = 0x00
            for col in range(8):
                if self._Display__grid[row][col] == '#':
                    data += 0x01 << col
            
            # We'll just set red
            drawBytes.append(data)
            drawBytes.append(0x00)
        self._bus.write_i2c_block_data(self._matrixAddr, 0, drawBytes)

    def clear(self):
        clearBytes = []
        for row in range(8):
            clearBytes.append(0x00)
            clearBytes.append(0x00)
        self._bus.write_i2c_block_data(self._matrixAddr, 0, clearBytes)

class CliDisplay(Display):
    def __init__(self, size, inpHand):
        super().__init__(size, inpHand)
        self._onLinux = platform.system() != 'Windows'
    
    # Handle cross-platform clearing of terminal
    def clear(self):
        if self._onLinux:
            os.system('clear')
        else:
            os.system('cls')
    
    def print(self):
        for row in range(super().size()[1]):
            print(' ' + self._Display__grid[row])
    
