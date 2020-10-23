#include <unistd.h>
#include <memaddr.h>
#include <gpio.h>

int main(int argc, char **args) {
    gpio.sysfs_disable_led_triggers();
    gpio_value_t switch_one_val = LOW;
    gpio_value_t switch_two_val = LOW;

    while(1) {
        if(gpio.init(GPIO0_START_ADDR)) {
            switch_one_val = gpio.read_value(P9_21);
        }
        if(gpio.init(GPIO1_START_ADDR)) {
            switch_two_val = gpio.read_value(P9_23);
            
            gpio.set_value(USR0, switch_one_val);
            gpio.set_value(USR1, switch_two_val);
        }
        usleep(10000);
    }

    return 0;
}
