#pragma once

#define GPIO0_START_ADDR    0x44E07000
#define GPIO1_START_ADDR    0x4804C000
#define GPIO2_START_ADDR    0x481AC000
#define GPIO3_START_ADDR    0x481AE000

#define GPIO_SIZE           0x00000FFF

#define GPIO_SETDATAOUT     0x0194
#define GPIO_CLEARDATAOUT   0x0190
#define GPIO_DATAIN         0x138
#define USR0                (1 << 21)
#define USR1                (1 << 22)
#define USR2                (1 << 23)
#define USR3                (1 << 24)
#define P9_21               (1 << 3)
#define P9_23               (1 << 17)
