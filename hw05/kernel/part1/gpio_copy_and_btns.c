#include <stdint.h>
#include <stddef.h> // For <signedness>int<number>_t constructions
#include <linux/init.h>
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/gpio.h> // Required for the GPIO functions
#include <linux/interrupt.h> // Required for the IRQ code

/*
 * Licensing stuff
 *
 * I'd say author Derek Molloy modified by me,
 * but at this point I've rewritten everything,
 * so I'm saying based-on the old file instead
 */
MODULE_LICENSE("GPL");
MODULE_AUTHOR("Dylan Turner (based on gpio_test.c by Derek Molloy)");
MODULE_DESCRIPTION(
    "A driver to map P9_15 to P9_16"
    " and turn on P9_12 and P9_14 from P9_15 and P9_18"
);
MODULE_VERSION("0.1");

// Some stucts to make code cleaner/more obvious hopefully
typedef struct {
    const uint32_t pin;
    const uint32_t irq_num;
    uint32_t num_triggers; // keep track of presses for info
} button_t;

typedef struct {
    const uint32_t pin;
    bool is_on;
} led_t; // keep track of current state

static led_t gpio_map_output_g = { 51, 0 }; // P9_16
static button_t gpio_map_input_g = { 48, 0, 0 }; // P9_15
static led_t gpio_leds_g[2] = {
    { 60, 0 }, // P9_12
    { 50, 0 } // P9_14
};
static button_t gpio_ctrl_btns_g[2] = {
    { 47, 0, 0 }, // P8_15
    { 65, 0, 0 } // P8_18
};

/*
 * Custom IRQ handlers
 * 
 * inline for SPEEEEEEEEDDDD
 */
inline irq_handler_t map_irq_handler(
        uint32_t irq, void *dev_id, struct pt_regs *regs) {
    gpio_map_input_g.num_triggers++;
    bool input_val = gpio_get_value(gpio_map_input_g.pin);
    
    // Copy the state of the input to the state of the output
    gpio_map_output_g.is_on = input_val;
    gpio_set_value(gpio_map_output_g.pin, gpio_map_output_g.is_on);
    
    // Print about it
    printk(
        KERN_INFO
            "GPIO Mapping and LED Control:"
            " 'map input' set to 'map output' with value %d\n",
        input_val
    );
    
    return (irq_handler_t) IRQ_HANDLED;
}

inline irq_handler_t led_ctrl_handler(
        uint32_t irq, void *dev_id, struct pt_regs *regs) {
    int index = irq == gpio_ctrl_btns_g[0].irq_num ? 0 : 1;
    gpio_ctrl_btns_g[index].num_triggers++;
    
    // Toggle LED
    gpio_leds_g[index].is_on = !gpio_leds_g[index].is_on;
    gpio_set_value(gpio_leds_g[index].pin, gpio_leds_g[index].is_on);
    
    printk(
        KERN_INFO
            "GPIO Mapping and LED Control:"
            " Toggled 'led %d' to value %d\n",
        index,
        gpio_leds_g[index].is_on
    );
    return (irq_handler_t) IRQ_HANDLED;
}

/*
 * LKM initialization function
 * 
 * __init indicates built-in driver (not LKM)
 * Only used at initialization and freed up after
 * Returns 0 on success
 */
