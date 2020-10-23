import typing

"""
This class represents data that can be drawn
to the display.
"""
class DrawBuffer:
    def __init__(self, size):
        self._buff = []
        self._size = size
        self.shouldUpdate = False

        # Populate buffer
        for row in range(self._size[1]):
            colBuf = []
            for col in range(self._size[0]):
                colBuf.append(False)
            self._buff.append(colBuf)
        
    def size(self):
        return self._size
    
    def setPoint(self, point, value):
        self._buff[point[1]][point[0]] = value
    
    def getPoint(self, point):
        return self._buff[point[1]][point[0]]
    
    def clear(self):
         for row in range(self._size[1]):
            for col in range(self._size[0]):
                self._buff[row][col] = False
