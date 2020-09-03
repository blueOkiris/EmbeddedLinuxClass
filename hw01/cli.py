from typing import List

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
