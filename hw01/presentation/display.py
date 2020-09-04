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
    
    # The following handle changing the buffer, either on or off
    def clearPoint(self, point : (int, int)) -> None:
        colStrLeft : str = self.__grid[point[1]][:point[0] - 1]
        colStrRight : str = self.__grid[point[1]][point[0] + 1:]
        self.__grid[point[1]] = colStrLeft + ' ' + colStrRight
    
    def setPoint(self, point : (int, int)) -> None:
        colStrLeft : str = self.__grid[point[1]][:point[0]]
        colStrRight : str = self.__grid[point[1]][point[0] + 1:]
        self.__grid[point[1]] = colStrLeft + '#' + colStrRight
    
    # Resets the buffer
    def clear(self) -> None:
        for row in range(self.__size[1]):
            colStr : str = ''
            for col in range(self.__size[0]):
                colStr += ' '
            self.__grid[row] = colStr
    
    def size(self) -> (int, int):
        return self.__size
    
    def debugInfo(self) -> str:
        return 'Display size: (' + str(self.__size[0]) + ', ' + str(self.__size[1]) + ')'
    
