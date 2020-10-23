import data.drawable as drawable

class AppState:
    def __init__(self, bufferSize, updateFunc):
        self.handled = True
        self.key = ''
        self.buffer = drawable.DrawBuffer(bufferSize)
        self.updateFunc = updateFunc
        self.shouldQuit = False
