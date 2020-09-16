#!/usr/bin/env python3

import multiprocessing
import getch
import Adafruit_BBIO.GPIO as gpio
import time
import sys

gpioPin = 'P8_12'

class GpioToggler:
    def __init__(self, pin):
        gpio.setup(pin, gpio.OUT)
        self.__pin = (pin, gpio.LOW)
    
    # Toggle a gpio on or off
    def toggleGpio(self, delay):
        gpio.output(self.__pin[0], self.__pin[1])
        if self.__pin[1] == gpio.LOW:
            self.__pin = (self.__pin[0], gpio.HIGH)
        else:
            self.__pin = (self.__pin[0], gpio.LOW)
        
        time.sleep(delay)
    
    def cleanup(self):
        gpio.cleanup()

## PROGRAM SETUP STUFF HERE (CAN IGNORE)
# Handle checking for 'q' key (i.e. quit) in separate process
def inputProcess(queue):
    shouldQuit = False
    while not shouldQuit:
        key = getch.getch()
        queue.put(key)
        if key == 'q':
            shouldQuit = True

def main(pin):
    gpioToggler = GpioToggler(pin)

    # Create a separate process for handling input
    inputQueue = multiprocessing.Queue()
    inputProc = multiprocessing.Process(
        target = inputProcess, args = (inputQueue,)
    )
    inputProc.start()

    shouldQuit = False
    while not shouldQuit:
        # THIS IS WHAT WE ACTUALLY CARE ABOUT
        gpioToggler.toggleGpio(float(sys.argv[1]) / 2)

        # Check if time to end 'infinite' loop
        key = ''
        if not inputQueue.empty():
            key = inputQueue.get()
        if key == 'q':
            shouldQuit = True
    
    gpioToggler.cleanup()
    
if __name__ == "__main__":
    main(gpioPin)