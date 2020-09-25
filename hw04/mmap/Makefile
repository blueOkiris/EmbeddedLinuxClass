# Compiler options
CC :=     gcc
CFLAGS := -O2 -Wall -Werror

.PHONY : all
all : blink-mmap toggle-fast

# Program targets
blink-mmap : blinkmmap.c
	$(CC) $(CFLAGS) -o $@ $^

toggle-fast : togglefast.c
	$(CC) $(CFLAGS) -o $@ $^

.PHONY : clean
clean :
	rm -rf blink-mmap
	rm -rf toggle-fast
