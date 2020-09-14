import typing

"""
This class represents data that can be drawn
to the display.
"""
class DrawBuffer:
    def __init__(self, size : (int, int)) -> None:
        self.__buff : List[List[bool]] = []
        self.__size : (int, int) = size
        self.shouldUpdate : bool = False

        # Populate buffer
        for row in range(self.__size[1]):
            colBuf : List[bool] = []
            for col in range(self.__size[0]):
                colBuf.append(False)
            self.__buff.append(colBuf)
        
    def size(self) -> (int, int):
        return self.__size
    
    def setPoint(self, point : (int, int), value : bool) -> None:
        self.__buff[point[1]][point[0]] = value
    
    def getPoint(self, point : (int, int)) -> bool:
        return self.__buff[point[1]][point[0]]
    
    def clear(self) -> None:
         for row in range(self.__size[1]):
            for col in range(self.__size[0]):
                self.__buff[row][col] = False
