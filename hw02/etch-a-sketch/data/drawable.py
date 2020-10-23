import typing

"""
This class represents data that can be drawn
to the display.
"""
class DrawBuffer:
    def __init__(self, size):
        self.__buff = []
        self.__size = size
        self.shouldUpdate = False

        # Populate buffer
        for row in range(self.__size[1]):
            colBuf = []
            for col in range(self.__size[0]):
                colBuf.append(False)
            self.__buff.append(colBuf)
        
    def size(self):
        return self.__size
    
    def setPoint(self, point, value):
        self.__buff[point[1]][point[0]] = value
    
    def getPoint(self, point):
        return self.__buff[point[1]][point[0]]
    
    def clear(self):
         for row in range(self.__size[1]):
            for col in range(self.__size[0]):
                self.__buff[row][col] = False
