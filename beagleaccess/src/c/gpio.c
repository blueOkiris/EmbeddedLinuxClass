#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ioctl.h>
#include <linux/gpio.h>
#include <fcntl.h>
#include <unistd.h>
#include <gpio.h>

void gpio_open_line(
        struct gpiohandle_request *req, struct gpiohandle_data *data, int flags,
        const char *chip_name, unsigned int line) {
    int chip_file, ret;

    chip_file = open(chip_name, 0);
    if(chip_file == -1) {
        printf("Failed to open gpiochip #1\n");
        return;
    }
    
    req->lineoffsets[0] = line;
    req->flags = flags;
    memcpy(req->default_values, data, sizeof(req->default_values));
    strcpy(req->consumer_label, "gpio");
    req->lines = 1;

    ret = ioctl(chip_file, GPIO_GET_LINEHANDLE_IOCTL, req);
    if(ret == -1) {
       printf("Failed to issue get line handle.\n");
    }

    close(chip_file);
}

unsigned int gpio_read_line(
        struct gpiohandle_request *req, struct gpiohandle_data *data) {
    if(ioctl(req->fd, GPIOHANDLE_GET_LINE_VALUES_IOCTL, data) < 0) {
        printf("Failed to issue get line.\n");
    }
    return data->values[0];
}

void gpio_write_line(
        struct gpiohandle_request *req, struct gpiohandle_data *data,
        unsigned int value) {
    data->values[0] = value;
    if(ioctl(req->fd, GPIOHANDLE_SET_LINE_VALUES_IOCTL, data) < 0) {
        printf("Failed to issue set line.\n");
    }
}

void gpio_close_chip(struct gpiohandle_request *req) {
    close(req->fd);
}

void clear_gpio_handle_info(
        struct gpiohandle_request *req, struct gpiohandle_data *data) {
    struct gpiohandle_request *blankReq = 
        malloc(sizeof(struct gpiohandle_request));
    struct gpiohandle_data *blankData = 
        malloc(sizeof(struct gpiohandle_data));
    memcpy(req, blankReq, sizeof(struct gpiohandle_request));
    memcpy(data, blankData, sizeof(struct gpiohandle_data));
    free(blankReq);
    free(blankData);
}
