#include <thread>
#include <chrono>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <sys/ioctl.h>
#include <linux/gpio.h>
#include <fcntl.h>
#include <unistd.h>
#include <iostream>
#include <utility>
#include <GpioLine.hpp>
#include <AccessLed.hpp>
#include <Button.hpp>

using namespace beagleaccess;

void testLedOn();
void testBlinkAllLeds();
void testButton();
void testRawGpio(char *chipName, unsigned int line, unsigned int value);
void testGpio();

int main() {
    //testLedOn();
    testBlinkAllLeds();
    //testRawGpio((char *) "/dev/gpiochip1", 22, 1);
    //testGpio();
}

void testButton() {
    std::cout << "Single button test" << std::endl;
    auto buttonInd = std::make_pair(GpioChip::Chip0, 0);
    while(true) {
        ButtonCtl::initAt(buttonInd);  // P8_25 - AD0
        std::cout << "Button is on: " << ButtonCtl::isPressed(buttonInd);
        ButtonCtl::shutDownAt(buttonInd);
        std::this_thread::sleep_for(std::chrono::seconds(1));
    }
}

void testBlinkAllLeds() {
    std::cout << "Led Blink through All Test" << std::endl;
    LedCtrl::init();
    while(true) {
        for(const auto ind : AllLedIndices) {
            LedCtrl::turnOn(ind);
            std::this_thread::sleep_for(std::chrono::milliseconds(250));
            LedCtrl::turnOff(ind);
            std::this_thread::sleep_for(std::chrono::milliseconds(250));
        }
    }
    LedCtrl::shutDown();
}

void testLedOn() {
    std::cout << "Single Led On Test" << std::endl;
    LedCtrl::init();
    LedCtrl::turnOn(LedIndex::Usr1);
    std::this_thread::sleep_for(std::chrono::milliseconds(250));
    LedCtrl::turnOff(LedIndex::Usr1);
    std::this_thread::sleep_for(std::chrono::milliseconds(250));
    LedCtrl::shutDown();
}

void testGpio() {
    std::cout << "Single Gpio CLASS Test" << std::endl;
    GpioLine ledLine;
    ledLine.open(std::make_pair(GpioChip::Chip1, 22), true);
    ledLine.set(1);
    std::this_thread::sleep_for(std::chrono::seconds(1));
    ledLine.set(0);
    std::this_thread::sleep_for(std::chrono::seconds(1));
    ledLine.close();
}

void testRawGpio(char *chipName, unsigned int line, unsigned int value) {
    std::cout << "Single Led Raw C API Test" << std::endl;

    struct gpiohandle_request req;
	struct gpiohandle_data data;
    int chipFile;
    int ret;
    
    chipFile = open(chipName, 0);
    if(chipFile == -1) {
        std::cout << "Failed to open gpiochip #1" << std::endl;
        return;
    }
    
    req.lineoffsets[0] = line;
    req.flags = GPIOHANDLE_REQUEST_OUTPUT;
    memcpy(req.default_values, &data, sizeof(req.default_values));
    strcpy(req.consumer_label, "gpio");
    req.lines = 1;

    ret = ioctl(chipFile, GPIO_GET_LINEHANDLE_IOCTL, &req);
    if(ret == -1) {
        std::cout << "Failed to issue get line handle." << std::endl;
    }
    
    close(chipFile);
    
    data.values[0] = value;
    ret = ioctl(req.fd, GPIOHANDLE_SET_LINE_VALUES_IOCTL, &data);
    if(ret == -1) {
        std::cout << "Failed to issue set line." << std::endl;
    }

    std::this_thread::sleep_for(std::chrono::seconds(1));

    data.values[0] = !value;
    ret = ioctl(req.fd, GPIOHANDLE_SET_LINE_VALUES_IOCTL, &data);
    if(ret == -1) {
        std::cout << "Failed to issue set line." << std::endl;
    }

    std::this_thread::sleep_for(std::chrono::seconds(1));

	close(req.fd);
}
