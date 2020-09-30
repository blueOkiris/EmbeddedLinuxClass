#include <stdio.h>
#include <unistd.h>
#include <memaddr.h>
#include <gpio.h>

void testBlink();
void testMultiBlink();
void testVerifyRead();

void blinkWithBtns();

int main(int argc, char **args) {
    //testBlink();
    //testMultiBlink();
    testVerifyRead();
    //void blinkWithBtns();

    return 0;
}

void blinkWithBtns() {
    if(gpio.init(GPIO1_START_ADDR, GPIO1_SIZE)) {
        gpio.sysfs_disable_led_triggers();

    }
}

void testVerifyRead() {
    if(gpio.init(GPIO1_START_ADDR, GPIO1_SIZE)) {
        gpio.sysfs_disable_led_triggers();
        gpio_value_t val = 0;
        while(1) {
            printf("Turning on USR0...\n");
            gpio.set_value(USR3, LOW);
            gpio.set_value(USR0, HIGH);
            val = gpio.read_value(USR3);
            printf("Val %d\n", val);
            usleep(1000000);

            printf("Turning on USR1...\n");
            gpio.set_value(USR0, LOW);
            gpio.set_value(USR1, HIGH);
            val = gpio.read_value(USR3);
            printf("Val %d\n", val);
            usleep(1000000);

            printf("Turning on USR2...\n");
            gpio.set_value(USR1, LOW);
            gpio.set_value(USR2, HIGH);
            val = gpio.read_value(USR3);
            printf("Val %d\n", val);
            usleep(1000000);

            printf("Turning on USR3...\n");
            gpio.set_value(USR2, LOW);
            gpio.set_value(USR3, HIGH);
            val = gpio.read_value(USR3);
            printf("Val %d\n", val);
            usleep(1000000);
        }
    }
}

void testBlink() {
    if(gpio.init(GPIO1_START_ADDR, GPIO1_SIZE)) {
        gpio.sysfs_disable_led_triggers();
        while(1) {
            printf("Turning on...\n");
            gpio.set_value(USR3, HIGH);
            printf("Done.\n");
            usleep(1000000);

            printf("Turning off...\n");
            gpio.set_value(USR3, LOW);
            printf("Done.\n");
            usleep(1000000);
        }
    }
}

void testMultiBlink() {
    if(gpio.init(GPIO1_START_ADDR, GPIO1_SIZE)) {
        gpio.sysfs_disable_led_triggers();
        while(1) {
            printf("Turning on...\n");
            gpio.set_value(USR0, HIGH);
            gpio.set_value(USR1, HIGH);
            gpio.set_value(USR2, HIGH);
            gpio.set_value(USR3, HIGH);
            printf("Done.\n");
            usleep(1000000);

            printf("Turning off...\n");
            gpio.set_value(USR0, LOW);
            gpio.set_value(USR1, LOW);
            gpio.set_value(USR2, LOW);
            gpio.set_value(USR3, LOW);
            printf("Done.\n");
            usleep(1000000);
        }
    }
}
