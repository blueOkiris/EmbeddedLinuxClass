import getch
import multiprocessing
import time

class InputHandler:
    def __init__(self) -> None:
        pass

    def getKey(self) -> str:
        return ''
    
    def start(self) -> None:
        pass

    def quit(self) -> None:
        pass

# Loop in a separate process, adding to the queue when a key is pressed
def cliUpdateInput(queue : multiprocessing.Queue):
    quit : bool = False
    while not quit:
        key : str = getch.getch()
        queue.put(key)

        if key == 'q':
            quit = True
        time.sleep(0.005)

# This just serves to set up and start the input loop (and give it a queue)
class CliInputHandler(InputHandler):
    def __init__(self) -> None:
        self.__queue : multiprocessing.Queue = multiprocessing.Queue()
        self.__updateThread : multiprocessing.Process = multiprocessing.Process(target = cliUpdateInput, args = (self.__queue,))
    
    def getKey(self) -> str:
        if self.__queue.empty():
            return ''
        else:
            return self.__queue.get()
    
    def start(self) -> None:
        self.__updateThread.start()

    def quit(self) -> None:
        self.__updateThread.join()