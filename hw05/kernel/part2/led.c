#include <linux/init.h>
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/gpio.h> // Required for the GPIO functions
#include <linux/kobject.h> // Using kobjects for the sysfs bindings
#include <linux/kthread.h> // Using kthreads for the flashing functionality
#include <linux/delay.h> // Using this header for the msleep() function

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Derek Molloy (modified by Dylan Turner)");
MODULE_DESCRIPTION("A simple Linux LED driver LKM for the BBB");
MODULE_VERSION("0.1");

// LEDs 12 and 14
static unsigned int gpioLED = 60;
static unsigned int gpioLED2 = 50;
module_param(gpioLED, uint, S_IRUGO); // Param desc. S_IRUGO cannot be changed
module_param(gpioLED2, uint, S_IRUGO);
MODULE_PARM_DESC(gpioLED, " GPIO LED 1 number (default=60)");
MODULE_PARM_DESC(gpioLED2, " GPIO LED 2 number (default=50)");

static unsigned int blinkPeriodMs = 1000;
static unsigned int blinkPeriodMs2 = 500;
module_param(blinkPeriodMs, uint, S_IRUGO);
module_param(blinkPeriodMs2, uint, S_IRUGO);
MODULE_PARM_DESC(
   blinkPeriodMs, " LED 1 blink period in ms (min=1, default=1000, max=10000)"
);
MODULE_PARM_DESC(
   blinkPeriodMs2, " LED 2 blink period in ms (min=1, default=1000, max=10000)"
);

enum modes { OFF, ON, FLASH };
static char ledName[7] = "ledXXX"; // Null terminated default string
static char ledName2[7] = "ledXXX";
static bool ledOn = 0; // Is the LED on or off? Used for flashing
static bool ledOn2 = 0;
static enum modes mode = FLASH;
static enum modes mode2 = FLASH;

/** @brief A callback function to display the LED mode
 *  @param kobj represents a kernel object device that appears in the sysfs
 *  @param attr the pointer to the kobj_attribute struct
 *  @param buf the buffer to which to write the number of presses
 *  @return return the number of characters of the mode string displayed
 */
static ssize_t mode_show(
      struct kobject *kobj, struct kobj_attribute *attr, char *buf) {
   switch(mode) {
      case OFF:
         return sprintf(buf, "off\n");
      case ON:
         return sprintf(buf, "on\n");
      case FLASH:
         return sprintf(buf, "flash\n");
      default:
         return sprintf(buf, "LKM Error\n");
   }
}

static ssize_t mode_show2(
      struct kobject *kobj, struct kobj_attribute *attr, char *buf) {
   switch(mode2) {
      case OFF:
         return sprintf(buf, "off\n");
      case ON:
         return sprintf(buf, "on\n");
      case FLASH:
         return sprintf(buf, "flash\n");
      default:
         return sprintf(buf, "LKM Error\n");
   }
}

/** @brief A callback function to store the LED mode using the enum above */
static ssize_t mode_store(
      struct kobject *kobj, struct kobj_attribute *attr,
      const char *buf, size_t count) {
   // the count-1 is important as otherwise the \n is used in the comparison
   if(strncmp(buf, "on", count - 1) == 0) {
      mode = ON;
   } else if(strncmp(buf, "off", count - 1) == 0) {
      mode = OFF;
   } else if(strncmp(buf, "flash", count - 1) == 0) {
      mode = FLASH;
   }
   return count;
}

static ssize_t mode_store2(
      struct kobject *kobj, struct kobj_attribute *attr,
      const char *buf, size_t count) {
   // the count-1 is important as otherwise the \n is used in the comparison
   if(strncmp(buf, "on", count - 1) == 0) {
      mode2 = ON;
   } else if(strncmp(buf, "off", count - 1) == 0) {
      mode2 = OFF;
   } else if(strncmp(buf, "flash", count - 1) == 0) {
      mode2 = FLASH;
   }
   return count;
}

/** @brief A callback function to display the LED period */
static ssize_t period_show(
      struct kobject *kobj, struct kobj_attribute *attr, char *buf) {
   return sprintf(buf, "%d\n", blinkPeriodMs);
}

static ssize_t period_show2(
      struct kobject *kobj, struct kobj_attribute *attr, char *buf) {
   return sprintf(buf, "%d\n", blinkPeriodMs2);
}

