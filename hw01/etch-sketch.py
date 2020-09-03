#!/usr/bin/env python3

import sys

from cli import CliProcessor
from display import Display

def main() -> None:
    cliProcessor = CliProcessor(sys.argv)
    if cliProcessor.successful():
        disp = Display(cliProcessor.displaySize())
        testDisplay(disp)

def testDisplay(disp : Display):
    print(disp.output())
    for x in range(min(disp.size()[0], disp.size()[1])):
        disp.setPoint((x, x))
    print(disp.output())
    disp.clear()
    print(disp.output())
    
if __name__ == '__main__':
    main()
