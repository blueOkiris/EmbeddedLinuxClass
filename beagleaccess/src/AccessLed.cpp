#include <vector>
#include <utility>
#include <GpioLine.hpp>
#include <AccessLed.hpp>

using namespace beagleaccess;

static GpioLine userLeds_g[4];

std::pair<GpioChip, unsigned int> LedCtrl::_ledLine(LedIndex ind) {
    switch(ind) {
        case LedIndex::Usr0:
            return std::make_pair(GpioChip::Chip1, 21);
            break;
        case LedIndex::Usr1:
            return std::make_pair(GpioChip::Chip1, 22);
            break;
        case LedIndex::Usr2:
            return std::make_pair(GpioChip::Chip1, 23);
            break;
        case LedIndex::Usr3:
            return std::make_pair(GpioChip::Chip1, 24);
            break;
    }

    return std::make_pair(GpioChip::Chip1, 22);
}

void LedCtrl::init() {
    system("echo none > /sys/class/leds/beaglebone\\:green\\:usr0/trigger");
    system("echo none > /sys/class/leds/beaglebone\\:green\\:usr1/trigger");
    system("echo none > /sys/class/leds/beaglebone\\:green\\:usr2/trigger");
    system("echo none > /sys/class/leds/beaglebone\\:green\\:usr3/trigger");

    for(const auto ind : AllLedIndices) {
        const auto lineInfo = _ledLine(ind);
        userLeds_g[static_cast<int>(ind)].open(lineInfo, true);
        userLeds_g[static_cast<int>(ind)].set(0);
    }
}

void LedCtrl::turnOn(LedIndex ind) {
    userLeds_g[static_cast<int>(ind)].set(1);
}

void LedCtrl::turnOff(LedIndex ind) {
    userLeds_g[static_cast<int>(ind)].set(0);
}

void LedCtrl::shutDown() {
    for(const auto ind : AllLedIndices) {
        userLeds_g[static_cast<int>(ind)].close();
    }
}