inline int __init copy_and_btns_init() {
    int result = 0;
    printk(KERN_INFO "GPIO Mapping and LED Control: Initializing!\n");
    
    // Initialize the outputs. Apparently don't have to do this for inputs?
    if (!gpio_is_valid(gpio_map_output_g.pin)) {
        printk(
            KERN_INFO
                "GPIO Mapping and LED Control: Invalid 'mapped gpio': %d\n",
            gpio_map_output_g.pin
        );
        return -ENODEV;
    }
    if (!gpio_is_valid(gpio_leds_g[0].pin)) {
        printk(
            KERN_INFO "GPIO Mapping and LED Control: Invalid 'led pin 0': %d\n",
            gpio_leds_g[0].pin
        );
        return -ENODEV;
    }
    if (!gpio_is_valid(gpio_leds_g[1].pin)) {
        printk(
            KERN_INFO "GPIO Mapping and LED Control: Invalid 'led pin 1': %d\n",
            gpio_leds_g[1].pin
        );
        return -ENODEV;
    }
   
    /*
     * Set up all the LEDs
     * GPIO in output mode and will be on by default
     * 
     * Request them, set them as output, and turn them on
     * Also tell them to appear in /sys/class/gpio
     * Note the false in the export means it can't dissapear
     */
    
    gpio_map_output_g.is_on = true;
    gpio_request(gpio_map_output_g.pin, "sysfs");
    gpio_direction_output(gpio_map_output_g.pin, gpio_map_output_g.is_on);
    gpio_export(gpio_map_output_g.pin, false);
    
    gpio_leds_g[0].is_on = true;
    gpio_request(gpio_leds_g[0].pin, "sysfs");
    gpio_direction_output(gpio_leds_g[0].pin, gpio_leds_g[0].is_on);
    gpio_export(gpio_leds_g[0].pin, false);
    
    gpio_leds_g[1].is_on = true;
    gpio_request(gpio_leds_g[1].pin, "sysfs");
    gpio_direction_output(gpio_leds_g[1].pin, gpio_leds_g[1].is_on);
    gpio_export(gpio_leds_g[1].pin, false);
    
    /*
     * Set up inputs
     * 
     * Request them, set output direction, and turn on debounce
     * Also tell them to appear in /sys/class/gpio
     * Note the false in the export means it can't dissapear
     */
    
    gpio_request(gpio_map_input_g.pin, "sysfs");
    gpio_direction_input(gpio_map_input_g.pin);
    gpio_set_debounce(gpio_map_input_g.pin, 200); // delay of 200ms
    gpio_export(gpio_map_input_g.pin, false);
    
    gpio_request(gpio_ctrl_btns_g[0].pin, "sysfs");
    gpio_direction_input(gpio_ctrl_btns_g[0].pin);
    gpio_set_debounce(gpio_ctrl_btns_g[0].pin, 200);
    gpio_export(gpio_ctrl_btns_g[0].pin, false);
    
    gpio_request(gpio_ctrl_btns_g[1].pin, "sysfs");
    gpio_direction_input(gpio_ctrl_btns_g[1].pin);
    gpio_set_debounce(gpio_ctrl_btns_g[1].pin, 200);
    gpio_export(gpio_ctrl_btns_g[1].pin, false);
    
    // Perform a quick test to see that the buttons are working as expected
    printk(
        KERN_INFO
            "GPIO Mapping and LED Control:"
            " The 'map button' state is currently: %d\n",
        gpio_get_value(gpio_map_input_g.pin)
    );
    printk(
        KERN_INFO
            "GPIO Mapping and LED Control:"
            " The 'ctrl button 0' state is currently: %d\n",
        gpio_get_value(gpio_ctrl_btns_g[0].pin)
    );
    printk(
        KERN_INFO
            "GPIO Mapping and LED Control:"
            " The 'ctrl button 1' state is currently: %d\n",
        gpio_get_value(gpio_ctrl_btns_g[1].pin)
    );
    
    // NOTE: GPIO numbers and IRQ numbers are not the same!
    uint32_t irq_num = gpio_to_irq(gpio_map_input_g.pin);
    gpio_map_input_g = { gpio_map_input_g.pin, irq_num_g, 0 };
    printk(
        KERN_INFO
            "GPIO Mapping and LED Control:"
            " The 'map button' is mapped to IRQ: %d\n",
        irq_num
    );
    
    irq_num = gpio_to_irq(gpio_ctrl_btns_g[0].pin);
    gpio_ctrl_btns_g[0] = { gpio_ctrl_btns_g[0].pin, irq_num, 0 };
    printk(
        KERN_INFO
            "GPIO Mapping and LED Control:"
            " The 'control button 0' is mapped to IRQ: %d\n",
        irq_num
    );
    
    irq_num = gpio_to_irq(gpio_ctrl_btns_g[1].pin);
    gpio_ctrl_btns_g[1] = { gpio_ctrl_btns_g[1].pin, irq_num, 0 };
    printk(
        KERN_INFO
            "GPIO Mapping and LED Control:"
            " The 'control button 1' is mapped to IRQ: %d\n",
        irq_num
    );
    
    // Request irqs for each input
    result = request_irq(
        gpio_map_input_g.irq_num, (irq_handler_t) map_irq_handler,
        IRQF_TRIGGER_RISING | IRQF_TRIGGER_FALLING,
        "map_irq_handler", // /proc/interrupts id
        NULL
    );
    result |= request_irq(
        gpio_ctrl_btns_g[0].irq_num, (irq_handler_t) led_ctrl_handler,
        IRQF_TRIGGER_HIGH, "led_ctrl_irq_handler0", // /proc/interrupts id
        NULL
    );
    result |= request_irq(
        gpio_ctrl_btns_g[1].irq_num, (irq_handler_t) led_ctrl_handler,
        IRQF_TRIGGER_HIGH, "led_ctrl_irq_handler1", // /proc/interrupts id
        NULL
    );

    printk(
        KERN_INFO
            "GPIO Mapping and LED Control:"
            " The interrupt request result is: %d\n",
        result
    );
    return result;
}

