#!/usr/bin/env python3
import gpiod
import getch
import time
import multiprocessing
import sys

gpioChipName = 'gpiochip1'
gpioLineOffset = 28

class GpioToggler:
    def __init__(self, chipName, line):
        ## GPIO STUFF HERE
        # Define the pin we want to use and its state (on/off)
        gpioPinsChip = gpiod.chip(chipName)
        gpioPinsLine = gpioPinsChip.get_line(line) # P9_12
        self.__gpioPin = (gpioPinsLine, False)

        # Initialize gpiod
        config = gpiod.line_request()
        config.consumer = 'Blink'
        config.request_type = gpiod.line_request.DIRECTION_OUTPUT
        self.__gpioPin[0].request(config)

    # Toggle a gpio on or off
    def toggleGpio(self, period):
        if self.__gpioPin[1]:
            self.__gpioPin[0].set_value(0)
            self.__gpioPin = (self.__gpioPin[0], False)
        else:
            self.__gpioPin[0].set_value(1)
            self.__gpioPin = (self.__gpioPin[0], True)

        time.sleep(period / 2)

## PROGRAM SETUP STUFF HERE (CAN IGNORE)
# Handle checking for 'q' key (i.e. quit) in separate process
def inputProcess(queue):
    shouldQuit = False
    while not shouldQuit:
        key = getch.getch()
        queue.put(key)
        if key == 'q':
            shouldQuit = True

def main(chipName, line):
    gpioToggler = GpioToggler(chipName, line)

    # Create a separate process for handling input
    inputQueue = multiprocessing.Queue()
    inputProc = multiprocessing.Process(
        target = inputProcess, args = (inputQueue,)
    )
    inputProc.start()

    shouldQuit = False
    while not shouldQuit:
        # THIS IS WHAT WE ACTUALLY CARE ABOUT
        gpioToggler.toggleGpio(float(sys.argv[1]))

        # Check if time to end 'infinite' loop
        key = ''
        if not inputQueue.empty():
            key = inputQueue.get()
        if key == 'q':
            shouldQuit = True
    
if __name__ == '__main__':
    main(gpioChipName, gpioLineOffset)