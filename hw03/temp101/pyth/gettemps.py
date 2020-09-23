#!/usr/bin/env python3
import board
import busio

# Convert raw data to temperature (deg Celsius)
def rawToCelsius(data):
    value = data[0] << 4 | (data[1] >> 4)
    temp = (value & 0x0FFF) / 16.0
    return temp
    
# Init everything and call data
def main():
    i2c = busio.I2C(board.SCL, board.SDA)
    print('I2C devices found: ', [ hex(i) for i in i2c.scan() ])

    leftAddr = 0x4A
    rightAddr = 0x48

    rawTemps = [ bytearray(2), bytearray(2) ]
    i2c.readfrom_into(leftAddr, rawTemps[0])
    i2c.readfrom_into(rightAddr, rawTemps[1])

    print('Left device temp: ' + str(rawToCelsius(rawTemps[0])) + ' °C')
    print('Right device temp: ' + str(rawToCelsius(rawTemps[1])) + ' °C')

if __name__ == '__main__':
    main()