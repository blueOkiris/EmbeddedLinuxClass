import threading
import platform
import os
import time
import data.drawable as drawable
import domain.app as app
import presentation.inp as inp

"""
The purpose of this class is to handle the drawing code
Currently it uses the cli, but could be repurposed
to draw to other displays.
Functionally, it abstracts a display output
"""
class CliDisplay:
    def __init__(self, size : (int, int)) -> None:
        self.__onLinux : bool = platform.system() != 'Windows'
        self.__size : (int, int) = size
        self.__grid : typing.List[str] = []
        for row in range(self.__size[1]):
            colStr : str = ''
            for col in range(self.__size[0]):
                colStr += ' '
            self.__grid.append(colStr)
        self.__quit : bool = False
        self.__inp : inp.CliInputHandler = inp.CliInputHandler()
    
    # Handle cross-platform clearing of terminal
    def __clearCli(self) -> None:
        if self.__onLinux:
            os.system('clear')
        else:
            os.system('cls')

    """
    Start the main draw loop (main render thread)
    Also start the application update process and key process
    """
    def start(self, application : app.Application) -> None:
        self.__inp.start()
        application.start()

        while not application.hasQuit():
            key : str = self.__inp.getKey()
            application.setKey(key)
            if key == 'q':
                application.quit()

            self.__clearCli()
            self.copyDrawBuffer(application.getBuffer())
            self.print()
            time.sleep(0.1)

        self.__inp.quit()
    
    def print(self) -> None:
        for row in range(self.__size[1]):
            print(' ' + self.__grid[row])
    
    # Copy the data layer's draw buffer into memory so it can be printed
    def copyDrawBuffer(self, buff : drawable.DrawBuffer) -> None:
        for row in range(min(self.size()[1], buff.size()[1])):
            for col in range(min(self.size()[0], buff.size()[0])):
                leftSide : str = self.__grid[row][0:col]
                rightSide : str = self.__grid[row][col + 1:]
                if buff.getPoint((col, row)):
                    self.__grid[row] = leftSide + '#' + rightSide
                else:
                    self.__grid[row] = leftSide + ' ' + rightSide
    
    def size(self) -> (int, int):
        return self.__size
    
    def debugInfo(self) -> str:
        return 'Display size: (' + str(self.__size[0]) + ', ' + str(self.__size[1]) + ')'
