#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/mman.h>
#include <stdio.h>
#include <stdlib.h>
#include <memaddr.h>
#include <gpio.h>

void *gpio_addr;
unsigned int *gpio_setdataout_addr;
unsigned int *gpio_cleardataout_addr;
unsigned int *gpio_datain_addr;
int fd = -1;

char failed = 1;

char gpio__init(unsigned int chip) {
    failed = 1;

    if(fd != -1) {
        munmap(0, GPIO_SIZE);
        close(fd);
    }
    fd = open("/dev/mem", O_RDWR);
    if(fd == -1) {
        printf("Failed to open /dev/mem. Are you root?\n");
        return 0;
    }

    gpio_addr = mmap(
        0, GPIO_SIZE,
        PROT_READ | PROT_WRITE, MAP_SHARED,
        fd, chip
    );

    if(gpio_addr != (void *) -1) {
        gpio_setdataout_addr = gpio_addr + GPIO_SETDATAOUT;
        gpio_cleardataout_addr = gpio_addr + GPIO_CLEARDATAOUT;
        gpio_datain_addr = gpio_addr + GPIO_DATAIN;

        failed = 0;
        return 1;
    } else {
        unsigned int rem = GPIO1_START_ADDR % sysconf(_SC_PAGE_SIZE);

        printf("Failed to map memory. Are you root?\n");
        printf("Address has remainder %d with page size\n", rem);
        return 0;
    }
}

void gpio__sysfs_disable_led_triggers() {
    const char *led_trigger_cmds[4] = {
        "echo \"none\" > /sys/class/leds/beaglebone:green:usr0/trigger",
        "echo \"none\" > /sys/class/leds/beaglebone:green:usr1/trigger",
        "echo \"none\" > /sys/class/leds/beaglebone:green:usr2/trigger",
        "echo \"none\" > /sys/class/leds/beaglebone:green:usr3/trigger"
    };

    for(int i = 0; i < 4; i++) {
        system(led_trigger_cmds[i]);
    }
}

void gpio__set_value(unsigned int addr, gpio_value_t value) {
    if(failed) {
        return;
    }

    if(value == HIGH) {
        *gpio_setdataout_addr = addr;
    } else if(value == LOW) {
        *gpio_cleardataout_addr = addr;
    }
}

gpio_value_t gpio__read_value(unsigned int addr) {
    if(*gpio_datain_addr & addr) {
        return HIGH;
    } else {
        return LOW;
    }
}

unsigned int gpio__read_value_raw() {
    return *gpio_datain_addr;
}
