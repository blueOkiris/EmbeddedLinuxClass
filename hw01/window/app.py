import platform
import os
import threading
import typing
import window.display as display

"""
This class creates the main processing loop
It also creates a thread for offloading key presses

In particular, this allows for an application-like system
but in cli
"""
class CliApplication:
    def __init__(self) -> None:
        self.__onLinux : bool = platform.system() != 'Windows'
        self.__key : str = ''
        self.__quit : bool = False
        self.__inputThread : threading.Thread = threading.Thread(target = self.inputAsync)
    
    # The separate thread that constantly receives key presses
    def inputAsync(self) -> None:
        while not self.__quit:
            self.__key = self.__readKey()

            if self.__key == 'q':
                self.__quit = True
    
    # Call the update func every loop with display
    def start(self, updateFunc, disp : display.Display) -> None:
        self.__quit = False
        self.__inputThread.start()

        # Main processing loop
        while not self.__quit:
            self.__clearCli()
            updateFunc(self.__key, disp)
            disp.print()
            self.__key = ''
        
        self.__inputThread.join()

    # Handle cross-platform getch()
    def __readKey(self) -> str:
        if self.__onLinux:
            import termios, tty, sys

            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch
        else:
            import msvcrt
            return msvcrt.getch()
    
    # Handle cross-platform clearing of terminal
    def __clearCli(self):
        if self.__onLinux:
            os.system('clear')
        else:
            os.system('cls')

# This class processes arguments
class CliProcessor:
    def __init__(self, args : typing.List[str]) -> None:
        self.__args : typing.List[str] = args
        self.__displaySize : (int, int) = (8, 8)
        self.__startPos : (int, int) = (4, 4)
        self.__success : bool = True
        self.__startPosChanged : (bool, bool) = (False, False)

        for arg in self.__args[1:]:
            self.__processArg(arg)

        if not self.__startPosChanged[0]:
            self.__startPos = (int(round(self.__displaySize[0] / 2)), self.__startPos[1])
        if not self.__startPosChanged[1]:
            self.__startPos = (self.__startPos[0], int(round(self.__displaySize[1] / 2)))
    
    def successful(self) -> bool:
        return self.__success
    
    def displaySize(self) -> (int, int):
        return self.__displaySize
    
    def startPosition(self) -> (int, int):
        return self.__startPos
    
    """
    Alter settings if argument is given.
    'Fail' if an unknown command is given
    or if there's a parsing error
    """
    def __processArg(self, arg : str) -> None:
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
        elif arg == '--help':
            self.__printHelp()
            self.__success = False
        else:
            print('Unknown option - ' + arg)
            self.__printHelp()
            
            self.__success = False

    # Just the help menu
    def __printHelp(self) -> None:
        print('./etch-sketch.py [OPTIONS]')
        print('Options:')
        print('  --width=#  --> sets the width of the display')
        print('  --height=# --> sets the height of the display')
        print('  --startx=# --> sets the starting x of the cursor')
        print('  --starty=# --> sets the starting y of the cursor')
        print('  --help     --> display this message')
        print('Game control:')
        print('  w, a, s, d --> up, down, left, and right, respectively')
        print('  e          --> reset cursor position and clear')
        print('  q          --> quit the etch-a-sketch program')
