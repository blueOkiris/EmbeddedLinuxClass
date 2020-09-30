#!/bin/bash

echo tmp101 0x48 > /sys/class/i2c-adapter/i2c-2/new_device
MILLIDEG=`cat /sys/class/i2c-adapter/i2c-2/2-0048/hwmon/hwmon0/temp1_input`
SCALE=1000
echo "$((MILLIDEG / SCALE))"
