# Compiler options
CC :=     gcc
CFLAGS := -g -Wall -Werror -I. -c

.PHONY : all
all : blink-mmap toggle-fast gpio-tests

%.o : %.c
	$(CC) $(CFLAGS) -o $@ $<

# Program targets
blink-mmap : blinkmmap.o gpio.o
	$(CC) -o $@ $^

toggle-fast : togglefast.o gpio.o
	$(CC) -o $@ $^

gpio-tests : gpiotests.o gpio.o
	$(CC) -o $@ $^

.PHONY : clean
clean :
	rm -rf gpio-tests
	rm -rf blink-mmap
	rm -rf toggle-fast
	rm -rf *.o
