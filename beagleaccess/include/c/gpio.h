#pragma once

#include <linux/gpio.h>

#ifdef __cplusplus
extern "C" {
#endif

void gpio_open_output_line(
    struct gpiohandle_request *req, struct gpiohandle_data *data,
    const char *chip_name, unsigned int line
);
void gpio_write_line(
    struct gpiohandle_request *req, struct gpiohandle_data *data,
    unsigned int value
);
void gpio_close_chip(struct gpiohandle_request *req);

#ifdef __cplusplus
}
#endif