from typing import List
from platform import system
from os import system as shell
from threading import Thread
from time import sleep

from display import Display

class CliApplication:
    def __init__(self):
        self.__onLinux : bool = system() != 'Windows'
        self.__key : str = ''
        self.__quit : bool = False
        self.__inputThread : Thread = Thread(target = self.inputAsync)
    
    def inputAsync(self):
        while not self.__quit:
            self.__key = self.__readKey()

            if self.__key == 'q':
                self.__quit = True
    
    def start(self, updateFunc, display : Display):
        self.__quit = False
        self.__inputThread.start()

        while not self.__quit:
            self.__clearCli()
            updateFunc(self.__key, display)
        
        self.__inputThread.join()

    def __readKey(self) -> str:
        if self.__onLinux:
            from termios import tcgetattr, tcsetattr, TCSADRAIN
            from tty import setraw
            from sys import stdin

            fd = stdin.fileno()
            old_settings = tcgetattr(fd)
            try:
                setraw(stdin.fileno())
                ch = stdin.read(1)
            finally:
                tcsetattr(fd, TCSADRAIN, old_settings)
            return ch
        else:
            from msvcrt import getch
            return getch()
    
    def __clearCli(self):
        if self.__onLinux:
            shell('clear')
        else:
            shell('cls')

class CliProcessor:
    def __init__(self, args : List[str]) -> None:
        self.__args : List[str] = args
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
        else:
            print('Unknown option - ' + arg)
            self.__printHelp()
            
            self.__success = False

    def __printHelp(self):
        print('./etch-sketch.py [OPTIONS]')
        print('Options:')
        print('  --width=#  --> sets the width of the display')
        print('  --height=# --> sets the height of the display')
        print('  --help=#   --> display this message')
