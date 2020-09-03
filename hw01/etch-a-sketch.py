#!/usr/bin/env python3

import sys
import etchsketch.tests as tests
import etchsketch.game as game
import etchsketch.cli as cli
import etchsketch.display as display

def main():
    #tests.testBasicApp(sys.argv)
    cliProcessor = cli.CliProcessor(sys.argv)
    if cliProcessor.successful():
        disp = display.Display(cliProcessor.displaySize())
        etchGame = game.Game()

        app = cli.CliApplication()
        app.start(etchGame.update, disp)

if __name__ == '__main__':
    main()