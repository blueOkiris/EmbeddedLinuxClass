import getch
import multiprocessing
import time
import typing
import gpiod
import os
import Adafruit_BBIO.Encoder

# This just serves to set up and start the input loop (and give it a queue)
class InputHandler:
    def __init__(self, updateFunc, startingQueueItems = []):
        self._queue = multiprocessing.Queue()
        for item in startingQueueItems:
            self._queue.put(item)
        self._updateThread = multiprocessing.Process(
            target = updateFunc, args = (self._queue,)
        )
    
    def getKey(self):
        if self._queue.empty():
            return ''
        else:
            return self._queue.get()
    
    def start(self):
        self._updateThread.start()

    def quit(self):
        self._updateThread.join()

class RotaryEncoderInputHandler(InputHandler):
    def __init__(self, btns, encoders):
        super().__init__(
            RotaryEncoderInputHandler._rotaryEncoderUpdateInput,
            [ btns, encoders ]
        )
    
    @staticmethod
    def _rotaryEncoderUpdateInput(queue):
        btnsRaw = queue.get()
        encodersRaw = queue.get()

        btns = {}
        for btnKey in btnsRaw:
            chip = gpiod.chip(btnsRaw[btnKey][0])
            line = chip.get_line(btnsRaw[btnKey][1])

            config = gpiod.line_request()
            config.consumer = 'Blink'
            config.request_type = gpiod.line_request.DIRECTION_INPUT
            line.request(config)

            btns[btnKey] = line
        
        encoders = {}
        for encoderKey in encodersRaw:
            if encodersRaw[encoderKey] == 1:
                os.system('config-pin P8_33 eqep')
                os.system('config-pin P8_35 eqep')
                encoders[encoderKey] = \
                    [ 
                        Adafruit_BBIO.Encoder.RotaryEncoder(
                            Adafruit_BBIO.Encoder.eQEP1
                        ), 0 
                    ]
            else:
                os.system('config-pin P8_11 eqep')
                os.system('config-pin P8_12 eqep')
                encoders[encoderKey] = \
                    [
                        Adafruit_BBIO.Encoder.RotaryEncoder(
                            Adafruit_BBIO.Encoder.eQEP2
                        ), 0 
                    ]
            encoders[encoderKey][0].setAbsolute()
            encoders[encoderKey][0].enable()
            encoders[encoderKey][1] = encoders[encoderKey][0].position
        
        quit = False
        hasProcessed = False
        while not quit:
            for btnKey in btns:
                if btns[btnKey].get_value() == 0:
                    queue.put(btnKey)
                    if btnKey == 'q':
                        quit = True
                    time.sleep(0.15)
            
            for encoderKey in encoders:
                if encoderKey == 'hor':
                    if encoders[encoderKey][0].position \
                    > encoders[encoderKey][1]:
                        queue.put('d')
                        encoders[encoderKey][1] = \
                            encoders[encoderKey][0].position
                    elif encoders[encoderKey][0].position \
                    < encoders[encoderKey][1]:
                        queue.put('a')
                        encoders[encoderKey][1] = \
                            encoders[encoderKey][0].position
                elif encoderKey == 'vert':
                    if encoders[encoderKey][0].position \
                    > encoders[encoderKey][1]:
                        queue.put('s')
                        encoders[encoderKey][1] = \
                            encoders[encoderKey][0].position
                    elif encoders[encoderKey][0].position \
                    < encoders[encoderKey][1]:
                        queue.put('w')
                        encoders[encoderKey][1] = \
                            encoders[encoderKey][0].position

class PushButtonInputHandler(InputHandler):
    def __init__(self, btns):
        super().__init__(
            PushButtonInputHandler._pushButtonUpdateInput, [ btns ]
        )
    
    # Loop in a separate process, adding to the queue when a key is pressed
    @staticmethod
    def _pushButtonUpdateInput(queue):
        btnsRaw = queue.get()
        btns = {}
        for btnKey in btnsRaw:
            chip = gpiod.chip(btnsRaw[btnKey][0])
            line = chip.get_line(btnsRaw[btnKey][1])

            config = gpiod.line_request()
            config.consumer = 'Blink'
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
        super().__init__(CliInputHandler._cliUpdateInput)
    
    @staticmethod
    def _cliUpdateInput(queue):
        quit = False
        while not quit:
            key = getch.getch()
            queue.put(key)

            if key == 'q':
                quit = True
            time.sleep(0.05)
