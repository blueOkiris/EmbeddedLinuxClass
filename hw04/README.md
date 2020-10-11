# hw04 grading

| Points      | Description |
| ----------- | ----------- |
|  2 | Memory map 
|  4 | mmap()
|  4 | i2c via Kernel
|  4 | Etch-a-Sketch via flask
|  4 | LCD display
|  1 | Extras
| 19 | **Total**

*My comments are in italics. --may*

*Well done.  Nice use of markdown.*

# HW04

## GPIO with MMAP

From the document:

> 1. Write a C or python program that reads from at least two switches and controls two LEDs (the built-in LEDs are fine). The GPIO pins used for the switches need to be from two different GPIO ports. This means you will have to use two separate mmap() calls.
> 
> 2. Write a C or python program that toggles a GPIO port as fast as it can. Measure the speed with an oscilloscope and compare with your previous measurements. Try toggling with no usleep. Is it faster?

1. The program is located in `hw04/mmap/blinkmmap.c`

2. The program is located in `hw04/mmap/togglefast.c`

   The period is 0.29 ms, which is even faster!

## I2C Kernel Driver

From document:

> Follow the directions at EBC_Exercise_12_I2C to read your TMP101 sensors using the kernel driver. Write a program (bash, python or c) that reads the sensor through the driver.

This program is in `hw04/i2c_kernel/temp101.sh`

## Control LED from Browswer

From document:

> Modify you Etch-a-Sketch to control the LED matrix from a web browser via Flask. Have four buttons on the web page that control up, down, left and right.

The new version is in `hw04/etch-a-sketch/etch-a-sketch.py`

## 2.4" Tft LCD

### Plug in an turn on

Nothing to turn in

### Image of Boris running on my display

![boris](./20200930_172628.jpg)

### Movie

Nothing to turn in

### Text generation

Nothing to turn in

