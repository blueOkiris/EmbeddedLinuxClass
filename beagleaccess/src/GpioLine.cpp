#include <iostream>
#include <string>
#include <cstring>
#include <GpioLine.hpp>
#include <gpio.h>

using namespace beagleaccess;

void GpioLine::open(GpioIndex ind, bool isOutput) {
    _isOutput = isOutput;

    auto blankReq = malloc(sizeof(struct gpiohandle_request));
    auto blankData = malloc(sizeof(struct gpiohandle_data));
    memcpy(&_req, blankReq, sizeof(struct gpiohandle_request));
    memcpy(&_data, blankData, sizeof(struct gpiohandle_data));
    free(blankReq);
    free(blankData);

    if(_isOutput) {
        gpio_open_output_line(
            &_req, &_data, chipStr(ind.first).c_str(), ind.second
        );
    } else {
        gpio_open_input_line(
            &_req, &_data, chipStr(ind.first).c_str(), ind.second
        );
    }

    _index = ind;
}

unsigned int GpioLine::get() {
    if(!_isOutput) {
        return gpio_read_line(&_req, &_data);
    } else {
        std::cout
            << "GpioLine at ( " << chipStr(_index.first) << ", "
            << _index.second
            << " ) already initialized as output. Cannot call get.";
        return 0;
    }
}

void GpioLine::set(unsigned int value) {
    if(_isOutput) {
        gpio_write_line(&_req, &_data, value);
    } else {
        std::cout
            << "GpioLine at ( " << chipStr(_index.first) << ", "
            << _index.second
            << " ) already initialized as input. Cannot call set.";
    }
}

void GpioLine::close() {
    gpio_close_chip(&_req);
}

GpioIndex GpioLine::index() {
    return _index;
}

std::string GpioLine::chipStr(const GpioChip &chip) {
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
