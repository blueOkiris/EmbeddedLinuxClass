#!/usr/bin/env python3

import sys

from cli import CliProcessor
from display import Display

def main() -> None:
    cliProcessor = CliProcessor(sys.argv)
    if cliProcessor.successful():
        disp = Display(cliProcessor.displaySize())
        print(disp.output())
    
if __name__ == '__main__':
    main()
