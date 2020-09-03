from typing import List

class Display:
    def __init__(self, size : (int, int)) -> None:
        self.__size : (int, int) = size
        self.__grid : List[List[Char]] = [ [' '] * self.__size[0] ] * self.__size[1]
    
    def output(self) -> str:
        out : str = ''
        for row in range(self.__size[1]):
            for col in range(self.__size[0]):
                out += self.__grid[row][col]
            out += '\n'
        return out
    
    def clearPoint(point : (int, int)) -> None:
        self.__grid[point[1]][point[0]]
    
    def setPoint(point : (int, int)) -> None:
        self.__grid[point[1]][point[0]] = '#'
    
    def clear(self) -> None:
        for row in range(self.__size[1]):
            for col in range(self.__size[0]):
                self.__grid[row][col] = ' '
    
    def debugInfo(self) -> str:
        return 'Display size: (' + str(self.__size[0]) + ', ' + str(self.__size[1]) + ')'
    
