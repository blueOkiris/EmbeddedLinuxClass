from typing import List

class Display:
    def __init__(self, size : (int, int)) -> None:
        self.__size : (int, int) = size
        self.__grid : List[str] = []
        for row in range(self.__size[1]):
            colStr : str = ''
            for col in range(self.__size[0]):
                colStr += ' '
            self.__grid.append(colStr)
    
    def output(self) -> str:
        out : str = ''
        for row in range(self.__size[1]):
            out += self.__grid[row]
            out += '\n'
        return out
    
    def clearPoint(self, point : (int, int)) -> None:
        colStrLeft : str = self.__grid[point[1]][:point[0] - 1]
        colStrRight : str = self.__grid[point[1]][point[0] + 1:]
        self.__grid[point[1]] = colStrLeft + ' ' + colStrRight
    
    def setPoint(self, point : (int, int)) -> None:
        colStrLeft : str = self.__grid[point[1]][:point[0]]
        colStrRight : str = self.__grid[point[1]][point[0] + 1:]
        self.__grid[point[1]] = colStrLeft + '#' + colStrRight
    
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
    
