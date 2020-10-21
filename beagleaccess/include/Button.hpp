#pragma once

#include <utility>
#include <GpioLine.hpp>

namespace beagleaccess {
    typedef std::pair<GpioLine, bool> ButtonLine;

    class ButtonCtl {
        public:
            static void initAt(GpioIndex ind, bool activeLow);
            static bool isPressed(GpioIndex ind);  
            static void shutDownAt(GpioIndex ind);          
    };
}