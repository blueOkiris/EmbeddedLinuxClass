#pragma once

#include <linux/gpio.h>
#include <string>

namespace beagleaccess {
    enum class GpioChip {
        Chip0, Chip1,
        Chip2, Chip3
    };

    static const GpioChip AllChips[4] = {
        GpioChip::Chip0, GpioChip::Chip1,
        GpioChip::Chip2, GpioChip::Chip3
    };

    class GpioLine {
        private:
            struct gpiohandle_request _req;
            struct gpiohandle_data _data;

            static std::string _chipStr(const GpioChip &chip);

        public:
            void open(GpioChip chip, unsigned int line);
            void set(unsigned int value);
            void close();
    };
}
