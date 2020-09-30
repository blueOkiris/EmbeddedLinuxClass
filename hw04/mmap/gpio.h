#pragma once

typedef enum {
    HIGH = 1, LOW = 0
} gpio_value_t;

char gpio__init();
void gpio__sysfs_disable_led_triggers();
void gpio__set_value(unsigned int addr, gpio_value_t value);

static const struct {
    char (*init)();
    void (*sysfs_disable_led_triggers)();
    void (*set_value)(unsigned int addr, gpio_value_t value);
} gpio = {
    gpio__init,
    gpio__sysfs_disable_led_triggers,
    gpio__set_value
};
