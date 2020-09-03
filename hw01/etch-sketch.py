#!/usr/bin/env python3

from sys import argv

from cli import CliProcessor, CliApplication
from display import Display

def main() -> None:
    cliProcessor = CliProcessor(argv)
    if cliProcessor.successful():
        disp = Display(cliProcessor.displaySize())
        app = CliApplication()
        app.start(simpleDraw, disp)

def simpleDraw(key : str, disp : Display):
    disp.clear()
    
    for col in range(disp.size()[0]):
        disp.setPoint((col, 0))
        disp.setPoint((col, disp.size()[1] - 1))
    
    for row in range(disp.size()[1] - 2):
        disp.setPoint((0, row + 1))
        disp.setPoint((disp.size()[0] - 1, row + 1))
    
    disp.print()

"""
def testDisplay(disp : Display):
    disp.print()
    for x in range(min(disp.size()[0], disp.size()[1])):
        disp.setPoint((x, x))
    disp.print()
    disp.clear()
    disp.print()
"""

if __name__ == '__main__':
    main()
