import typing
import multiprocessing
import data.drawable as drawable
import data.queuestate as queuestate

"""
Take application state, and update the draw buffer
However, ONLY do this when the draw buffer HAS BEEN COPIED
"""
def updateApplication(queue):
    shouldQuit = False
    while not shouldQuit:
        appState = queue.get()
        
        if appState.handled:
            appState.buffer = appState.updateFunc(appState.key, appState.buffer)
        shouldQuit = appState.shouldQuit

        queue.put(appState)

# Create an API for talking to the update process
# that generates draw buffers based on the inputted updateFunc
class Application:
    def __init__(self, buffSize, updateFunc):        
        self._queue = multiprocessing.Queue()
        state = queuestate.AppState(buffSize, updateFunc)
        self._queue.put(state)
        self._updateThread = multiprocessing.Process(
            target = updateApplication, args = (self._queue,)
        )
    
    def start(self):
        self._updateThread.start()
        
    def handledBuffer(self):
        state = self._queue.get()
        state.buffer.shouldUpdate = False
        self._queue.put(state)

    def quit(self):
        state = self._queue.get()
        state.shouldQuit = True
        self._queue.put(state)
        self._updateThread.join()

    def setKey(self, key):
        state = self._queue.get()
        state.key = key
        self._queue.put(state)
    
    def hasQuit(self):
        state = self._queue.get()
        quitBool = state.shouldQuit
        self._queue.put(state)
        return quitBool
    
    # Not only gets the buffer, but tells the update loop to get a new buffer
    def getBuffer(self):
        state = self._queue.get()
        state.handled = True
        self._queue.put(state)
        
        return state.buffer
