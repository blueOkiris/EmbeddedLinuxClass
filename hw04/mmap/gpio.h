#pragma once

typedef enum {
    HIGH = 1, LOW = 0
} gpio_value_t;

char gpio__init(unsigned int chip);
void gpio__sysfs_disable_led_triggers();
void gpio__set_value(unsigned int addr, gpio_value_t value);
gpio_value_t gpio__read_value(unsigned int addr);
unsigned int gpio__read_value_raw();

static const struct {
    char (*init)(unsigned int);
    void (*sysfs_disable_led_triggers)();
    void (*set_value)(unsigned int addr, gpio_value_t value);
    gpio_value_t (*read_value)(unsigned int addr);
    unsigned int (*read_value_raw)();
} gpio = {
    gpio__init,
    gpio__sysfs_disable_led_triggers,
    gpio__set_value,
    gpio__read_value,
    gpio__read_value_raw
};
