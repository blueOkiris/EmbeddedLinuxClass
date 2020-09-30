# HW04

## GPIO with MMAP

From the document:

> 1. Write a C or python program that reads from at least two switches and controls two LEDs (the built-in LEDs are fine). The GPIO pins used for the switches need to be from two different GPIO ports. This means you will have to use two separate mmap() calls.
> 
> 2. Write a C or python program that toggles a GPIO port as fast as it can. Measure the speed with an oscilloscope and compare with your previous measurements. Try toggling with no usleep. Is it faster?

1. The program is located in `hw04/mmap/blinkmmap.c`

2. The program is located in `hw04/mmap/togglefast.c`

   The period is 0.29 ms, which is even faster!
