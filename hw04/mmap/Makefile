# Compiler options
CC :=     gcc
CFLAGS := -g -Wall -Werror -I.

.PHONY : all
all : blink-mmap toggle-fast

# Program targets
blink-mmap : blinkmmap.c gpio.c
	$(CC) $(CFLAGS) -o $@ $^

toggle-fast : togglefast.c gpio.c
	$(CC) $(CFLAGS) -o $@ $^

.PHONY : clean
clean :
	rm -rf blink-mmap
	rm -rf toggle-fast
