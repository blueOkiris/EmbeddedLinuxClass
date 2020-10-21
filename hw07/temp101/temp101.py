import blynklib
import busio
import Adafruit_BBIO.GPIO as GPIO

# Convert raw data to temperature (deg Celsius)
def rawToCelsius(data):
    value = data[0] << 4 | (data[1] >> 4)
    temp = (value & 0x0FFF) / 16.0
    return temp

# Setup the LED
LED = 'USR3'
GPIO.setup(LED, GPIO.OUT)
GPIO.output(LED, 1) 

# Setup the button
button = 'P9_11'
GPIO.setup(button, GPIO.IN)
# print("button: " + str(GPIO.input(button)))

# Set up temp101 sensor
i2c = busio.I2C(board.SCL, board.SDA)
addr = 0x49
rawTemp = bytearray(2)
#i2c.readfrom_into(addr, rawTemp)
#temp = rawToCelsius(rawTemp)

# Get the autherization code (See setup.sh)
BLYNK_AUTH = 'TY24DjD6DOiO7tUavJ7oWwTUZ7Bz8myL'#os.getenv('BLYNK_AUTH')
print('Auth: ' + str(BLYNK_AUTH))

# Initialize Blynk
blynk = blynklib.Blynk(BLYNK_AUTH)

# Register Virtual Pins
# The V* says to response to all virtual pins
@blynk.handle_event('write V*')
def my_write_handler(pin, value):
    print('Current V{} value: {}'.format(pin, value))
    GPIO.output(LED, int(value[0])) 
    
# This calback is called everytime the button changes
# channel is the name of the pin that changed
def pushed(channel):
    # Read the current value of the input
    state = GPIO.input(channel)
    print('Edge detected on channel {}, value={}'.format(channel, state))
    # Write it out
    GPIO.output(LED, state)     # Physical LED
    blynk.virtual_write(10, 255*state)  # Virtual LED: 255 max brightness

# This is a non-blocking event 
GPIO.add_event_detect(button, GPIO.BOTH, callback=pushed) 

while True:
    blynk.run()
