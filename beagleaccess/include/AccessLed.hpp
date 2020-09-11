#pragma once

#include <GpioLine.hpp>

namespace beagleaccess {
    enum class LedIndex {
        Usr0, Usr1,
        Usr2, Usr3
    };

    static const LedIndex AllLedIndices[4] = {
        LedIndex::Usr0, LedIndex::Usr1,
        LedIndex::Usr2, LedIndex::Usr3
    };

    class LedCtrl {
        private:
            static GpioIndex _ledLine(LedIndex ind);
        public:
            static void init();
            static void turnOn(LedIndex ind);
            static void turnOff(LedIndex ind);
            static void shutDown();
    };
}