/** @brief A callback function to store the LED period value */
static ssize_t period_store(
      struct kobject *kobj, struct kobj_attribute *attr,
      const char *buf, size_t count) {
   unsigned int period; // Using a variable to validate the data sent
   sscanf(buf, "%du", &period); // Read in the period as an unsigned int
   if((period > 1) && (period <= 10000)) { // Must be 2ms or more, 10s or less
      blinkPeriodMs = period; // Within range, assign to blinkPeriod variable
   }
   return period;
}

static ssize_t period_store2(
      struct kobject *kobj, struct kobj_attribute *attr,
      const char *buf, size_t count) {
   unsigned int period; // Using a variable to validate the data sent
   sscanf(buf, "%du", &period); // Read in the period as an unsigned int
   if((period > 1) && (period <= 10000)) { // Must be 2ms or more, 10s or less
      blinkPeriodMs2 = period; // Within range, assign to blinkPeriod variable
   }
   return period;
}

/** Use these helper macros to define the name
 *  and access levels of the kobj_attributes
 *  The kobj_attribute has an attribute attr (name and mode),
 *  show and store function pointers
 *  The period variable is associated with the blinkPeriod variable
 *  and it is to be exposed
 *  with mode 0666 using the period_show and period_store functions above
 */
static struct kobj_attribute period_attr = __ATTR(
   blinkPeriodMs, 0660, period_show, period_store
);
static struct kobj_attribute period_attr2 = __ATTR(
   blinkPeriodMs2, 0660, period_show2, period_store2
);
static struct kobj_attribute mode_attr = __ATTR(
   mode, 0660, mode_show, mode_store
);
static struct kobj_attribute mode_attr2 = __ATTR(
   mode2, 0660, mode_show2, mode_store2
);

/** The ebb_attrs[] is an array of attributes
 *  that is used to create the attribute group below.
 *  The attr property of the kobj_attribute is used
 *  to extract the attribute struct
 */
static struct attribute *ebb_attrs[] = {
   &period_attr.attr, // The period at which the LED flashes
   &mode_attr.attr, // Is the LED on or off?
   NULL,
};
static struct attribute *ebb_attrs2[] = {
   &period_attr2.attr, // The period at which the LED flashes
   &mode_attr2.attr, // Is the LED on or off?
   NULL,
};

/** The attribute group uses the attribute array and a name,
 *  which is exposed on sysfs -- in this case it is gpio49,
 *  which is automatically defined in the ebbLED_init() function below
 *  using the custom kernel parameter
 *  that can be passed when the module is loaded.
 */
static struct attribute_group attr_group = {
   .name  = ledName, // The name is generated in ebbLED_init()
   .attrs = ebb_attrs, // The attributes array defined just above
};
static struct attribute_group attr_group2 = {
   .name  = ledName2, // The name is generated in ebbLED_init()
   .attrs = ebb_attrs2, // The attributes array defined just above
};

static struct kobject *ebb_kobj;            /// The pointer to the kobject
static struct kobject *ebb_kobj2;
static struct task_struct *task;            /// The pointer to the thread task
static struct task_struct *task2;

/** @brief The LED Flasher main kthread loop
 *
 *  @param arg A void pointer used in order to pass data to the thread
 *  @return returns 0 if successful
 */
static int flash(void *arg) {
   printk(KERN_INFO "EBB LED: Thread has started running \n");
   while(!kthread_should_stop()) { // Returns true when kthread_stop() is called
      set_current_state(TASK_RUNNING);
      if(mode == FLASH) {
         ledOn = !ledOn; // Invert the LED state
      } else if(mode == ON) {
         ledOn = true;
      } else {
         ledOn = false;
      }
      gpio_set_value(gpioLED, ledOn); // Use the LED state to change the LED
      set_current_state(TASK_INTERRUPTIBLE);
      msleep(blinkPeriodMs / 2); // millisecond sleep for half of the period
   }
   printk(KERN_INFO "EBB LED: Thread has run to completion \n");
   return 0;
}

static int flash2(void *arg) {
   printk(KERN_INFO "EBB LED: Thread has started running \n");
   while(!kthread_should_stop()) { // Returns true when kthread_stop() is called
      set_current_state(TASK_RUNNING);
      if(mode2 == FLASH) {
         ledOn2 = !ledOn; // Invert the LED state
      } else if(mode2 == ON) {
         ledOn2 = true;
      } else {
         ledOn2 = false;
      }
      gpio_set_value(gpioLED2, ledOn2); // Use the LED state to change the LED
      set_current_state(TASK_INTERRUPTIBLE);
      msleep(blinkPeriodMs2 / 2); // millisecond sleep for half of the period
   }
   printk(KERN_INFO "EBB LED: Thread has run to completion \n");
   return 0;
}

