import data.drawable as drawable

"""
The purpose of this class is to handle the drawing code
Currently it uses the cli, but could be repurposed
to draw to other displays.
Functionally, it abstracts a display buffer and display output
"""
class Display:
    def __init__(self, size : (int, int)) -> None:
        self.__size : (int, int) = size
        self.__grid : typing.List[str] = []
        for row in range(self.__size[1]):
            colStr : str = ''
            for col in range(self.__size[0]):
                colStr += ' '
            self.__grid.append(colStr)
    
    def print(self) -> None:
        for row in range(self.__size[1]):
            print('\r' + self.__grid[row])
    
    def copyDrawBuffer(self, buff : drawable.DrawBuffer):
        for row in range(min(self.size()[1], buff.size()[1])):
            for col in range(min(self.size()[0], buff.size()[0])):
                leftSide : str = self.__grid[row][0:col - 1]
                rightSide : str = self.__grid[row][col + 1:]
                if buff.getPoint((col, row)):
                    self.__grid[row] = leftSide + '#' + rightSide
                else:
                    self.__grid[row] = leftSide + ' ' + rightSide
    
    def size(self) -> (int, int):
        return self.__size
    
    def debugInfo(self) -> str:
        return 'Display size: (' + str(self.__size[0]) + ', ' + str(self.__size[1]) + ')'
    
