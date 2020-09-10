#include <iostream>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <sys/ioctl.h>
#include <linux/gpio.h>
#include <fcntl.h>
#include <unistd.h>
#include <string>
#include <thread>
#include <chrono>
#include <GpioLine.hpp>

using namespace beagleaccess;

// This is mostly C code. maybe wrap in a separate file and link...?
void gpioOpenOutputLine(
        struct gpiohandle_request &req, struct gpiohandle_data &data,
        const char *chipName, unsigned int line) {
    int chipFile, ret;

    chipFile = open(chipName, 0);
    if(chipFile == -1) {
        std::cout << "Failed to open gpiochip #1" << std::endl;
        return;
    }
    
    req.lineoffsets[0] = line;
    req.flags = GPIOHANDLE_REQUEST_OUTPUT;
    memcpy(req.default_values, &data, sizeof(req.default_values));
    strcpy(req.consumer_label, "gpio");
    req.lines = 1;

    ret = ioctl(chipFile, GPIO_GET_LINEHANDLE_IOCTL, &req);
    if(ret == -1) {
        std::cout << "Failed to issue get line handle." << std::endl;
    }

    close(chipFile);
}

// This is mostly C code. maybe wrap in a separate file and link...?
void gpioWriteLine(
        struct gpiohandle_request &req, struct gpiohandle_data &data,
        unsigned int value) {
    data.values[0] = value;
    if(ioctl(req.fd, GPIOHANDLE_SET_LINE_VALUES_IOCTL, &data)) {
        std::cout << "Failed to issue set line." << std::endl;
    }
}

// This is mostly C code. maybe wrap in a separate file and link...?
void gpioCloseChip(struct gpiohandle_request &req) {
    close(req.fd);
}

void GpioLine::open(GpioChip chip, unsigned int line) {
    auto blankReq = malloc(sizeof(struct gpiohandle_request));
    auto blankData = malloc(sizeof(struct gpiohandle_data));
    memcpy(&_req, blankReq, sizeof(struct gpiohandle_request));
    memcpy(&_data, blankData, sizeof(struct gpiohandle_data));
    free(blankReq);
    free(blankData);

    gpioOpenOutputLine(_req, _data, _chipStr(chip).c_str(), line);
}

void GpioLine::set(unsigned int value) {
    gpioWriteLine(_req, _data, value);
}

void GpioLine::close() {
    gpioCloseChip(_req);
}

std::string GpioLine::_chipStr(const GpioChip &chip) {
    switch(chip) {
        case GpioChip::Chip0:
            return "/dev/gpiochip0";
        case GpioChip::Chip1:
            return "/dev/gpiochip1";
        case GpioChip::Chip2:
            return "/dev/gpiochip2";
        case GpioChip::Chip3:
            return "/dev/gpiochip3";
    }
    return "";
}
