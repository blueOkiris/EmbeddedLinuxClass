#!/usr/bin/env python3

import sys
import presentation.argproc as argproc
import presentation.display as display
import domain.app as app
import domain.game as game

def main():
    # Create a instance of the processor to handle cli args
    cliProcessor = argproc.CliProcessor(sys.argv)
    
    if cliProcessor.successful():
        """
        1) Get a reference to the game specific code
        2) Create an application
        3) Create a display
        4) Use the display to start the application and draw loops
        """
        etchGame = game.Game(cliProcessor.startPosition())
        application = app.Application(cliProcessor.displaySize(), etchGame.update)
        disp = display.Display(cliProcessor.displaySize())
        disp.start(application)

if __name__ == '__main__':
    main()