/** @brief The LKM initialization function
 *  The static keyword restricts the visibility of the function to in this file.
 *  The __init macro means that for a built-in driver (not a LKM)
 *  the function is only used at initialization time
 *  and that it can be discarded and its memory freed up after that point.
 *  In this example this function sets up the GPIOs and the IRQ
 *  @return returns 0 if successful
 */
static int __init ebbLED_init(void) {
   int result = 0;

   printk(KERN_INFO "EBB LED: Initializing the EBB LED LKM\n");
   sprintf(ledName, "led%d", gpioLED); // Create the gpio115 name
   sprintf(ledName2, "led%d", gpioLED2); // Create the gpio115 name

   ebb_kobj = kobject_create_and_add("ebb1", kernel_kobj->parent);
   if(!ebb_kobj) {
      printk(KERN_ALERT "EBB LED: failed to create kobject\n");
      return -ENOMEM;
   }
   // add the attributes to /sys/ebb/ -- for example, /sys/ebb/led49/ledOn
   result = sysfs_create_group(ebb_kobj, &attr_group);
   if(result) {
      printk(KERN_ALERT "EBB LED: failed to create sysfs group\n");
      kobject_put(ebb_kobj); // clean up -- remove the kobject sysfs entry
      return result;
   }
   ledOn = true;
   gpio_request(gpioLED, "sysfs"); // gpioLED is 49 by default, request it
   gpio_direction_output(gpioLED, ledOn); // gpio in output mode and turn on
   gpio_export(gpioLED, false);  // causes gpio49 to appear in /sys/class/gpio
                                 // 2nd argument stops the dir from changing
   task = kthread_run(flash, NULL, "LED_flash_thread"); // Start LED flashing
   if(IS_ERR(task)) { // Kthread name is LED_flash_thread
      printk(KERN_ALERT "EBB LED: failed to create the task\n");
      return PTR_ERR(task);
   }

   ebb_kobj2 = kobject_create_and_add("ebb2", kernel_kobj->parent);
   if(!ebb_kobj2) {
      printk(KERN_ALERT "EBB LED: failed to create kobject\n");
      return -ENOMEM;
   }
   // add the attributes to /sys/ebb/ -- for example, /sys/ebb/led49/ledOn
   result |= sysfs_create_group(ebb_kobj2, &attr_group2);
   if(result) {
      printk(KERN_ALERT "EBB LED: failed to create sysfs group\n");
      kobject_put(ebb_kobj2); // clean up -- remove the kobject sysfs entry
      return result;
   }
   ledOn2 = true;
   gpio_request(gpioLED2, "sysfs"); // gpioLED is 49 by default, request it
   gpio_direction_output(gpioLED2, ledOn2); // gpio in output mode and turn on
   gpio_export(gpioLED2, false);  // causes gpio49 to appear in /sys/class/gpio
                                 // 2nd argument stops the dir from changing
   task2 = kthread_run(flash2, NULL, "LED_flash_thread2"); // Start LED flashing
   if(IS_ERR(task2)) { // Kthread name is LED_flash_thread
      printk(KERN_ALERT "EBB LED: failed to create the task\n");
      return PTR_ERR(task2);
   }
   
   return result;
}

/** @brief The LKM cleanup function
 *  Similar to the initialization function, it is static. The __exit macro notifies that if this
 *  code is used for a built-in driver (not a LKM) that this function is not required.
 */
static void __exit ebbLED_exit(void){
   kthread_stop(task); // Stop the LED flashing thread
   kobject_put(ebb_kobj); // clean up -- remove the kobject sysfs entry
   gpio_set_value(gpioLED, 0); // Turn the LED off
   gpio_set_value(gpioLED2, 0); // Turn the LED off
   gpio_unexport(gpioLED); // Unexport the Button GPIO
   gpio_unexport(gpioLED2); // Unexport the Button GPIO
   gpio_free(gpioLED); // Free the LED GPIO
   gpio_free(gpioLED2); // Free the LED GPIO
   printk(KERN_INFO "EBB LED: Goodbye from the EBB LED LKM!\n");
}

/// This next calls are  mandatory -- they identify the initialization function
/// and the cleanup function (as above).
module_init(ebbLED_init);
module_exit(ebbLED_exit);
