#!/usr/bin/env python3

import sys
import window.app as app
import window.display as display
import etchsketch.game as game
import etchsketch.tests as tests

def main():
    #tests.testBasicApp(sys.argv)
    cliProcessor = app.CliProcessor(sys.argv)
    if cliProcessor.successful():
        disp = display.Display(cliProcessor.displaySize())
        etchGame = game.Game()

        application = app.CliApplication()
        application.start(etchGame.update, disp)

if __name__ == '__main__':
    main()