#pragma once

#include <string>

namespace beagleaccess {
    enum class LedIndex {
        Usr0, Usr1,
        Usr2, Usr3
    };

    static const LedIndex AllLedIndices[4] = {
        LedIndex::Usr0, LedIndex::Usr1,
        LedIndex::Usr2, LedIndex::Usr3
    };

    class Led {
        private:
            LedIndex _index;
            
            static void _writeState(
                const LedIndex &ind, const unsigned int &state
            );
            static std::string _readState(const LedIndex &ind);
            static std::string _ledBrightnessFolder(const LedIndex &ind);
            
        public:
            Led(LedIndex ind);
            
            static void allOff();

            LedIndex index();
            void on();
            void off();
            bool isOn();
    };
}
