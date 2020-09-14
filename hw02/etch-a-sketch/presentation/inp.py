import getch
import multiprocessing
import time
import typing
import gpiod

# This just serves to set up and start the input loop (and give it a queue)
class InputHandler:
    def __init__(self, updateFunc) -> None:
        self.__queue : multiprocessing.Queue = multiprocessing.Queue()
        self.__updateThread : multiprocessing.Process = multiprocessing.Process(
            target = updateFunc, args = (self.__queue,)
        )
    
    def getKey(self) -> str:
        if self.__queue.empty():
            return ''
        else:
            return self.__queue.get()
    
    def start(self) -> None:
        self.__updateThread.start()

    def quit(self) -> None:
        self.__updateThread.join()

class PushButtonInputHandler(InputHandler):
    def __init__(self, btns : typing.List[typing.Tuple(str, int)]) -> None:
        super().__init__(PushButtonInputHandler.__pushButtonUpdateInput)
        self.__queue.put(btns)
    
    # Loop in a separate process, adding to the queue when a key is pressed
    @staticmethod
    def __pushButtonUpdateInput(queue : multiprocessing.Queue):
        btnsRaw = queue.get()
        btn = []
        for btnRaw in btnsRaw:
            chip = gpiod.chip(btnRaw[0])
            line = gpiod.get_line(btnRaw[1])

        quit : bool = False
        while not quit:
            key : str = getch.getch()
            queue.put(key)

            if key == 'q':
                quit = True
            time.sleep(0.05)

class CliInputHandler(InputHandler):
    def __init__(self) -> None:
        super().__init__(CliInputHandler.__cliUpdateInput)

    # Loop in a separate process, adding to the queue when a key is pressed
    @staticmethod
    def __cliUpdateInput(queue : multiprocessing.Queue):
        quit : bool = False
        while not quit:
            key : str = getch.getch()
            queue.put(key)

            if key == 'q':
                quit = True
            time.sleep(0.05)
