#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

const char *gpio_file_name = "/sys/class/gpio/gpio44/value";
const char *gpio_dir_file_name = "/sys/class/gpio/gpio44/direction";

int main(int argc, char **args) {
    if(argc < 2) {
        printf("No us time entered\n");
        return -1;
    }
    int period = atoi(args[1]);
    int value = 0;

    // Set as output
    FILE *gpio_dir_file = fopen(gpio_dir_file_name, "w");
    if(gpio_dir_file == NULL) {
        printf("Failed to set gpio as output!\n");
        return -1;
    }
    fprintf(gpio_dir_file, "out");
    fclose(gpio_dir_file);

    while(1) {
        FILE *gpio_file = fopen(gpio_file_name, "w");
        if(gpio_file == NULL) {
            printf("Failed to open gpio file!\n");
            return -1;
        }
        fprintf(gpio_file, "%d\n", value);
        fclose(gpio_file);

        usleep(period / 2);
        value = value ? 0 : 1;
    }

    return 0;
}
