#include <unistd.h>
#include <memaddr.h>
#include <gpio.h>

int main(int argc, char **args) {
    if(gpio.init(GPIO0_START_ADDR)) {
        gpio.sysfs_disable_led_triggers();
        while(1) {
            gpio.set_value(P9_22, HIGH);
            gpio.set_value(P9_22, LOW);
        }
    }
    return 0;
}
