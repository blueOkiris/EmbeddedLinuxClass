import getch
import multiprocessing
import time
import typing
import gpiod

# This just serves to set up and start the input loop (and give it a queue)
class InputHandler:
    def __init__(self, updateFunc, startingQueueItems = []):
        self.__queue = multiprocessing.Queue()
        for item in startingQueueItems:
            self.__queue.put(item)
        self.__updateThread = multiprocessing.Process(
            target = updateFunc, args = (self.__queue,)
        )
    
    def getKey(self):
        if self.__queue.empty():
            return ''
        else:
            return self.__queue.get()
    
    def start(self):
        self.__updateThread.start()

    def quit(self):
        self.__updateThread.join()

class PushButtonInputHandler(InputHandler):
    def __init__(self, btns):
        super().__init__(
            PushButtonInputHandler.__pushButtonUpdateInput, [ btns ]
        )
    
    # Loop in a separate process, adding to the queue when a key is pressed
    @staticmethod
    def __pushButtonUpdateInput(queue):
        btnsRaw = queue.get()
        btns = {}
        for btnKey in btnsRaw:
            chip = gpiod.chip(btnsRaw[btnKey][0])
            line = chip.get_line(btnsRaw[btnKey][1])

            config = gpiod.line_request()
            config.consumer = "Blink"
            config.request_type = gpiod.line_request.DIRECTION_INPUT
            line.request(config)

            btns[btnKey] = line
        
        quit = False
        hasProcessed = False
        while not quit:
            for btnKey in btns:
                if btns[btnKey].get_value() == 0:
                    queue.put(btnKey)
                    if btnKey == 'q':
                        quit = True
                    time.sleep(0.15)

class CliInputHandler(InputHandler):
    def __init__(self):
        super().__init__(CliInputHandler.__cliUpdateInput)
    
    @staticmethod
    def __cliUpdateInput(queue):
        quit = False
        while not quit:
            key = getch.getch()
            queue.put(key)

            if key == 'q':
                quit = True
            time.sleep(0.05)
