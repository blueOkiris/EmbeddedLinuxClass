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
#include <AccessLed.hpp>
#include <GpioLine.hpp>

void testLedOn();
void testLedBlink();
void testBlinkAllLeds();
void testRawGpio(char *chipName, unsigned int line, unsigned int value);
void testGpio();

int main() {
    //testLedOn();
    //testLedBlink();
    //testBlinkLeds();
    //testRawGpio((char *) "/dev/gpiochip1", 22, 1);
    testGpio();
}

void testLedBlink() {
    std::cout << "Single Led Blink Test" << std::endl;
    beagleaccess::Led led(beagleaccess::LedIndex::Usr0);
    led.off();
    std::this_thread::sleep_for(std::chrono::seconds(1));
    led.on();
    std::this_thread::sleep_for(std::chrono::seconds(1));
    led.off();
    std::this_thread::sleep_for(std::chrono::seconds(1));
}

void testLedOn() {
    std::cout << "Single Led On Test" << std::endl;
    beagleaccess::Led led(beagleaccess::LedIndex::Usr1);
    led.on();
}

void testBlinkAllLeds() {
    std::cout << "Led Blink through All Test" << std::endl;
    beagleaccess::Led::allOff();
    for(const auto index : beagleaccess::AllLedIndices) {
        beagleaccess::Led led(index);
        led.on();
        std::this_thread::sleep_for(std::chrono::seconds(1));
        led.off();
    }
}

void testGpio() {
    std::cout << "Single Gpio CLASS Test" << std::endl;
    beagleaccess::GpioLine ledLine;
    ledLine.open(beagleaccess::GpioChip::Chip1, 22);
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