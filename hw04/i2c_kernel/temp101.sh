#!/bin/bash

echo tmp101 0x4A > /sys/class/i2c-adapter/i2c-2/new_device
MILLIDEG=`cat /sys/class/i2c-adapter/i2c-2/2-004a/hwmon/hwmon0/temp1_input`
SCALE=1000
echo "$((MILLIDEG / SCALE))"
