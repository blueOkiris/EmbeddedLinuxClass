#!/usr/bin/env python3
import board
import busio
import digitalio
import time
import os

# Convert raw data to temperature (deg Celsius)
def rawToCelsius(data):
    value = data[0] << 4 | (data[1] >> 4)
    temp = (value & 0x0FFF) / 16.0
    return temp

# Convert temperature (cels) to raw data
def celsiusToRaw(temp):
    data = bytearray(2)
    data[0] = ((temp * 16) >> 4) & 0xFF
    data[1] = ((temp * 16) << 4) & 0xFF
    return data

# Init everything and call data
def main():
    i2c = busio.I2C(board.SCL, board.SDA)
    print('I2C devices found: ', [ hex(i) for i in i2c.scan() ])

    # Set up data
    leftAddr = 0x4A
    rightAddr = 0x48

    highAddr = bytearray(1)
    lowAddr = bytearray(1)
    reset = bytearray(1)
    highAddr[0] = 0x03
    lowAddr[0] = 0x02
    reset[0] = 0x00

    highThresh = celsiusToRaw(28)
    lowThresh = celsiusToRaw(26)

    # Set the thresholds
    highSetBytes = bytearray(3)
    lowSetBytes = bytearray(3)
    highSetBytes[0] = highAddr[0]
    highSetBytes[1] = highThresh[0]
    highSetBytes[2] = highThresh[1]
    lowSetBytes[0] = lowAddr[0]
    lowSetBytes[1] = lowThresh[0]
    lowSetBytes[2] = lowThresh[1]
    i2c.writeto(leftAddr, highSetBytes)
    i2c.writeto(leftAddr, lowSetBytes)
    i2c.writeto(rightAddr, highSetBytes)
    i2c.writeto(rightAddr, lowSetBytes)

    # Wait for interrupts
    leftAlertPin = digitalio.DigitalInOut(board.P9_12)
    rightAlertPin = digitalio.DigitalInOut(board.P9_30)
    leftAlertPin.direction = digitalio.Direction.INPUT
    rightAlertPin.direction = digitalio.Direction.INPUT

    # Test
    while True:
        os.system('clear')

        rawTemps = [ bytearray(2), bytearray(2) ]
        thresholds = [ bytearray(2), bytearray(2) ]

        i2c.writeto(leftAddr, reset)
        i2c.writeto(rightAddr, reset)
        i2c.readfrom_into(leftAddr, rawTemps[0])
        i2c.readfrom_into(rightAddr, rawTemps[1])
        
        i2c.writeto(leftAddr, highAddr)
        i2c.readfrom_into(leftAddr, thresholds[0])
        i2c.writeto(leftAddr, lowAddr)
        i2c.readfrom_into(leftAddr, thresholds[1])

        print(
            'Left: Temp = ' \
            + str(rawToCelsius(rawTemps[0])) + ', Value: ' \
            + str(leftAlertPin.value)
        )
        print(
            'Right: Tmep = ' \
            + str(rawToCelsius(rawTemps[1])) + ', Value: ' \
            + str(rightAlertPin.value)
        )
        print(
            'Thresh: High = ' + str(rawToCelsius(thresholds[0])) \
            + ', Low = ' + str(rawToCelsius(thresholds[1]))
        )

        time.sleep(0.1)

if __name__ == '__main__':
    main()