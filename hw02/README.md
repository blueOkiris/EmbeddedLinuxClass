# HW02 Answers/Turn-in-ables

## Description

There are a few different things that appeared to be required as turn-ins for HW02

This information is repeated in `docs/Answers.md`, but I thought this information should also be front and center.

## Buttons and LEDs

From the hw02 document:

> 3. Write a simple program that reads the switches and lights a corresponding LED. Use interrupts. (callback in Python.)

This program is located in the `hw02/btn2led` folder

## Measuring a gpio pin on an Oscilloscope

Each of the following questions is from the hw02 document:

1. What's the min and max voltage?



2. What period is it?



3. How close is it to 100ms?



4. Why do they differ?



5. Run htop and see how much processor you are using.



6. Try different values for the sleep time (2nd argument). What's the shortest period you can get? Make a table of the values you try and the corresponding period and processor usage. Try using markdown tables: https://www.markdownguide.org/extended-syntax/#tables



7. How stable is the period?



8. Try launching something like vi. How stable is the period?



9. Try cleaning up togglegpio.sh and removing unneeded lines. Does it impact the period?



10. togglegpio uses bash (first line in file). Try using sh. Is the period shorter?



11. What's the shortest period you can get?


### Python

From the doc:

> Write a python script to toggle a gpio pin. Answer the above questions for you Python script. Present the shell script and Python script results in a table for easy comparison.

This program is in the `hw02/gpio-measure/c` python

### C

From the doc:

> Repeat the above using C. Modify togglegpio.c to use lseek() instead of opening and cloing the file. How much faster is it? Add your results to the table.

This program is in the `hw02/gpio-measure/c` folder

## gpiod

Nothing is requested to be turned in for this

## Security

Nothing is requested to be turned in for this

## Etch-a-Sketch

The etch-a-sketch program, modified to use buttons, is located in `hw02/etch-a-sketch`
