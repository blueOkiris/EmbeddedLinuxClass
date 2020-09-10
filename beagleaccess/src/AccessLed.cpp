#include <iostream>
#include <string>
#include <fstream>
#include <AccessLed.hpp>

using namespace beagleaccess;

void Led::allOff() {
    for(const auto index : beagleaccess::AllLedIndices) {
        beagleaccess::Led led(index);
        led.off();
    }
}

Led::Led(LedIndex ind) {
    _index = ind;
}

LedIndex Led::index() {
    return _index;
}

bool Led::isOn() {
    return _readState(_index) == "1";
}

void Led::on() {
    _writeState(_index, 1);
}

void Led::off() {
    _writeState(_index, 0);
}

void Led::_writeState(const LedIndex &ind, const unsigned int &state) {
    const auto ledFileName = _ledBrightnessFolder(ind) + "brightness";
    /*std::ofstream ledFile;
    
    ledFile.open(ledFileName);
    ledFile << state;
    ledFile.close();*/
    /*FILE *ledFile = fopen("/sys/class/leds/beaglebone\\:green\\:usr0/brightness", "w");
    if(ledFile == NULL) {
        std::cout
            << "Failed to open led file '" 
            << ledFileName.c_str() << ".'" << std::endl;
    } else {
        fprintf(ledFile, "%s\n", state.c_str());
        fclose(ledFile);
    }*/
}

std::string Led::_readState(const LedIndex &ind) {
    return "0";
}

std::string Led::_ledBrightnessFolder(const LedIndex &ind) {
    switch(ind) {
        case LedIndex::Usr0:
            return "/sys/class/leds/beaglebone\\:green\\:usr0/";
        case LedIndex::Usr1:
            return "/sys/class/leds/beaglebone\\:green\\:usr1/";
        case LedIndex::Usr2:
            return "/sys/class/leds/beaglebone\\:green\\:usr2/";
        case LedIndex::Usr3:
            return "/sys/class/leds/beaglebone\\:green\\:usr3/";
    }
    return "";
}
