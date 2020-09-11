#include <iostream>
#include <string>
#include <cstring>
#include <GpioLine.hpp>
#include <gpio.h>

using namespace beagleaccess;

void GpioLine::open(GpioChip chip, unsigned int line) {
    auto blankReq = malloc(sizeof(struct gpiohandle_request));
    auto blankData = malloc(sizeof(struct gpiohandle_data));
    memcpy(&_req, blankReq, sizeof(struct gpiohandle_request));
    memcpy(&_data, blankData, sizeof(struct gpiohandle_data));
    free(blankReq);
    free(blankData);

    gpio_open_output_line(&_req, &_data, _chipStr(chip).c_str(), line);
}

void GpioLine::set(unsigned int value) {
    gpio_write_line(&_req, &_data, value);
}

void GpioLine::close() {
    gpio_close_chip(&_req);
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
