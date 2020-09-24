import presentation.inp as inp
import presentation.display as display

# This class processes arguments
class CliProcessor:
    def __init__(self, args):
        self._args = args
        self._displaySize = (8, 8)
        self._startPos = (4, 4)
        self._success = True
        self._startPosChanged = (False, False)
        self._inputHandler = 'encoder'
        self._outputHandler = 'matrix'

        for arg in self._args[1:]:
            self._processArg(arg)

        if not self._startPosChanged[0]:
            self._startPos = \
                (int(round(self._displaySize[0] / 2)), self._startPos[1])
        if not self._startPosChanged[1]:
            self._startPos = \
                (self._startPos[0], int(round(self._displaySize[1] / 2)))
    
    def successful(self):
        return self._success
    
    def displaySize(self):
        return self._displaySize
    
    def startPosition(self):
        return self._startPos
    
    def inputHandlerFactory(self):
        if self._inputHandler == 'cli':
            return inp.CliInputHandler()
        elif self._inputHandler == 'pushbtn':
            return inp.PushButtonInputHandler(
                {
                    'q' : ('gpiochip1', 29),
                    'e' : ('gpiochip0', 27),
                    'w' : ('gpiochip1', 17),
                    's' : ('gpiochip3', 19),
                    'a' : ('gpiochip0', 20),
                    'd' : ('gpiochip1', 15)
                }
            )
        elif self._inputHandler == 'encoder':
            return inp.RotaryEncoderInputHandler(
                {
                    'e' : ('gpiochip1', 29), # P8_26
                    'q' : ('gpiochip0', 27) # P8_17
                },
                {
                    'hor' : 1,
                    'vert' : 2
                }
            )
        else:
            return None
    
    def outputHandlerFactory(self):
        if self._outputHandler == 'cli':
            return display.CliDisplay(
                self._displaySize, self.inputHandlerFactory()
            )
        elif self._outputHandler == 'matrix':
            return display.Matrix8Display(self.inputHandlerFactory())
    
    """
    Alter settings if argument is given.
    'Fail' if an unknown command is given
    or if there's a parsing error
    """
    def _processArg(self, arg):
        if arg.startswith('--width='):
            try:
                self._displaySize = (int(arg[8:]), self._displaySize[1])
            except:
                print('Failed to parse width argument - ' + arg + '!')
                self._success = False
        elif arg.startswith('--height='):
            try:
                self._displaySize = (self._displaySize[0], int(arg[9:]))
            except:
                print('Failed to parse height argument - ' + arg + '!')
                self._success = False
        elif arg.startswith('--startx='):
            try:
                self._startPos = (int(arg[9:]), self._startPos[1])
                self._startPosChanged = (True, self._startPosChanged[1])
            except:
                print('Failed to parse start x argument - ' + arg + '!')
                self._success = False
        elif arg.startswith('--starty='):
            try:
                self._startPos = (self._startPos[0], int(arg[9:]))
                self._startPosChanged = (self._startPosChanged[0], True)
            except:
                print('Failed to parse start y argument - ' + arg + '!')
                self._success = False
        elif arg.startswith('--disp='):
            outputType = ''
            try:
                outputType = arg[7:]
            except:
                print('Failed to parse output argument - ' + arg + '!')
                self._success = False
            
            if outputType == 'cli' or outputType == 'matrix':
                self._outputHandler = outputType
            else:
                print('Unexpected output type given: ' + outputType)
                self._success = False
        elif arg.startswith('--input='):
            inputType = ''
            try:
                inputType = arg[8:]
            except:
                print('Failed to parse input argument - ' + arg + '!')
                self._success = False
            
            if inputType == 'cli' or inputType == 'pushbtn' \
            or inputType == 'encoder':
                self._inputHandler = inputType
            else:
                print('Unexpected input type given: ' + inputType)
                self._success = False
        elif arg == '--help':
            self._printHelp()
            self._success = False
        else:
            print('Unknown option - ' + arg)
            self._printHelp()
            
            self._success = False

    # Just the help menu
    def _printHelp(self):
        print('./etch-sketch.py [OPTIONS]')
        print('Options:')
        print(
            '  --width=#                     ' \
            + '--> sets the width of the display'
        )
        print(
            '  --height=#                    ' \
            + '--> sets the height of the display'
        )
        print(
            '  --startx=#                    ' \
            + '--> sets the starting x of the cursor'
        )
        print(
            '  --starty=#                    ' \
            + '--> sets the starting y of the cursor'
        )
        print('  --input=[pushbtn|cli|encoder] --> sets input handler type')
        print('  --disp=[cli|matrix]           --> sets input handler type')
        print('  --help                        --> display this message')
        print('Game control:')
        print('  wasd, dir btns, encoders      --> up, down, left, and right')
        print(
            '  e or yellow btn               ' \
            + '--> reset cursor position and clear'
        )
        print(
            '  q or red btn                  ' \
            + '--> quit the etch-a-sketch program'
        )
