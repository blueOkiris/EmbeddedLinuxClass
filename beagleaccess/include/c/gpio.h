#pragma once

#include <linux/gpio.h>

#ifdef __cplusplus
extern "C" {
#endif

void gpio_open_line(
    struct gpiohandle_request *req, struct gpiohandle_data *data, int flags,
    const char *chip_name, unsigned int line
);
void gpio_write_line(
    struct gpiohandle_request *req, struct gpiohandle_data *data,
    unsigned int value
);
unsigned int gpio_read_line(
    struct gpiohandle_request *req, struct gpiohandle_data *data
);
void gpio_close_chip(struct gpiohandle_request *req);
void clear_gpio_handle_info(
    struct gpiohandle_request *req, struct gpiohandle_data *data
);

#ifdef __cplusplus
}
#endif