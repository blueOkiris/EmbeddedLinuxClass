#!/usr/bin/env python3
import board
import busio
import adafruit_tmp006
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

    sensor = adafruit_tmp006.TMP006(i2c)

    # Test
    while True:
        os.system('clear')
        print(sensor.temperature)
        time.sleep(0.1)

if __name__ == '__main__':
    main()