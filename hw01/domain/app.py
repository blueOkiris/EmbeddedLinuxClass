import typing
import multiprocessing
import data.drawable as drawable
import data.queuestate as queuestate

"""
Take application state, and update the draw buffer
However, ONLY do this when the draw buffer HAS BEEN COPIED
"""
def updateApplication(queue : multiprocessing.Queue) -> None:
    shouldQuit : bool = False
    while not shouldQuit:
        appState : queuestate.AppState = queue.get()
        
        if appState.handled:
            appState.buffer = appState.updateFunc(appState.key, appState.buffer)
        shouldQuit = appState.shouldQuit

        queue.put(appState)

# Create an API for talking to the update process that generates draw buffers based on the inputted updateFunc
class Application:
    def __init__(self, buffSize : (int, int), updateFunc) -> None:        
        self.__queue : multiprocessing.Queue = multiprocessing.Queue()
        state : queuestate.AppState = queuestate.AppState(buffSize, updateFunc)
        self.__queue.put(state)
        self.__updateThread : multiprocessing.Process = multiprocessing.Process(target = updateApplication, args = (self.__queue,))
    
    def start(self) -> None:
        self.__updateThread.start()

    def quit(self) -> None:
        state : queuestate.AppState = self.__queue.get()
        state.shouldQuit = True
        self.__queue.put(state)
        self.__updateThread.join()

    def setKey(self, key : str) -> None:
        state : queuestate.AppState = self.__queue.get()
        state.key = key
        self.__queue.put(state)
    
    def hasQuit(self) -> bool:
        state : queuestate.AppState = self.__queue.get()
        quitBool : bool = state.shouldQuit
        self.__queue.put(state)
        return quitBool
    
    # Not only gets the buffer, but tells the update loop to get a new buffer
    def getBuffer(self) -> drawable.DrawBuffer:
        state : queuestate.AppState = self.__queue.get()
        state.handled = True
        self.__queue.put(state)
        
        return state.buffer
