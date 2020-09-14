import data.drawable as drawable

class AppState:
    def __init__(self, bufferSize : (int, int), updateFunc):
        self.handled : bool = True
        self.key : str = ''
        self.buffer : drawable.DrawBuffer = drawable.DrawBuffer(bufferSize)
        self.updateFunc = updateFunc
        self.shouldQuit : bool = False
