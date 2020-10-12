# HW05 Answers Document

## Project

> Add a project (or two) to the Project page (see Moodle). Put your name on projects you are interested in doing.

Here's a bit more description on the projects that I posted.

I've mentioned some project ideas in class though:

 1. Building an Android's head

    - Take a rubber halloween mask and put it over a head "skeleton" where the mouth can be moved into a few positions with servos

    - Use speech recognition to create a text stream input

    - Feed it into a chat bot program. I could probably find an open source one online as writing my own could be out of scope unless it's just super barebones like `if(strcmp(voiceInput, "hello") = 0) { say("hello"); }`

    - Use speech synthesis to redirect the chat bot text output to a speaker

    - *Seems* like a lot more work than it actually __would__ be. The chat bot is really the only super complex thing there.

 2. Robot Dog (Fetch Bot)

    - Lot's of things could be here and make it out of scope, so only one should be implemented: playing fetch.

    - "Dog" has a robot body that can move different directions

    - Uses camera and the OpenCV library to do object tracking on a green ball

    - Moves body to search for and move to ball, playing "fetch"

## Make

> Do the http://elinux.org/EBC_make exercise and put your Makefile in your repo

### Part A

> Build and run “Hello World” from the command line.

`gcc -g -c app.c -o app.o`

> In the above gcc command, name the target, dependency and command.

Target: app.o

Dependency: app.c

Command: `gcc` or I suppose more specifically `gcc -g -c <dependency> -o <target>`

> What does the –c option (from the previous step) tell the compiler to do?

It compiles the c source to an object file

> Link the object file and produce the final executable.

`gcc -g app.o -o app.arm`

The rest is making the Makefile, which is continued and added to in part B

### Part B

The next part requires making a makefile that compiles the `app.arm` file, but using variables, generic rules, phonies, etc.

I've elected to make the program a little more complicated so the Makefile can also be a bit more interesting as well by introducing header files

All I've done is move the C files into a `src` folder and made a second header/c file that has a `print_hello_world` function, nothing super crazy. Also I created a separate folder for object files since there's two of them now

The Makefile and project can be found in `hw05/make/`

## Installing the Kernel Source

When I run `uname -a`, I receive:

```
debian@beaglebone:~/EmbeddedLinuxClass/hw05/make$ uname -a
Linux beaglebone 5.8.10-bone16 #1 PREEMPT Thu Sep 24 15:42:38 EDT 2020 armv7l GNU/Linux
```

Which shows I'm using the compiled 5.8.10 kernel

## Cross-Compiling

> Do the https://elinux.org/EBC_Exercise_08a_Cross-Compiling exercise and capture the output of the “Hello World” program from both the host and the Bone. Put the output in your memo.

### Host Output

```
dylan@dylanarch ~/Documents/School/2020-21/ECE/434/exercises (master*) $ gcc helloWorld.c 
dylan@dylanarch ~/Documents/School/2020-21/ECE/434/exercises (master*) $ file a.out 
a.out: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=261de81ee7cebd4725da05c652b194f0fe0d3ab7, for GNU/Linux 3.2.0, not stripped
dylan@dylanarch ~/Documents/School/2020-21/ECE/434/exercises (master*) $ ./a.out
Hello, World! Main is executing at 0x56052c510149
This address (0x7fffbcc68480) is in our stack frame
This address (0x56052c513040) is in our bss section
This address (0x56052c513038) is in our data section
```

### Cross-compiling on host

```
dylan@dylanarch ~/Documents/School/2020-21/ECE/434/exercises (master*) $ source ../crossCompileEnv.sh
dylan@dylanarch ~/Documents/School/2020-21/ECE/434/exercises (master*) $ ${CROSS_COMPILE}gcc helloWorld.c
dylan@dylanarch ~/Documents/School/2020-21/ECE/434/exercises (master*) $ file a.out
a.out: ELF 32-bit LSB executable, ARM, EABI5 version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux-armhf.so.3, for GNU/Linux 3.2.0, with debug_info, not stripped
```

Looks good to go!

### Running on beagle

After scping it over:

```
debian@beaglebone:~/EmbeddedLinuxClass$ ~/a.out 
Hello, World! Main is executing at 0x103dd
This address (0xbe8b50fc) is in our stack frame
This address (0x21030) is in our bss section
This address (0x21028) is in our data section
```

## Kernel Modules

> Modify gpio_test (http://derekmolloy.ie/kernel-gpio-programming-buttons-and-leds) to copy P9_15 to P9_16. Have it trigger for both rising and falling edges.
> 
> Modify the gpio _test example to take two button inputs (P18_15 and P8_18) and two LED outputs (P9_12 and P9_14).

The code for this is in `kernel/part1`

> modify the led example to flash two LEDs, each at a different rate. (See Example 3.)
>
> Hint: To get the led example to run you will have to change the permissions on lines 81 and 82 of led.c. Change the 666 to 660 on each.

The code for this is in `kernel/part2`
