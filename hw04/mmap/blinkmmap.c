#include <stdio.h>
#include <unistd.h>
#include <memaddr.h>
#include <gpio.h>

void testBlink();
void testMultiBlink();

int main(int argc, char **args) {
    //testBlink();
    testMultiBlink();

    return 0;
}

void testBlink() {
    gpio.sysfs_disable_led_triggers();
    if(gpio.init()) {
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
    if(gpio.init()) {
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
