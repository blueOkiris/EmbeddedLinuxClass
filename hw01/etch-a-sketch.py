#!/usr/bin/env python3

import sys
import presentation.app as app
import presentation.display as display
import domain.game as game

def main():
    # Create a instance of the processor to handle cli args
    cliProcessor = app.CliProcessor(sys.argv)
    
    if cliProcessor.successful():
        disp = display.Display(cliProcessor.displaySize())
        etchGame = game.Game(cliProcessor.startPosition())

        """
        Start the app loop using 
         1) the 'Game' class's update function and 
         2) our created display
        """
        application = app.CliApplication()
        application.start(etchGame.update, disp)

if __name__ == '__main__':
    main()