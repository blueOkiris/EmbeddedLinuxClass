#pragma once

#include <linux/gpio.h>
#include <utility>
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

    typedef std::pair<GpioChip, unsigned int> GpioIndex;

    class GpioLine {
        private:
            struct gpiohandle_request _req;
            struct gpiohandle_data _data;
            GpioIndex _index;
            bool _isOutput;

        public:
            static std::string chipStr(const GpioChip &chip);

            void open(GpioIndex ind, bool isOutput);
            void set(unsigned int value);
            unsigned int get();
            void close();
            GpioIndex index();
    };
}