// Clean up function
inline void __exit copy_and_btns_exit(void){
    // Remove the buttons
    printk(
        KERN_INFO
            "GPIO Mapping and LED Control:"
            " The 'map button' state is currently: %d\n", 
        gpio_get_value(gpio_map_input_g.pin);
    );
    printk(
        KERN_INFO
            "GPIO Mapping and LED Control:"
            " The 'map button' was triggered %d times\n",
        gpio_map_input_g.num_triggers
    );
    free_irq(gpio_map_input_g.irq, NULL);
    gpio_unexport(gpio_map_input_g.pin);
    gpio_free(gpio_map_input_g.pin);
    
    printk(
        KERN_INFO
            "GPIO Mapping and LED Control:"
            " The 'control button 0' state is currently: %d\n", 
        gpio_get_value(gpio_ctrl_btns_g[0].pin);
    );
    printk(
        KERN_INFO
            "GPIO Mapping and LED Control:"
            " The 'control button 0' was triggered %d times\n",
        gpio_ctrl_btns_g[0].num_triggers
    );
    free_irq(gpio_ctrl_btns_g[0].irq, NULL);
    gpio_unexport(gpio_ctrl_btns_g[0].pin);
    gpio_free(gpio_ctrl_btns_g[0].pin);
    
    printk(
        KERN_INFO
            "GPIO Mapping and LED Control:"
            " The 'control button 1' state is currently: %d\n", 
        gpio_get_value(gpio_ctrl_btns_g[0].pin);
    );
    printk(
        KERN_INFO
            "GPIO Mapping and LED Control:"
            " The 'control button 1' was triggered %d times\n",
        gpio_map_input_g.num_triggers
    );
    free_irq(gpio_ctrl_btns_g[1].irq, NULL);
    gpio_unexport(gpio_ctrl_btns_g[1].pin);
    gpio_free(gpio_ctrl_btns_g[1].pin);
    
    // Remove the leds
    gpio_set_value(gpio_map_output_g.pin, 0);
    gpio_unexport(gpio_map_output_g.pin);
    gpio_free(gpio_map_output_g.pin);
    
    gpio_set_value(gpio_leds_g[0].pin, 0);
    gpio_unexport(gpio_leds_g[0].pin);
    gpio_free(gpio_leds_g[0].pin);
    
    gpio_set_value(gpio_leds_g[1].pin, 0);
    gpio_unexport(gpio_leds_g[1].pin);
    gpio_free(gpio_leds_g[1].pin);
    
    
    printk(KERN_INFO "GPIO Mapping and LED Control: Goodbye!\n");
}

/*
 * These next calls are mandatory
 * Identify the initialization function and cleanup functions
 */
module_init(copy_and_btns_init);
module_exit(copy_and_btns_exit);
