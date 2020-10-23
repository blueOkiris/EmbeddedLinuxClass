#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <memaddr.h>
#include <gpio.h>

void testBlink();
void testMultiBlink();
void testVerifyRead();
void testBtns();

int main(int argc, char **args) {
    //testBlink();
    //testMultiBlink();
    //testVerifyRead();
    testBtns();
}

void testBtns() {
    gpio.sysfs_disable_led_triggers();
    gpio_value_t switch_one_val = LOW;
    gpio_value_t switch_two_val = LOW;

    while(1) {
        system("clear");
        printf("Round:\n");
        if(gpio.init(GPIO0_START_ADDR)) {
            switch_one_val = gpio.read_value(P9_21);
            printf("%d - raw: %u\n", switch_one_val, gpio.read_value_raw());
        }

        if(gpio.init(GPIO1_START_ADDR)) {
            switch_two_val = gpio.read_value(P9_23);
            printf("%d - raw: %u", switch_two_val, gpio.read_value_raw());

            gpio.set_value(USR0, switch_one_val);
            gpio.set_value(USR1, switch_two_val);
        }
        printf("\n");
        usleep(10000);
    }
}

void testVerifyRead() {
    if(gpio.init(GPIO1_START_ADDR)) {
        gpio.sysfs_disable_led_triggers();
        gpio_value_t val = 0;
        while(1) {
            printf("Turning on USR0...\n");
            gpio.set_value(USR3, LOW);
            gpio.set_value(USR0, HIGH);
            val = gpio.read_value(USR3);
            printf("Val %d\n", val);
            printf("Raw Val %d:\n", gpio.read_value_raw());
            usleep(100000);

            printf("Turning on USR1...\n");
            gpio.set_value(USR0, LOW);
            gpio.set_value(USR1, HIGH);
            val = gpio.read_value(USR3);
            printf("Val %d\n", val);
            printf("Raw Val %d:\n", gpio.read_value_raw());
            usleep(100000);

            printf("Turning on USR2...\n");
            gpio.set_value(USR1, LOW);
            gpio.set_value(USR2, HIGH);
            val = gpio.read_value(USR3);
            printf("Val %d\n", val);
            printf("Raw Val %d:\n", gpio.read_value_raw());
            usleep(100000);

            printf("Turning on USR3...\n");
            gpio.set_value(USR2, LOW);
            gpio.set_value(USR3, HIGH);
            val = gpio.read_value(USR3);
            printf("Val %d\n", val);
            usleep(100000);
        }
    }
}

void testBlink() {
    if(gpio.init(GPIO1_START_ADDR)) {
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
    if(gpio.init(GPIO1_START_ADDR)) {
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
