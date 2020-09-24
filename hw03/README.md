# HW 3 Answers

## TMP101

The following instructions are from the hw03 document.

1. Wire up your two TMP101 on the i2c bus so each has a different address. Also wire the ALERT pin to a GPIO port.

   Wired up, the one on the left has ADDR0 attached to VCC, and the other has its ADDR0 to GND which means that their addresses are 0x4A and 0x48, respectively.

2. Use the shell commands to read the temperature of each. Write a shell file to read the temperature and convert it to Fahrenheit. Hint: temp=`i2cget -y 1 0x48` assigns the output of i2cget to the variable temp. Hint 2: temp2=$(($temp *2)) multiplies temp by two.

   My output:

   ```
   debian@beaglebone:~/EmbeddedLinuxClass$ i2cget -y 2 0x48
   0x19
   debian@beaglebone:~/EmbeddedLinuxClass$ i2cget -y 2 0x4a
   0x19
   ```

3. Write a python program to read the temperature of each.

   This program is `hw03/tmp101/gettemps.py`

4. Use the i2cset command to set the temperature limits THIGH and TLOW. Test that they are working.

   The THIGH register is P1 = P0 = 1, and we want to set it to write

   The TLOW is P1 = 1, P0 = 0, and we also want to set it to write

   Each are two bytes wide in the form D[11:4] { D[3:0], 0, 0, 0, 0 }

   A good high temperature is 28 degrees celsisus for where I am doing this. That, in hex, is 28 °C -> 0d28 * 0d16 = 0d448 -> 0x01C0 which becomes 0x1C00

   We can only read back 1 byte using i2cget, but I can write multiple.

   ```
   debian@beaglebone:~/EmbeddedLinuxClass/hw03/temp101/pyth$ i2cset -y 2 0x4A 0x03 0x1C 0x00 i
   debian@beaglebone:~/EmbeddedLinuxClass/hw03/temp101/pyth$ i2cget -y 2 0x4A 0x03
   0x1c
   debian@beaglebone:~/EmbeddedLinuxClass/hw03/temp101/pyth$
   debian@beaglebone:~/EmbeddedLinuxClass/hw03/temp101/pyth$ i2cset -y 2 0x4A 0x03 0x00 0x1C i
   debian@beaglebone:~/EmbeddedLinuxClass/hw03/temp101/pyth$ i2cget -y 2 0x4A 0x03
   0x00
   ```

   So setting works as expected, and of course the first byte we write should be the higher byte, so the 0x1C 0x00 version is the correct one:

   ```
   i2cset -y 2 0x4A 0x03 0x1C 0x00 i
   ```

   Same thing with setting the low, only a good temp for that would be 25 °C -> 0d25 * 0d16 = 0d400 -> 0x0190 which becomes 0x1900

   We send it with:

   ```
   i2cset -y 2 0x4A 0x02 0x19 0x00 i
   ```

5. Write a python program that sets the temperature limits on each TMP101 and waits for an interrupt on the ALERT pin, then pri

   This program is `hw03/tmp101/threshtemps.py`

## TMP006

> You also have a TMP006 i2c sensor in your kit. Wire it up and see what you can do with it.

I decided to port my "threshtemps.py" program over, as it sets the threshold and reads the temp, so it kind of does everything.

This port is `hw03/tmp006/threshtemps.py`

## Etch-a-sketch

> Modify your etch-a-sketch program to use the bicolor LED matrix in your kit. The matrix will work off 3.3V.

The program is `hw03/etch-a-sketch/etch-a-sketch.py`

## Rotary encoders

> Modify your Etch-a-Sketch to use two rotary encoders.

The program is `hw03/etch-a-sketch/etch-a-sketch.py`
