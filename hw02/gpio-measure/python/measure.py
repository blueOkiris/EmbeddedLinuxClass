#!/usr/bin/env python3
import gpiod
import getch
import time
import multiprocessing

## GPIO STUFF HERE
# Define the pin we want to use and its state (on/off)
gpioPinsChip = gpiod.chip('gpiochip1')
gpioPinsLine = gpioPinsChip.get_line(29) # P8_26
gpioPin = (gpioPinsLine, False)

# Initialize gpiod
config = gpiod.line_request()
config.consumer = "Blink"
config.request_type = gpiod.line_request.DIRECTION_OUTPUT
gpioPin[0].request(config)

# Toggle a gpio on or off
def toggleGpio(gpio):
    if gpio[1]:
        gpio[0].set_value(0)
        gpio = (gpio[0], False)
    else:
        gpio[0].set_value(1)
        gpio = (gpio[0], True)
    
    time.sleep(2)

## PROGRAM SETUP STUFF HERE (CAN IGNORE)
# Handle checking for 'q' key (i.e. quit) in separate process
def inputProcess(queue):
    shouldQuit = False
    while not shouldQuit:
        key = getch.getch()
        queue.put(key)
        if key == 'q':
            shouldQuit = True

def main(gpio):
    # Create a separate process for handling input
    inputQueue = multiprocessing.Queue()
    inputProc = multiprocessing.Process(
        target = inputProcess, args = (inputQueue,)
    )
    inputProc.start()

    shouldQuit = False
    while not shouldQuit:
        # THIS IS WHAT WE ACTUALLY CARE ABOUT
        toggleGpio(gpio)

        # Check if time to end 'infinite' loop
        key = ''
        if not inputQueue.empty():
            key = inputQueue.get()
        if key == 'q':
            shouldQuit = True
    
if __name__ == "__main__":
    main(gpioPin)