#pragma once

#define GPIO1_START_ADDR    0x4804C000
#define GPIO1_END_ADDR      0x4804E000
#define GPIO1_SIZE          (GPIO1_END_ADDR - GPIO1_START_ADDR)

#define GPIO_SETDATAOUT     0x0194
#define GPIO_CLEARDATAOUT   0x0190
#define USR0                (1 << 21)
#define USR1                (1 << 22)
#define USR2                (1 << 23)
#define USR3                (1 << 24)
