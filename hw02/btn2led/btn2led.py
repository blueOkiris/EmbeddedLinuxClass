#!/usr/bin/env python3

import gpiod

def main():
    ## Set up
    """
    Buttons are:
     - Gpiochip 1 Line 17 - Up
     - Gpiochip 3 Line 19 - Down
     - Gpiochip 0 Line 20 - Left
     - Gpiochip 1 Line 15 - Right
     - Gpiochip 1 Line 29 - Stop
    Leds are:
     - Gpiochip 1 Line 21 - USR0
     - Gpiochip 1 Line 22 - USR1
     - Gpiochip 1 Line 23 - USR2
     - Gpiochip 1 Line 24 - USR3
    """
    btnInfos = [
        ('gpiochip1', 17, gpiod.line_request.DIRECTION_INPUT),
        ('gpiochip3', 19, gpiod.line_request.DIRECTION_INPUT),
        ('gpiochip0', 20, gpiod.line_request.DIRECTION_INPUT),
        ('gpiochip1', 15, gpiod.line_request.DIRECTION_INPUT),
        ('gpiochip1', 29, gpiod.line_request.DIRECTION_INPUT)
    ]
    ledInfos = [
        ('gpiochip1', 21, gpiod.line_request.DIRECTION_OUTPUT),
        ('gpiochip1', 22, gpiod.line_request.DIRECTION_OUTPUT),
        ('gpiochip1', 23, gpiod.line_request.DIRECTION_OUTPUT),
        ('gpiochip1', 24, gpiod.line_request.DIRECTION_OUTPUT)
    ]

    # Will store the actual Line objects, not their info
    btnLines = []
    ledLines = []

    # Set up and copy all the pins
    for btnInfo in btnInfos:
        chip = gpiod.chip(btnInfo[0])
        line = chip.get_line(btnInfo[1])
        config = gpiod.line_request()
        config.consumer = 'blink'
        config.request_type = btnInfo[2]
        line.request(config)
        
        btnLines.append(line)
    
    # Repeat for leds
    for ledInfo in ledInfos:
        chip = gpiod.chip(ledInfo[0])
        line = chip.get_line(ledInfo[1])
        config = gpiod.line_request()
        config.consumer = 'blink'
        config.request_type = ledInfo[2]
        line.request(config)
        
        ledLines.append(line)
    
    ## Actually do stuff
    while btnLines[4].get_value():
        for i in range(len(ledLines)):
            ledLines[i].set_value(btnLines[i].get_value())

if __name__ == '__main__':
    main()