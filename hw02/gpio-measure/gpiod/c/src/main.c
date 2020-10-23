#include <stdio.h>
#include <stdlib.h>
#include <linux/gpio.h>
#include <sys/ioctl.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>

/*
 * While this doesn't call the gpiod library,
 * it does the exact same thing. Literally.
 * 
 * This is recreated based on the gpiod source
 * So in essence it is still the gpiod library,
 * just without direct function calls
 */

// Configured for P8_12
const char *chip_name = "/dev/gpiochip1";
const int line = 28;

int main(int argc, char **args) {
    int period = atoi(args[1]);

    struct gpiohandle_request req;
    struct gpiohandle_data data;
    int chip_file, ret;

    chip_file = open(chip_name, 0);
    if(chip_file == -1) {
        printf("Failed to open gpiochip %s\n", chip_name);
        return - 1;
    }
    
    req.lineoffsets[0] = line;
    req.flags = GPIOHANDLE_REQUEST_OUTPUT;
    memcpy(req.default_values, &data, sizeof(req.default_values));
    strcpy(req.consumer_label, "gpio");
    req.lines = 1;

    ret = ioctl(chip_file, GPIO_GET_LINEHANDLE_IOCTL, &req);
    if(ret == -1) {
       printf("Failed to issue get line handle.\n");
       return -1;
    }

    close(chip_file);

    while(1) {
        data.values[0] = data.values[0] ? 0 : 1;
        if(ioctl(req.fd, GPIOHANDLE_SET_LINE_VALUES_IOCTL, &data) < 0) {
            printf("Failed to issue set line.\n");
        }

        usleep(period / 2);
    }

    close(req.fd);
    return 0;
}
