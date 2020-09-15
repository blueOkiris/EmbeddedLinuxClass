import typing
import presentation.inp as inp

# This class processes arguments
class CliProcessor:
    def __init__(self, args):
        self.__args = args
        self.__displaySize = (8, 8)
        self.__startPos = (4, 4)
        self.__success = True
        self.__startPosChanged = (False, False)
        self.__inputHandler = 'pushbtn'

        for arg in self.__args[1:]:
            self.__processArg(arg)

        if not self.__startPosChanged[0]:
            self.__startPos = \
                (int(round(self.__displaySize[0] / 2)), self.__startPos[1])
        if not self.__startPosChanged[1]:
            self.__startPos = \
                (self.__startPos[0], int(round(self.__displaySize[1] / 2)))
    
    def successful(self):
        return self.__success
    
    def displaySize(self):
        return self.__displaySize
    
    def startPosition(self):
        return self.__startPos
    
    def inputHandlerFactory(self):
        if self.__inputHandler == 'cli':
            return inp.CliInputHandler()
        elif self.__inputHandler == 'pushbtn':
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
        else:
            return None
    
    """
    Alter settings if argument is given.
    'Fail' if an unknown command is given
    or if there's a parsing error
    """
    def __processArg(self, arg):
        if arg.startswith('--width='):
            try:
                self.__displaySize = (int(arg[8:]), self.__displaySize[1])
            except:
                print('Failed to parse width argument - ' + arg + '!')
                self.__success = False
        elif arg.startswith('--height='):
            try:
                self.__displaySize = (self.__displaySize[0], int(arg[9:]))
            except:
                print('Failed to parse height argument - ' + arg + '!')
                self.__success = False
        elif arg.startswith('--startx='):
            try:
                self.__startPos = (int(arg[9:]), self.__startPos[1])
                self.__startPosChanged = (True, self.__startPosChanged[1])
            except:
                print('Failed to parse start x argument - ' + arg + '!')
                self.__success = False
        elif arg.startswith('--starty='):
            try:
                self.__startPos = (self.__startPos[0], int(arg[9:]))
                self.__startPosChanged = (self.__startPosChanged[0], True)
            except:
                print('Failed to parse start y argument - ' + arg + '!')
                self.__success = False
        elif arg.startswith('--input='):
            inputType = ''
            try:
                inputType = arg[8:]
            except:
                print('Failed to parse input argument - ' + arg + '!')
                self.__success = False
            
            if inputType == 'cli' or inputType == 'pushbtn':
                self.__inputHandler = inputType
            else:
                print('Unexpected input type given: ' + inputType)
                self.__success = False
        elif arg == '--help':
            self.__printHelp()
            self.__success = False
        else:
            print('Unknown option - ' + arg)
            self.__printHelp()
            
            self.__success = False

    # Just the help menu
    def __printHelp(self):
        print('./etch-sketch.py [OPTIONS]')
        print('Options:')
        print('  --width=#             --> sets the width of the display')
        print('  --height=#            --> sets the height of the display')
        print('  --startx=#            --> sets the starting x of the cursor')
        print('  --starty=#            --> sets the starting y of the cursor')
        print('  --input=[pushbtn|cli] --> sets input handler type')
        print('  --help                --> display this message')
        print('Game control:')
        print('  w, a, s, d            --> up, down, left, and right')
        print('  e                     --> reset cursor position and clear')
        print('  q                     --> quit the etch-a-sketch program')
