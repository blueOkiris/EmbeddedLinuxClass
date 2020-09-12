#include <iostream>
#include <string>
#include <GpioLine.hpp>
#include <gpio.h>

using namespace beagleaccess;

void GpioLine::open(GpioIndex ind, bool isOutput) {
    _isOutput = isOutput;
    _index = ind;
    clear_gpio_handle_info(&_req, &_data);    
    gpio_open_line(
        &_req, &_data, 
        _isOutput ? GPIOHANDLE_REQUEST_OUTPUT : GPIOHANDLE_REQUEST_INPUT, 
        chipStr(ind.first).c_str(), ind.second
    );
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
