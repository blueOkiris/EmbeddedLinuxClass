import platform
import os
import threading
import typing
import window.display as display

class CliApplication:
    def __init__(self) -> None:
        self.__onLinux : bool = platform.system() != 'Windows'
        self.__key : str = ''
        self.__quit : bool = False
        self.__inputThread : threading.Thread = threading.Thread(target = self.inputAsync)
    
    def inputAsync(self) -> None:
        while not self.__quit:
            self.__key = self.__readKey()

            if self.__key == 'q':
                self.__quit = True
    
    def start(self, updateFunc, disp : display.Display) -> None:
        self.__quit = False
        self.__inputThread.start()

        while not self.__quit:
            self.__clearCli()
            updateFunc(self.__key, disp)
            disp.print()
            self.__key = ''
        
        self.__inputThread.join()

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
    
    def __clearCli(self):
        if self.__onLinux:
            os.system('clear')
        else:
            os.system('cls')

class CliProcessor:
    def __init__(self, args : typing.List[str]) -> None:
        self.__args : typing.List[str] = args
        self.__displaySize : (int, int) = (8, 8)
        self.__success : bool = True
        
        for arg in self.__args[1:]:
            self.__processArg(arg)
    
    def successful(self) -> bool:
        return self.__success
    
    def displaySize(self) -> (int, int):
        return self.__displaySize
    
    def __processArg(self, arg : str) -> None:
        if arg.startswith('--width='):
            try:
                self.__displaySize = (int(arg[8:]), self.__displaySize[1])
            except:
                print('Failed to parse width argument - ' + arg + '!')
        elif arg.startswith('--height='):
            try:
                self.__displaySize = (self.__displaySize[0], int(arg[9:]))
            except:
                print('Failed to parse height argument - ' + arg + '!')
        elif arg == '--help':
            self.__printHelp()
            self.__success = False
        else:
            print('Unknown option - ' + arg)
            self.__printHelp()
            
            self.__success = False

    def __printHelp(self) -> None:
        print('./etch-sketch.py [OPTIONS]')
        print('Options:')
        print('  --width=#  --> sets the width of the display')
        print('  --height=# --> sets the height of the display')
        print('  --help     --> display this message')
        print('Game control:')
        print('  w, a, s, d --> up, down, left, and right, respectively')
        print('  e          --> reset cursor position and clear')
        print('  q          --> quit the etch-a-sketch program')
