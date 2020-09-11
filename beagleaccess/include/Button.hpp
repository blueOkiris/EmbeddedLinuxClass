#pragma once

#include <GpioLine.hpp>

namespace beagleaccess {
    class ButtonCtl {
        public:
            static void initAt(GpioIndex ind);
            static bool isPressed(GpioIndex ind);  
            static void shutDownAt(GpioIndex ind);          
    };
}