import getch
import multiprocessing
import time
import typing
import gpiod
import os
import signal
import Adafruit_BBIO.Encoder
import flask
import blynklib

# This just serves to set up and start the input loop (and give it a queue)
class InputHandler:
    def __init__(self, updateFunc, startingQueueItems = []):
        self._queue = multiprocessing.Queue()
        for item in startingQueueItems:
            self._queue.put(item)
        self.updateFunc = updateFunc
    
    def getKey(self):
        if self._queue.empty():
            return ''
        else:
            return self._queue.get()
    
    def start(self):
        self._updateThread = multiprocessing.Process(
            target = self.updateFunc, args = (self._queue,)
        )
        self._updateThread.start()

    def quit(self):
        self._updateThread.join()

class BlynkInputHandler(InputHandler):
    def __init__(self, btns, auth):
        super().__init__(BlynkInputHandler._blynkUpdateInput, [ btns, auth ])
    
    @staticmethod
    def _blynkUpdateInput(queue):
        quit = False
        btns = queue.get()
        auth = queue.get()
        
        blynk = blynklib.Blynk(auth)
        
        # Register Virtual Pins
        # The V* says to response to all virtual pins
        @blynk.handle_event('write V*')
        def writeHandler(pin, value):
            print('Current V{} value: {}'.format(pin, value))
            if int(value[0]) != 0:
                queue.put(btns[pin])
                if btns[pin] == 'q':
                    quit = True
        
        while not quit:
            blynk.run()

class WebInputHandler(InputHandler):
    def __init__(self):
        super().__init__(WebInputHandler._webUpdateInput, [])
    
    @staticmethod
    def _webUpdateInput(queue):
        inputApp = flask.Flask(__name__)

        @inputApp.route('/')
        def index():
            templateData = {
                'title' : 'Etch-A-Sketch Input Handler',
                'page_title' : 'Etch-A-Sketch Controller',
                'info' : 
                    'Click the buttons to control the cursor on the screen!'
            }
            return flask.render_template('index.html', **templateData)
        
        @inputApp.route('/input/up')
        def up():
            queue.put('w')
            queue.put('')
            return index()

        @inputApp.route('/input/down')
        def down():
            queue.put('s')
            queue.put('')
            return index()

        @inputApp.route('/input/left')
        def left():
            queue.put('a')
            queue.put('')
            return index()

        @inputApp.route('/input/right')
        def right():
            queue.put('d')
            queue.put('')
            return index()

        @inputApp.route('/input/clear')
        def clear():
            queue.put('e')
            queue.put('')
            queue.put('e')
            queue.put('')
            return index()

        @inputApp.route('/input/quit')
        def shutdown():
            shutdown = flask.request.environ.get('werkzeug.server.shutdown')
            shutdown()
            queue.put('q')
            return 'Shutting down...'
        
        inputApp.run(host = '0.0.0.0', port = 8081, debug = True)

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
